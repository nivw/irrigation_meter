# Irrigation meter

Connect your IoT beaglebone black to a cheap flow meter and get graphes for current flow rate and accumalated water flow.<br/>

Result would look like this:</br>
1. [bounces](https://github.com/nivw/irrigation_meter/blob/master/demo_graphes/water.flow.bounces.open.faucet.png) is the current flow rate, and as you can see, when opening a faucet, the air is pushed out of the pipe causing bouncy flow rate.</br>
2. [flow counter](https://github.com/nivw/irrigation_meter/blob/master/demo_graphes/water.flow.count.png) , is the accumalated bounces throgh the sensor.</br>

## Hardware:
1. [Beaglebone black](https://beagleboard.org/black)</br>
2. [Water Flow sensor](http://www.seeedstudio.com/wiki/G3/4_Water_Flow_sensor)</br>

### Connection:<br/>
- connect the beaglebone pin P9_15 to the yellow sensor pin. Also supply +5V to the red sensor and GND.
- You need to use a pull-up for P5_15, either via using the beaglebone devicetree or by a 1K resistor from this pin to 3.3v+

## Software:
- install the image for debian 8.4 from [rcn-ee](http://beagleboard.org/latest-images)

### Notes:
- This installs the graphite packages and uses gunicorn to serve the graphes.
- To reduce flash wear due to many writes, I use the Ram to store the graphitefiles, and copy them to flash every 15 min.
- I use systemd service to run a simple python script to epoll the GPIO sensor
- Graphite webapp is available at port 8888 of the beaglebone IP.
	    