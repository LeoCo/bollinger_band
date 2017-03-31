import time
from livedata import livedata as livedata
from engine import engine as engine

class dispatcher(object):


    def __init__(self):
        pass

    def run(self, interval=1):

        self.live = engine(time_window=5, interval=interval)

        self.live.init_bollingerbands()

        self.live.run(graphics=True)



if __name__ == '__main__':
    print('Test of the dispatcher')

    dis = dispatcher()

    dis.run()