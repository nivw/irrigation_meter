Irrigation meter
====

Connect your IoT beaglebone black to a cheap flow meter and get graphes for current flow rate and accumalated water flow.<br/>

***********
Hardware:
----------
1. Beaglebone black: https://beagleboard.org/black
2. Water Flow sensor: http://www.seeedstudio.com/wiki/G3/4_Water_Flow_sensor

Connection:<br/>
   - connect the beaglebone pin P9_15 to the yellow sensor pin. Also supply +5V to the red sensor and GND.

***********
Software:
----------
   - install the image for debian 8.4 from http://beagleboard.org/latest-images

================================================================
   - This installs the graphite packages
   - create a tmpfs and moves the graphite files to it, then use a systemd timer to backup the files to the flash. This is done in order to reduce flash wear.
   - It uses systemd service to run a simple python script to epoll the GPIO sensor
   - Graphite webapp is available at port 8888 of the beaglebone IP.