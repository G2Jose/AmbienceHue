import time
import struct
import Quartz.CoreGraphics as CG
import numpy as np
from phue import Bridge
import colorsys
import time
import contextlib

BRIDGE_IP = '10.88.111.1'
LEFT_LIGHT = 2
RIGHT_LIGHT = 1
TRANSITION_TIME = 0.1
WIDTH = 50

@contextlib.contextmanager
def timer(msg):
    start = time.time()
    yield
    end = time.time()
    print("Framerate:\t", str(1.0 / (end - start)))
    print("Time:\t", str(end - start))



class Screen:
    def capture(self, region = None):
        if region == None:
            region = CG.CGRectInfinite
        else:
            region = CG.CGRectMake(region)
        image = CG.CGWindowListCreateImage(region, CG.kCGWindowListOptionOnScreenOnly, CG.kCGNullWindowID, CG.kCGWindowImageDefault)
        provider = CG.CGImageGetDataProvider(image)
        self._data = CG.CGDataProviderCopyData(provider)
        self.width = CG.CGImageGetWidth(image)
        self.height = CG.CGImageGetHeight(image)
        imgdata=np.fromstring(self._data,dtype=np.uint8).reshape(len(self._data)/4,4)
        return imgdata[:self.width*self.height,:-1].reshape(self.height,self.width,3)

def rgb2hsv(color):
    r, g, b = color
    _h, _s, _v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    h = int(_h * 65535)
    s = int(_s * 255)
    v = int(_v * 255)
    return h, s, v

class Hue:
    def __init__(self, ip):
        self.b = Bridge(ip)
        self.b.connect()
        self.RIGHT = RIGHT_LIGHT
        self.LEFT = LEFT_LIGHT
        self.TRANSITION_TIME = TRANSITION_TIME
        self.b.lights[self.LEFT].transitiontime = self.TRANSITION_TIME
        self.b.lights[self.RIGHT].transitiontime = self.TRANSITION_TIME
        self.blink(self.LEFT)
        self.blink(self.RIGHT)
        self.debug()
    
    def debug(self):
        for i, light in enumerate(self.b.lights):
            print(light)

    def off(self, light):
        self.b.set_light(light, 'on', False)

    def on(self, light):
        self.b.set_light(light, 'on', True)

    def set_color_hsv(self, light, color):
        h, s, v = color
        command = {'hue': (h), 'sat': (s), 'bri': (v)}
        self.b.set_light(light, command)

    def set_color_rgb(self, light, color):
        self.set_color_hsv(light, rgb2hsv(color))

    def blink(self, light, times = 1):
        for i in range(times):
            self.off(light)
            time.sleep(0.5)
            self.on(light)
            time.sleep(0.5)

h = Hue(BRIDGE_IP)
h.set_color_rgb(1, (255, 255, 255))

sp = Screen()

while True:
    try:
        img = sp.capture()
        left = img[:, 0:WIDTH, :]
        right = img[:, -WIDTH:, :]
        lr, lg, lb = np.mean(left[:, :, 0]), np.mean(left[:, :, 1]), np.mean(left[:, :, 2])
        rr, rg, rb = np.mean(right[:, :, 0]), np.mean(right[:, :, 1]), np.mean(right[:, :, 2])
        h.set_color_rgb(h.LEFT, (lr, lg, lb))
        h.set_color_rgb(h.RIGHT, (rr, rg, rb))
    except Exception:
        print('exception')
        pass
    except KeyboardInterrupt:
        h.set_color_rgb(h.LEFT, (255, 255, 255))
        h.set_color_rgb(h.RIGHT, (255, 255, 255))
        exit()


