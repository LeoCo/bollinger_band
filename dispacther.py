from engine import Engine as Engine

class Dispatcher(object):


    def __init__(self):
        pass

    def run(self):

        self.live = Engine(time_window=5, interval=1, bb_length=5)

        self.live.run(graphics=True,candlestick=False)


if __name__ == '__main__':
    print('Test of the dispatcher')

    dis = Dispatcher()

    dis.run()