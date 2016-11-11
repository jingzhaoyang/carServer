import cv2
import redis
import time

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(3, 320)
        self.video.set(4, 240)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tostring()

def capture():
    camera = VideoCamera()
    r =  redis.StrictRedis()
    while  True:
        value = camera.get_frame()
        r.set('video', value)
        time.sleep(0.1)


if __name__ == '__main__':
    capture()
