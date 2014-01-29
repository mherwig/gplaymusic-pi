from gmusicapi import Webclient
from mpd import MPDClient
from django.core.cache import cache

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.cache import cache

import json

from play_pi.models import *
from play_pi.settings import GPLAY_USER, GPLAY_PASS, SITE_ROOT

import logging
logger = logging.getLogger('play_pi')

api = Webclient()
api.login(GPLAY_USER,GPLAY_PASS)

client = MPDClient()
client.connect("localhost", 6600)

def home(request):
	if GPLAY_USER == "" or GPLAY_PASS == "":
		return render_to_response('error.html', context_instance=RequestContext(request))
	artists = cache.get('artists_all')
	if artists is None:
		artists = Artist.objects.all().order_by('name')
		cache.add('artists_all', artists)
	return render_to_response('index.html',
		{'list': artists, 'view':'artist'},
		context_instance=RequestContext(request))

def artist(request,artist_id):
	artist = Artist.objects.get(id=artist_id)
	albums = cache.get('albums_' + artist.name)
	if albums is None:
		albums = Album.objects.filter(artist=artist)
		cache.add('albums_' + artist.name, albums)
	return render_to_response('index.html',
		{'list': albums, 'artist': artist, 'view':'album'},
		context_instance=RequestContext(request))

def playlists(request):
	playlists = cache.get('playlists_all')
	if playlists is None:
		playlists = Playlist.objects.all()
		cache.add('playlists_all', playlists)
	return render_to_response('index.html',
		{'list': playlists, 'view':'playlist'},
		context_instance=RequestContext(request))

def playlist(request,playlist_id):
	playlist = Playlist.objects.get(id=playlist_id)
	tracks = [pc.track for pc in PlaylistConnection.objects.filter(playlist=playlist)]
	return render_to_response('playlist.html',
		{'playlist': playlist, 'tracks': tracks},
		context_instance=RequestContext(request))

def album(request,album_id):
	album = Album.objects.get(id=album_id)
	tracks = Track.objects.filter(album=album).order_by('track_no')
	return render_to_response('album.html',
		{'album': album, 'tracks': tracks},
		context_instance=RequestContext(request))

def play_album(request,album_id):
	album = Album.objects.get(id=album_id)
	tracks = Track.objects.filter(album=album).order_by('track_no')
	urls = []
	for track in tracks:
		urls.append(reverse('get_stream',args=[track.id,]))
	mpd_play(urls)
	current, status = get_current()
	if request.is_ajax():
		return HttpResponse(json.dumps({'artist': current.artist.name, 'name': current.name, 'status': status}), 'application/json')
	return HttpResponseRedirect(reverse('album',args=[album.id,]))
	
def play_artist(request,artist_id):
	artist = Artist.objects.get(id=artist_id)
	albums = Album.objects.filter(artist=artist)
	urls = []
	for album in albums:
		tracks = Track.objects.filter(album=album).order_by('track_no')
		for track in tracks:
			urls.append(reverse('get_stream',args=[track.id,]))
	mpd_play(urls)
	current, status = get_current()
	if request.is_ajax():
		return HttpResponse(json.dumps({'artist': current.artist.name, 'name': current.name, 'status': status}), 'application/json')
	return HttpResponseRedirect(reverse('artist',args=[artist.id,]))
	
def play_playlist(request,playlist_id):
	playlist = Playlist.objects.get(id=playlist_id)
	tracks = [pc.track for pc in PlaylistConnection.objects.filter(playlist=playlist)]
	urls = []
	for track in tracks:
		urls.append(reverse('get_stream',args=[track.id,]))
	mpd_play(urls)
	current, status = get_current()
	if request.is_ajax():
		return HttpResponse(json.dumps({'artist': current.artist.name, 'name': current.name, 'status': status}), 'application/json')
	return HttpResponseRedirect(reverse('playlist',args=[playlist.id,]))

def get_stream(request,track_id):
	track = Track.objects.get(id=track_id)
	url = get_gplay_url(track.stream_id)
	return HttpResponseRedirect(url)

def play_track(request,track_id):
	url = reverse('get_stream',args=[track_id,])
	mpd_play([url,])
	current, status = get_current()
	if request.is_ajax():
		return HttpResponse(json.dumps({'artist': current.artist.name, 'name': current.name, 'status': status}), 'application/json')
	return HttpResponseRedirect(request.GET.get('to', '/'))

def stop(request):
	client = get_client()
	client.clear()
	client.stop()
	if request.is_ajax():
		return HttpResponse(json.dumps(client.status()), 'application/json')
	return HttpResponseRedirect(request.GET.get('to', '/'))
	
def random(request):
	client = get_client()
	status = client.status()
	client.random(1 - int(status['random']))
	if request.is_ajax():
		return HttpResponse(json.dumps(client.status()), 'application/json')
	return HttpResponseRedirect(request.GET.get('to', '/'))

def repeat(request):
	client = get_client()
	status = client.status()
	client.repeat(1 - int(status['repeat']))
	if request.is_ajax():
		return HttpResponse(json.dumps(client.status()), 'application/json')
	return HttpResponseRedirect(request.GET.get('to', '/'))
	
def pause(request):
	client = get_client()
	status = client.status()
	state = status['state']

	if state == 'play':
		client.pause(1)
	elif state == 'pause':
		client.pause(0)
	if request.is_ajax():
		return HttpResponse(json.dumps(client.status()), 'application/json')
	return HttpResponseRedirect(request.GET.get('to', '/'))
		
def get_current():
	client = get_client()
	status = client.status()
	try:
		stream_url = client.currentsong()['file'].rstrip('/')
		index = stream_url.rfind("/")
		track_id = stream_url[index+1:]
		track = Track.objects.get(id=track_id)
	except KeyError:
		track = ""
	return track, status

def get_gplay_url(stream_id):
	global api
	try:
		url = api.get_stream_urls(stream_id)[0]
	except:
		api.login(GPLAY_USER,GPLAY_PASS)
		url = api.get_stream_urls(stream_id)[0]
	return url

def mpd_play(urls):
	client = get_client()
	client.clear()
	for url in urls:
		client.add(SITE_ROOT + url)
	client.play()

def get_client():
	global client
	try:
		client.status()
	except:
		client.connect("localhost", 6600)
	return client
