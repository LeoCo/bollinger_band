from engine import Engine as Engine
import timeit

class Dispatcher(object):


    def __init__(self):
        pass

    def run(self):

        self.live = Engine(time_window=20, interval=0.00001, bb_length=20)

        self.live.run(loops=101200)


if __name__ == '__main__':
    start = timeit.default_timer()

    print('Trading starts')

    dis = Dispatcher()



    dis.run()

    stop = timeit.default_timer()
    print('Execution time: ' + str(stop - start))