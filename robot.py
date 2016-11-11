#!/usr/bin/python
#coding: utf8
import RPi.GPIO as GPIO
import time
import sys
import threading
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
import json
import redis
import sys
from camera import VideoCamera, capture

tornado.options.define("port",default=80,type=int)

IN1 = 11
IN2 = 12
IN3 = 16
IN4 = 18


stop_status = 0
last_key = ""
last_request_time = 0
r =  redis.StrictRedis()

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(IN1,GPIO.OUT)
    GPIO.setup(IN2,GPIO.OUT)
    GPIO.setup(IN3,GPIO.OUT)
    GPIO.setup(IN4,GPIO.OUT)

# 前进
def forward():
    global stop_status
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)

# 后退
def reverse():
    global stop_status
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)


# 左转弯
def left():
    global stop_status
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)

# 右转弯
def right():
    global stop_status
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)

def stop_car():
    GPIO.output(IN1,False)
    GPIO.output(IN2,False)
    GPIO.output(IN3,False)
    GPIO.output(IN4,False)
    global stop_status
    stop_status = 1

def close_car():
    global stop_status
    stop_status = 1
    GPIO.cleanup()


class IndexHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', '*')
    def get(self):
        self.render("index.html")
    def post(self):
        global stop_status
        global last_key
        global last_request_time
        old_request_time = last_request_time
        init()
        sleep_time = 0.1
        try:
            arg = self.get_argument('k')
            new_request_time = self.get_argument('time')
            print 'get last time',new_request_time
        except Exception, e:
            arg = json.loads(self.request.body)['k']
            new_request_time = json.loads(self.request.body)['time']
            print 'json last time', new_request_time

        print "==new time ==", new_request_time
        print "==old time ==", old_request_time
        if(arg=='w' and last_key!='w' and new_request_time >= old_request_time):
            print "forward"
            stop_status = 0
            autoThread = threading.Thread(target = forward)
            autoThread.start()
            last_key = 'w'
        elif(arg=='s' and last_key!='s' and new_request_time >= old_request_time):
            print "reverse"
            stop_status = 0
            autoThread = threading.Thread(target = reverse)
            autoThread.start()
            last_key = 's'
        elif(arg=='a' and last_key!='a' and new_request_time >= old_request_time):
            print "left"
            stop_status = 0
            autoThread = threading.Thread(target = left)
            autoThread.start()
            last_key = 'a'
        elif(arg=='d' and last_key!='d' and new_request_time >= old_request_time):
            print "right"
            stop_status = 0
            autoThread = threading.Thread(target = right)
            autoThread.start()
            last_key = 'd'
        elif(arg=='stop' and new_request_time >= old_request_time):
            print "stop"
            last_key = "stop"
            time.sleep(0.3)
            stop_car()
        else:
            print "error"
        last_request_time = new_request_time
        self.write(arg)
    def options(self):
            pass
class VideoHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', '*')
    def get(self):
        image = r.get('video')
        self.write(image)



if __name__ == '__main__':
    captureThread = threading.Thread(target = capture)
    captureThread.start()
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r'/',IndexHandler), (r'/video_feed', VideoHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()
