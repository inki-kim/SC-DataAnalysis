# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, DateTime, Integer

from .mariadb_engine import Base


class TB_Analysis(Base):
    __tablename__ = 'TB_Analysis'

    data_code = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    slot_1 = Column(String(100))
    slot_2 = Column(String(100))
    slot_3 = Column(String(100))
    slot_4 = Column(String(100))
    final_slot = Column(String(100))
    data_content = Column(String)
    data_link = Column(String(500))
    upload_date = Column(DateTime)

    def __init__(self, slot_1, slot_2, slot_3, slot_4, final_slot,
                 data_content, data_link, upload_date):
        self.slot_1 = slot_1
        self.slot_2 = slot_2
        self.slot_3 = slot_3
        self.slot_4 = slot_4
        self.final_slot = final_slot
        self.data_content = data_content
        self.data_link = data_link
        self.upload_date = upload_date

    def __repr__(self):
        return 'data_code : %d, slot_1 : %s, slot_2 : %s, slot_3 : %s, slot_4 : %s, final_slot : %s, ' \
               'data_content : %s, data_link : %s, upload_date : %s' % \
               (self.data_code, self.slot_1, self.slot_2, self.slot_3, self.slot_4, self.final_slot,
                self.data_content, self.data_link, self.upload_date)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


class Member(Base):
    __tablename__ = 'TB_Member'

    email = Column(String(40), primary_key=True)
    password = Column(String(40), unique=True)
    gender = Column(String(40))
    profile_image = Column(String(40))
    name = Column(String(40))
    phone_number = Column(String(40))
    birth = Column(String(40))

    def __init__(self, email=None, password=None, gender=None, profile_image=None, name=None,
                 phone_number=None, birth=None):
        self.email = email
        self.password = password
        self.gender = gender
        self.profile_image = profile_image
        self.name = name
        self.phone_number = phone_number
        self.birth = birth

    def __repr__(self):
        return "<Member(email=%s, password='%s', gender='%s', profile_image='%s', " \
               "name='%s', phone_number='%s', birth='%s')>" % (self.email, self.password, self.gender,
                                                               self.profile_image, self.name, self.phone_number,
                                                               self.birth)

    def to_dict(self):
        return {
            'email': self.email,
            'password': self.password,
            'gender': self.password,
            'profile_image': self.profile_image,
            'name': self.name,
            'phone_number': self.phone_number,
            'birth': self.birth
        }
