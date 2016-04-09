# JTSWeer

# Introduction

Weather dashboard for Raspberry pi.

# Installation

 * apt-get install libffi-dev
 * sudo pip install pygal
 * sudo pip install matplotlib
 * sudo pip install cairosvg
 
## Kiosk mode

 * disable lightdm
 * upstart script in /etc/init/jtsweer.conf (see [ubuntu kiosk][1])
 * sudo apt-get install upstart
 * 
 
 [1]: http://askubuntu.com/questions/490820/how-to-make-ubuntu-14-04-a-kiosk
 [2]: https://www.danpurdy.co.uk/web-development/raspberry-pi-kiosk-screen-tutorial/
 [3]: http://kivypie.mitako.eu/kivy-faq.html
 