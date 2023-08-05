import rich
import sys



class Read:
    @staticmethod
    def run():
        ...


class Last:
    @staticmethod
    def run():
        ...


class Info:
    @staticmethod
    def run():
        ...


FLAGS: dict = {
    "-r": Read,
    "-l": Last,
    "-i": Info
}

args = sys.argv[1: len(sys.argv)]

for item in args:
    worker = FLAGS.get(item)

    if worker:
        worker.run()
