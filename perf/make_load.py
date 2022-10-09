import requests
import argparse
from time import time
from multiprocessing import Process

parser = argparse.ArgumentParser(description='App params')
parser.add_argument(
    '--threads',
    help='num of http workers',
    type=int,
)
parser.set_defaults(threads=1)
args = parser.parse_args()


def worker(thread_num):
    requests_handled = 0

    while True:
        start = time()
        requests.get('http://localhost:5000/api/post/2856/details')
        requests_handled += 1
        print(time() - start)
        print('thread #{}; total responses: {} '.format(
            thread_num,
            requests_handled,
        ))


def main():
    for i in range(0, args.threads):
        thread = Process(target=worker, args=(i,))
        thread.start()
        thread.join()


if __name__ == '__main__':
    main()
