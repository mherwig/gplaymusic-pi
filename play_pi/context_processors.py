from mpd import MPDClient
from play_pi.models import *

def mpd_status(request):
	client = MPDClient()
	client.connect("localhost", 6600)
	status = client.status()
	client.disconnect()
	return {'mpd_status': status}

def artists_playlists_count(request):
	artists_count = Artist.objects.all().count()
	playlists_count = Playlist.objects.all().count()
	return {'artists_count': artists_count, 'playlists_count': playlists_count}

def current_track(request):
	client = MPDClient()
	client.connect("localhost", 6600)
	stream_url = client.currentsong()['file'].rstrip('/')
	index = stream_url.rfind("/")
	track_id = stream_url[index+1:]
	current_track = Track.objects.get(id=track_id)
	client.disconnect()
	return {'current_track': current_track}
