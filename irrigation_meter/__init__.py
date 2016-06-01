#!/usr/bin/python
import time
from socket import socket
import os
import select

#taken from irrigation-bone/wfs_config.py
gpio_base = '/sys/class/gpio'
gpio = '48' #P9_15
WATERFLOW_TIMEOUT = 60 #no water flow for a minute

gpio_path = os.path.join( gpio_base, 'gpio' + gpio )
gpio_value = os.path.join(gpio_path, 'value')

def main():
  accumulated_value = 0
  sock = socket()
  sock.connect( ('127.0.0.1', 2003) )
  previous_timestamp = timestamp = int( time.time() )
  with open(gpio_value) as gpio_fd:
    po = select.epoll()
    po.register(gpio_fd, select.EPOLLIN | select.EPOLLET)  
    while True:
      events = po.poll( WATERFLOW_TIMEOUT )
      timestamp = int( time.time() )
      gpio_fd.seek(0)
      value = gpio_fd.read().strip()
      if previous_timestamp == timestamp:
        accumulated_value +=1
      else:
        accumulated_value = 0
      message = 'water.flow.count {} {}\n' .format(accumulated_value, timestamp)
      print message
      sock.sendall(message)
      previous_timestamp = timestamp
  sock.close()

if __name__ == "__main__":
      main()
