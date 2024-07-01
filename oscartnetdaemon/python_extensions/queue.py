from multiprocessing import Queue


def clear(queue: Queue):
    while not queue.empty():
        queue.get()
