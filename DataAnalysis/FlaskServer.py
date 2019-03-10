# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask_restful import Api

from serverscenter_mariadb.mariadb_engine import db_session
from serverscenter_restapi import member_api, message_api

application = Flask(__name__)
application.config.from_object(__name__)
application.config.update(dict(
    JSONIFY_PRETTYPRINT_REGULAR=False
))
application.config.from_envvar('FLASK_SERVER_SETTINGS', silent=True)

api = Api(application)


@application.teardown_appcontext
def shutdown_dbsession(exception=None):
    db_session.remove()


@application.route('/')
def index():
    return jsonify({'status': 'success'})


api.add_resource(member_api.MemberLogin, '/api/member/login')
api.add_resource(message_api.MessageResponse, '/api/message')


# app.debug=True 는 서버가 코드 변경을 감지하고 자동으로 리로드, 문제 발생시 디버거 제공한다.
# 대화식 디버거는 임의의 코드가 실행될수 있기 때문에 보안취약점 가능성으로 운영환경에서는 [절대 사용하지 말아야 한다].
def run():
    application.run(debug=False, host='0.0.0.0', port=5050)


if __name__ == '__main__':
    run()
