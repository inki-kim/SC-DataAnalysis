# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse

from serverscenter_mariadb.mariadb_engine import db_session
from serverscenter_mariadb.mariadb_model import Member


class MemberLogin(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()

            _memberEmail = args['email']
            _memberPassword = args['password']

            member = db_session.query(Member).filter_by(email=_memberEmail, password=_memberPassword).first()

            if member is None:
                return {'status': 'failed'}

            return {'status': 'success'}
        except Exception as e:
            return {'error': str(e)}
