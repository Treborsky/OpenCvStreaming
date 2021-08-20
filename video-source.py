import cv2 as cv
import numpy as np
import imutils
import pickle
import socket
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = '127.0.0.1' # loopback ip
print('HOST_IP: ', host_ip)
port = 9999
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen()
print('Listening at', socket_address)

def start_video_stream():
  client_socket, addr = server_socket.accept()
  camera = False
  if camera == True:
    vid = cv.VideoCapture(0)
  else:
    vid = cv.VideoCapture('videos/vid1.mp4')

  try:
    print('CLIENT {} CONNECTED!'.format(addr))
    if client_socket:
      while (vid.isOpened()):
        img, frame = vid.read()

        frame = imutils.resize(frame, width=320)
        a = pickle.dump(frame)
        message = struct.pack("Q", len(a)) + a
        client_socket.sendall(message)
        cv.imshow('TRANSMITTING TO CACHE SERVER', frame)
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
          client_socket.close()
          break

  except Exception as e:
    print(f'CACHE SERVER {addr} DISCONNECTED')
    pass

while True:
  start_video_stream()
  
