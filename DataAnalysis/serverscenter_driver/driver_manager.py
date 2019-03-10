# -*- coding: utf-8 -*-
import os

from selenium import webdriver

from custom_class import SingletonInstance


class DriverManager(SingletonInstance):
    def __init__(self):
        self.linux_driver_path = "/driver_chrome_2.38_linux64.exe"
        self.window_driver_path = "/driver_chrome_2.38_win32.exe"

    def __enter__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-gpu-sandbox')
        self.options.add_argument('--disable-impl-side-painting')
        self.options.add_argument('--disable-accelerated-2d-canvas')
        self.options.add_argument('--disable-accelerated-jpeg-decoding')
        self.driver = webdriver.Chrome(os.path.dirname(os.path.realpath(__file__))
                                       + self.linux_driver_path, options=self.options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()
