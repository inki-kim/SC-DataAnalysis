# -*- coding: utf-8 -*-
import pandas as pd

from .mariadb_engine import db_session
from .mariadb_model import TB_Analysis


def show_table():
    rows = db_session.query(TB_Analysis)
    row_list = [dict(data_code=row.data_code, slot_1=row.slot_1, slot_2=row.slot_2,
                slot_3=row.slot_3, slot_4=row.slot_4, final_slot=row.final_slot,
                data_content=row.data_content, data_link=row.data_link, upload_date=row.upload_date) for row in rows]
    for row in row_list:
        print(row)


def select_analysis_table_rows():
    rows = db_session.query(TB_Analysis)
    row_list = [dict(data_code=row.data_code, slot_1=row.slot_1, slot_2=row.slot_2,
                slot_3=row.slot_3, slot_4=row.slot_4, final_slot=row.final_slot,
                data_content=row.data_content, data_link=row.data_link, upload_date=row.upload_date) for row in rows]

    return row_list


def select_analysis_table_frame():
    queryset = db_session.query(TB_Analysis)
    frame = pd.read_sql(queryset.statement, queryset.session.bind)

    return frame


def insert(slot_1, slot_2, slot_3, slot_4, final_slot, data_content, data_link, upload_date):
    queries = db_session.query(TB_Analysis.data_link)
    link_list = list(q.data_link for q in queries)
    data_source = TB_Analysis(slot_1, slot_2, slot_3, slot_4, final_slot, data_content, data_link, upload_date)

    print(link_list)
    print(str(data_source.data_link))
    if data_source.data_link in link_list:
        # 중복감지
        print("중복 감지... 다음 링크로 이동...")
        return False
    else:
        db_session.add(data_source)
        db_session.commit()
        print(data_source.slot_1 + "---" + data_source.slot_2 + "---" + data_source.slot_3
              + data_source.final_slot + "   >>> added")


def delete(data_code, slot_1, slot_2, slot_3, slot_4, final_slot, data_content, data_link, upload_date):
    db_session.query(TB_Analysis).filter(TB_Analysis.data_code == data_code,
                                         TB_Analysis.slot_1 == slot_1,
                                         TB_Analysis.slot_2 == slot_2,
                                         TB_Analysis.slot_3 == slot_3,
                                         TB_Analysis.slot_4 == slot_4,
                                         TB_Analysis.final_slot == final_slot,
                                         TB_Analysis.data_content == data_content,
                                         TB_Analysis.data_link == data_link,
                                         TB_Analysis.upload_date == upload_date).delete()
    db_session.commit()
