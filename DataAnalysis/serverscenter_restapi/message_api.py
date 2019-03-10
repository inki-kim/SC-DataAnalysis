# -*- coding: utf-8 -*-
import mecab
import pandas as pd
from flask import request, jsonify
from flask_restful import Resource
from sklearn.feature_extraction.text import TfidfVectorizer

from serverscenter_mariadb.mariadb_query import select_analysis_table_frame


class MessageResponse(Resource):
    def get(self):
        args = request.args
        received_message = args['msg']

        analysis_frame = select_analysis_table_frame()
        print(analysis_frame)

        question_nouns = ''

        final_slot_max_tfidf_value = 0.0
        final_slot_nouns = ''

        analysis_frame['slot_str'] = pd.Series(analysis_frame['slot_1'] + ' ' + analysis_frame['slot_2'] + ' ' + analysis_frame['slot_3'] + ' ' + analysis_frame['slot_4'])
        print(analysis_frame['slot_str'])

        tagger = mecab.MeCab()
        print("메캡 객체 생성 완료.")

        nouns = tagger.nouns(received_message)
        print("메캡 동사 추출 완료")
        for noun in nouns:
            question_nouns += noun + ' '

        result = ""
        
        print('question : ' + received_message)
        print('question_nouns : ' + question_nouns + '\n')
        
        for index, row in analysis_frame.iterrows():
            slots_nouns = ''
            nouns = tagger.nouns(row['slot_str'])
            for noun in nouns:
                slots_nouns += noun + ' '

            calc_list = list()
            calc_list.append(question_nouns)
            calc_list.append(slots_nouns)
            print('slots calc data : ' + str(calc_list) + '\n')

            tfidf_vectorizer = TfidfVectorizer(min_df=1)
            tfidf_matrix = tfidf_vectorizer.fit_transform(calc_list)
            document_distances = (tfidf_matrix * tfidf_matrix.T)
            print('slots and question - document_distances : ' + str(document_distances.toarray()[0][1]))

            if document_distances.toarray()[0][1] >= 0.8:
                result += str(row['final_slot']) + ' at ' + str(row['upload_date']) + ' / '


            nouns = tagger.nouns(row['final_slot'])
            final_slot_nouns = slots_nouns + ' '

            for noun in nouns:
                final_slot_nouns += noun + ' '

            calc_list = list()
            calc_list.append(question_nouns)
            calc_list.append(final_slot_nouns)

            print('final slot calc data : ' + str(calc_list) + '\n')

            tfidf_vectorizer = TfidfVectorizer(min_df=1)
            tfidf_matrix = tfidf_vectorizer.fit_transform(calc_list)
            document_distances = (tfidf_matrix * tfidf_matrix.T)
            print('final slot and question - document_distances : ' + str(document_distances.toarray()[0][1]))

            if document_distances.toarray()[0][1] >= 0.85:
                result = row['data_content']
                break

        if result == "":
            result = "일치할 것으로 예상되는 값이 없습니다."

        # 딕셔너리로 변환
        # json_dict = dict(json.loads(return_m))
        # print(json_dict.keys())
        # print(json_dict.values())
        print("받은 메세지 :" + received_message)

        return jsonify({'result': result})
