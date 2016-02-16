import time
import struct
import collections
from phue import Bridge
import Quartz.CoreGraphics as CG
import colorsys

BRIDGE_IP = '192.168.0.10'
LEFT_LIGHT = 3
RIGHT_LIGHT  = 1
# LEFT_LIGHT = 3
# RIGHT_LIGHT  = 2
TRANSITION_TIME = 0.1

class ScreenPixel(object):
    def capture(self, region = None):
        if region is None:
            region = CG.CGRectInfinite
        else:
            
            if region.size.width % 2 > 0:
                emsg = "Capture region width should be even (was %s)" % (
                    region.size.width)
                raise ValueError(emsg)

        image = CG.CGWindowListCreateImage(
            region,
            CG.kCGWindowListOptionOnScreenOnly,
            CG.kCGNullWindowID,
            CG.kCGWindowImageDefault)

        prov = CG.CGImageGetDataProvider(image)

        self._data = CG.CGDataProviderCopyData(prov)

        self.width = CG.CGImageGetWidth(image)
        self.height = CG.CGImageGetHeight(image)

    def pixel(self, x, y):



        data_format = "BBBB"


        offset = 4 * ((self.width*int(round(y))) + int(round(x)))


        b, g, r, a = struct.unpack_from(data_format, self._data, offset=offset)
        color = collections.namedtuple('color', ['r', 'g', 'b', 'a'])
        c = color(r = r, g = g, b = b, a = a)
        return c


if __name__ == '__main__':
    # Timer helper-function
    import contextlib

    @contextlib.contextmanager
    def timer(msg):
        start = time.time()
        yield
        end = time.time()
        # print "%s: %.02fs" % (msg, (end-start))
        print "%s: %.02ffps" % ("Framerate:\t", 1.0/(end-start))
        print "%s: %.02fs" % (msg, (end-start))

    b = Bridge(BRIDGE_IP)
    b.connect()
    b.set_light(LEFT_LIGHT+1, 'on', True)
    b.set_light(RIGHT_LIGHT+1, 'on', True)
    lights = b.lights
    lights[LEFT_LIGHT].transitiontime = TRANSITION_TIME
    lights[RIGHT_LIGHT].transitiontime = TRANSITION_TIME

    lights[LEFT_LIGHT].on = True
    lights[RIGHT_LIGHT].on = True

    sp = ScreenPixel()
    sp.capture()

    COL_INTERVAL = 50
    ROW_INTERVAL = 100
    WIDTH = sp.width/20
    HEIGHT = sp.height
    print "---PARAMETERS---"
    print "width: \t", WIDTH
    print "height: \t", HEIGHT
    print "Rows being processed:\t", int(HEIGHT / ROW_INTERVAL)
    print "Cols being processed:\t", int(WIDTH / COL_INTERVAL)
    print "Pixels being processed:\t", int(WIDTH / COL_INTERVAL) * int(HEIGHT / ROW_INTERVAL)
    
    i = 0
    while True:
        ++i
        # if (i%100 == 0): 
        #     b.connect()
        # with timer ("Capture"):
        sp.capture()
        avg_r = 0
        avg_g = 0
        avg_b = 0
        with timer("Computation time:\t"): 

            avg_r = 0
            avg_g = 0
            avg_b = 0
            for col in range(WIDTH):
                for row in range(HEIGHT):
                    if row % ROW_INTERVAL == 0 and col % COL_INTERVAL == 0:
                        # print(sp.pixel(row, col))
                        avg_r += sp.pixel(col, row).r
                        avg_g += sp.pixel(col, row).g
                        avg_b += sp.pixel(col, row).b
                        # print (row, col, avg_r)
            avg_r = avg_r / (WIDTH * HEIGHT / COL_INTERVAL / ROW_INTERVAL)
            avg_g = avg_g / (WIDTH * HEIGHT / COL_INTERVAL / ROW_INTERVAL)
            avg_b = avg_b / (WIDTH * HEIGHT / COL_INTERVAL / ROW_INTERVAL)
            h, s, v = colorsys.rgb_to_hsv((avg_r+0.0)/255, (avg_g+0.0)/255, (avg_b+0.0)/255)
            command = {'hue': int(h * 65535), 'sat': int(s * 255), 'bri': int(v * 255)}
            
            # print "\nLeft HSV: ", h, s, v
            # print "Left RGB: ", avg_r, avg_g, avg_b
            b.set_light(LEFT_LIGHT+1, command)

            avg_r = 0
            avg_g = 0
            avg_b = 0
            for col in range(sp.width - WIDTH, sp.width):
                    for row in range(HEIGHT):
                        if row % ROW_INTERVAL == 0 and col % COL_INTERVAL == 0:
                            # print(sp.pixel(row, col))
                            avg_r += sp.pixel(col, row).r
                            avg_g += sp.pixel(col, row).g
                            avg_b += sp.pixel(col, row).b
                            # print (row, col, avg_r)
            avg_r = avg_r / (WIDTH * HEIGHT / COL_INTERVAL / ROW_INTERVAL)
            avg_g = avg_g / (WIDTH * HEIGHT / COL_INTERVAL / ROW_INTERVAL)
            avg_b = avg_b / (WIDTH * HEIGHT / COL_INTERVAL / ROW_INTERVAL)
            h, s, v = colorsys.rgb_to_hsv((avg_r+0.0)/255, (avg_g+0.0)/255, (avg_b+0.0)/255)
            command = {'hue': int(h * 65535), 'sat': int(s * 255), 'bri': int(v * 255)}
            
            # print "\nRight HSV: ", h, s, v
            # print "Right RGB: ", avg_r, avg_g, avg_b
            b.set_light(RIGHT_LIGHT+1, command)



















