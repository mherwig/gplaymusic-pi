from django.db import models

import time

class Artist(models.Model):
	name = models.CharField(max_length=200, unique=True)
	art_url = models.CharField(max_length=200)
	
	def get_albums(self):
		albums = Album.objects.filter(artist=self)
		return albums
	
	def get_latest_album(self):
		album = Album.objects.filter(artist=self).order_by('year').reverse()[:1].get()
		return album
		
	latest_album = property(get_latest_album)
	albums = property(get_albums)

class Album(models.Model):
	name = models.CharField(max_length=200)
	year = models.IntegerField(default=0)
	art_url = models.CharField(max_length=200)
	artist = models.ForeignKey(Artist)

class Track(models.Model):
	name = models.CharField(max_length=200)
	artist = models.ForeignKey(Artist)
	album = models.ForeignKey(Album)
	stream_id = models.CharField(max_length=100)
	track_no = models.IntegerField(default=0)
	duration = models.IntegerField(default=0)
	
	def get_formatted_duration(self):
		return time.strftime("%M:%S", time.gmtime(self.duration/1000))
	
	duration_formatted = property(get_formatted_duration)


class Playlist(models.Model):
	name = models.CharField(max_length=200)
	pid = models.CharField(max_length=200)

	def get_art_url(self):
		pc = PlaylistConnection.objects.filter(playlist=self)[0]
		track = pc.track
		return track.album.art_url

	art_url = property(get_art_url)
	
	def get_number_of_tracks(self):
		return PlaylistConnection.objects.filter(playlist=self).count()
		
	tracks_count = property(get_number_of_tracks)
		


class PlaylistConnection(models.Model):
	track = models.ForeignKey(Track)
	playlist = models.ForeignKey(Playlist)
