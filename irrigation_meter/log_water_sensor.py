#!/usr/bin/python
import time
from socket import socket
import os
import select

"""
This sensor: http://www.seeedstudio.com/wiki/G3/4_Water_Flow_sensor
Shows a coeff of 5.5 between pulse frequecy and flow rate.
when the flow rate is  2L/min it issues pulses at 11Hz
When the flow rate is 10L/min it issues pulses at 55Hz
sensor range is 1-60 L/min, so the frequency range is 5.5-330Hz
converting min -> sec:
range is 0.01667-1 L/sec
"""

gpio_base = '/sys/class/gpio'
gpio = '48' #P9_15
WATERFLOW_TIMEOUT = 60 #no water flow for a minute
DEBOUNCE_DELAY = 1/5.5  #sec

gpio_path = os.path.join( gpio_base, 'gpio' + gpio )
gpio_value = os.path.join(gpio_path, 'value')

def main():
  triggers_during_sec = last_litter_timestamp = 0
  previous_timestamp = timestamp = int( time.time() )
  sock = socket()
  sock.connect( ('127.0.0.1', 2003) )
  with open(gpio_value) as gpio_fd:
    po = select.epoll()
    po.register(gpio_fd, select.EPOLLIN | select.EPOLLET)  
    while True:
      events = po.poll( WATERFLOW_TIMEOUT )
      timestamp = time.time()
      gpio_fd.seek(0)
      value = gpio_fd.read().strip()
      if value == '1' :
        if (timestamp - last_litter_timestamp) > DEBOUNCE_DELAY:
          if int(last_litter_timestamp) != int(timestamp):
            current_litter = 1/5.5
          else:
            current_litter += 1/5.5
          message = 'water.flow.count {} {}\n' .format(current_litter, int(timestamp))
          sock.sendall(message)
          last_litter_timestamp = timestamp

        if int(previous_timestamp) == int(timestamp):
          triggers_during_sec += 1/5.5
        else:
          triggers_during_sec = 1/5.5
        message = 'water.flow.triggers {} {}\n' .format(triggers_during_sec, int(timestamp) )
        sock.sendall(message)
        previous_timestamp = timestamp
    po.unregister(gpio_fd)
  sock.close()

if __name__ == "__main__":
      main()
