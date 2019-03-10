# -*- coding: utf-8 -*-
import re
import urllib.request
import time
import pandas as pd
from bs4 import BeautifulSoup

from serverscenter_driver import DriverManager
from serverscenter_mariadb.mariadb_query import insert


class DongyangCrawler:
    def __init__(self):
        self.login_address = "https://portal.dongyang.ac.kr/login_real.jsp"
        self.login_id_name = "user_id"
        self.login_pw_name = "user_password"
        self.login_button_class = "btn_login"

        self.count=0
        self.slot_1 = ""
        self.slot_2 = ""
        self.slot_3 = ""
        self.slot_4 = ""
        self.final_slot = ""
        self.data_content = ""
        self.data_link = ""
        self.upload_date = ""

        self.browser = None

    def regexp_data_content(self):
        self.data_content = re.sub('<.+?>', '', self.data_content, 0, re.I | re.S)
        self.data_content = self.data_content.replace('\\u200b', '')
        self.data_content = self.data_content.replace('\\xa0', '')
        self.data_content = re.sub('[a-zA-Z]', '', self.data_content)
        self.data_content = re.sub('[\{\}\[\]\/?,;:|\)*`!^\-_+<>@\#$%&\\\=\(\'\"]', '', self.data_content)
        return True

    def soup_link_find_tag(self, link, tag_name):
        self.browser.driver.get(str(link))
        time.sleep(1)
        soup_result = BeautifulSoup(self.browser.driver.page_source, "html.parser")
        tag_zip = soup_result.find_all(str(tag_name))
        return tag_zip

    def page_move(self, tag_zip):
        cnt = 0
        self.count=0
        for tag in tag_zip:
            try:
                prop = tag.get('class')
                if prop is not None and prop[0] == "go":
                    cnt += 1
                if prop is not None and prop[0] == "btn_go" and prop[1] == "go_next":
                    tag_zip = self.soup_link_find_tag(tag.get('href'), "a")
            except UnicodeEncodeError:
                print("Error")

        if cnt != 11:
            return False
        else:
            return tag_zip

    def search(self, tag_zip, class_name, attribute, flag, data):
        if tag_zip is False:
            return

        for tag in tag_zip:
            try:
                prop = tag.get('class')
                if prop is not None and prop[0] == str(class_name):
                    if (tag.get(attribute)) is not None:
                        if flag == 1:
                            tag_zip = self.soup_link_find_tag(tag.get('href'), "a")
                            if self.search(tag_zip=tag_zip, class_name="ellipsis", attribute="href",
                                           flag=0, data=data) is False:
                                return
                        elif tag.get(attribute) == "#none":
                            print("읽을 권한이 없는 글입니다(비밀글). 다음 글로 넘어갑니다.")
                        else:
                            self.count+=1
                            if 10 < self.count:
                                self.count=0
                                return False
                            print(self.count)
                            self.slot_1 = data[0]
                            self.slot_2 = data[1]
                            self.slot_3 = data[2]
                            self.slot_4 = ""
                            self.final_slot = str(tag.get_text())
                            self.data_content=""
                            soup_result = BeautifulSoup(urllib.request.urlopen(str(tag.get(attribute))),
                                                        "lxml", from_encoding="utf-8")
                            for item in soup_result.find_all('div', class_="txt"):
                                self.data_content += str(item.find_all(text=True))

                            self.regexp_data_content()
                            self.data_link = str(tag.get(attribute))
                            self.upload_date = str(soup_result.find("span", class_="date").get_text())

                            if insert(self.slot_1, self.slot_2, self.slot_3, self.slot_4, self.final_slot,
                                      self.data_content, self.data_link, self.upload_date) is False:
                                return False

            except UnicodeEncodeError:
                print("Unicode Encode Error")

        if flag == 1:
            self.search(tag_zip=self.page_move(tag_zip), class_name="go", attribute="href",
                        flag=1, data=data)

    def start(self, dongyang_id, dongyang_pw):
        with DriverManager.instance() as browser:
            self.browser = browser
            self.browser.driver.get(self.login_address)
            self.browser.driver.find_element_by_name(self.login_id_name).send_keys(dongyang_id)
            self.browser.driver.find_element_by_name(self.login_pw_name).send_keys(dongyang_pw)
            self.browser.driver.find_element_by_class_name(self.login_button_class).click()
            time.sleep(1)
            excel_source = pd.read_excel("serverscenter_dataset/board_links.xlsx")
            indexing_source = excel_source.set_index("slot1").dropna(axis=0)
            for row in indexing_source.itertuples():
                self.browser.driver.get(row[3])
                page_source = self.browser.driver.page_source
                soup_result = BeautifulSoup(page_source, "html.parser")
                a_tag_zip = soup_result.find_all("a")

                self.search(tag_zip=a_tag_zip, class_name="go", attribute="href", flag=1, data=row)