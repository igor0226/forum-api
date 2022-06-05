import requests
import argparse
from multiprocessing import Process

parser = argparse.ArgumentParser(description='App params')
parser.add_argument(
    '--threads',
    help='num of http workers',
    type=int,
)
parser.set_defaults(threads=1)
args = parser.parse_args()


def worker():
    while True:
        requests.get('http://localhost:5000/api/post/2856/details')


if __name__ == '__main__':
    for _ in range(0, args.threads):
        thread = Process(target=worker)
        thread.start()
