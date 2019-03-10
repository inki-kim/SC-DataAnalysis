# -*- coding: utf-8 -*-
from multiprocessing import Process

import CrawlerApp
import FlaskServer

if __name__ == '__main__':
    processTest = Process(target=CrawlerApp.run)
    processFlask = Process(target=FlaskServer.run)

    processTest.start()
    processFlask.start()

    processTest.join()
    processFlask.join()
