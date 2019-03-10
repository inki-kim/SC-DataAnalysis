# -*- coding: utf-8 -*-
from serverscenter_config import ConfigManager
from serverscenter_crawling.dongyang_cralwer import DongyangCrawler


def _job_crawling():
    config = ConfigManager.instance()
    crawler = DongyangCrawler()

    crawler.start(dongyang_id=config.get_dongyang_id(), dongyang_pw=config.get_dongyang_pw())


def run():
    _job_crawling()


if __name__ == '__main__':
    _job_crawling()
