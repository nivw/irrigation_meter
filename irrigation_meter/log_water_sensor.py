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
  bounches_sum = bounches_during_sec = 0
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
        bounches_during_sec +=1
        message = 'water.flow.bounces {} {}\n' .format(bounches_during_sec, timestamp)
        sock.sendall(message)
      else:
        bounches_sum += bounches_during_sec
        bounches_during_sec = 0
      message = 'water.flow.count {} {}\n' .format(bounches_sum, timestamp)
      #print message
      sock.sendall(message)
      previous_timestamp = timestamp
    po.unregister(gpio_fd)
  sock.close()

if __name__ == "__main__":
      main()
