from engine import Engine as Engine

class Dispatcher(object):


    def __init__(self):
        pass

    def run(self, interval=1):

        self.live = Engine(time_window=10, interval=interval)

        self.live.init_bollingerbands(length=5)

        self.live.run(graphics=True,candlestick=False)


if __name__ == '__main__':
    print('Test of the dispatcher')

    dis = Dispatcher()

    dis.run()