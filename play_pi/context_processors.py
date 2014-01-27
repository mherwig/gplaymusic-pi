from mpd import MPDClient

def mpd_status(request):
	client = MPDClient()
	client.connect("localhost", 6600)
	status = client.status()
	state = status['state']
	client.disconnect()
	
	return {'mpd_status': status, 'mpd_status_state': state}
