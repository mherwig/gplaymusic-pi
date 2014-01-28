#gplaymusic-pi

gplaymusic-pi provides a web-frontend for browsing and playing music from a [Google Play Music](http://play.google.com/music/) library.
Installed on a RaspberryPi that you usally only access remotely, gmusicplay-pi allows you to turn your Raspi into a jukeboy playing music from your Google Play Music library without the need of having a VNC session for browsing songs.

gplaymusic-pi is a fork of [play-pi](https://github.com/fredley/play-pi) by [Tom Medley (fredley)](https://github.com/fredley) and is probably less stable and less flawless in its current state than the original project.
I strongly recommend to check out the original project as gplaymusic-pi is for testing purposes in its current state.

Note: The template isn't finished yet either! Some features might be missing.

![Screenshot](http://i.imgur.com/roqEV3h.png)

###Installation instructions (derived from the original project):

* Assuming you've got the Pi set up as you want, you'll need to install the required tools:
`sudo apt-get install mpd mpc python-mpd python-pip screen`
* Test that `mpc` is working by entering the command `sudo mpc`. You should see output like
*volume: 80%   repeat: off   random: off   single: off   consume: off*
* Next you'll need to use `pip` to install Django and gmusicapi:
`sudo pip install django`
`sudo pip install git+git://github.com/simon-weber/Unofficial-Google-Music-API.git@develop`
* Now clone this repository:
`git clone git://github.com/mherwig/gplaymusic-pi.git`
`cd play-pi`
* Create a file called `local_settings.py` in the same folder as `settings.py`. Add the following lines:
`GPLAY_USER="you@gmail.com"`
`GPLAY_PASS="your-password"`
It's highly recommended you use an [application specific password](https://support.google.com/accounts/answer/185833?hl=en) for this.
* Now set up the Django app with the following commands. This will create the database:
`./manage.py syncdb`
During this step you will be asked for a superuser name and password. You can use these to access the admin.
* Now sync your Google Music library. This can take a very long time (depends on the library size):
`./manage.py init_gplay`
* You're now ready to run the server! Start up a screen by typing `screen`. Running the server in the screen means that it will keep running after `ssh` is disconnected.
`sudo ./manage.py runserver 0.0.0.0:8080`
* You should now be able to access gplaymusic-pi from your web browser, point it at the IP of your Pi followed by the port.
* Note that starting the server on any other port requires you to change the settings.py accordingly.
* For better performance I suggest to use nginx and uwsgi. You find a pretty good tutorial [here](https://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html)
