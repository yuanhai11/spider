#!/usr/bin/python3
# -*- coding:utf-8 -*-
import requests
from flask import Flask, request, jsonify, make_response
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='RPA机器人API'
          )
# flask原生api页面
ns = api.namespace('rpa/api', description="RPA机器人")
response_model = api.model('Model', {
    'code': fields.Integer, 'data': fields.String, 'message': fields.String
    # 'code':fields.Integer,'data': fields.String,'message':fields.String,'type':fields.String,'company_id':fields.String
})
aaa = api.namespace('rpaapi', description="存入账号信息")
@aaa.route('/api/', methods=['post'])
@aaa.response(404, '接口调用失败')
@aaa.response(200, 'Success', response_model)
class GuessGender(Resource):
    @aaa.expect(aaa.model('Resource', {
        'type': fields.String(required=True, description='报税类型'),
        'declareId': fields.String(required=True, description='申报ID')
    }), validate=True)
    def post(self):
        '''添加待报税公司id信息信息'''
        todos = request.get_json()
        typeq = todos['type']
        company_id = todos['declareId']
        if company_id == '' and typeq == '':
            response = make_response(
                jsonify({'data': None, "message": '未接收到数据', 'code': 1}))
            return response
        if typeq == '':
            response = make_response(
                jsonify({'data': None, "message": '未接收到类型数据', 'code': 1}))
            return response
        if company_id == '':
            response = make_response(
                jsonify({'data': None, "message": '未接收到公司id数据', 'code': 1}))
            return response
        url = "http://127.0.0.1:2229"
        payload = "{'type':'%s','company_id':'%s'}" % (typeq, company_id)  # 添加待报税公司id信息信息
        print(payload)
        payload = payload.encode('utf-8')
        headers = {
            'Accept-Language':'zh-CN,zh;q=0.9',
        }
        res = requests.request("POST",url,headers=headers,data=payload).text.encode('latin-1').decode('utf8').replace('company_id','declareId')
        response = make_response(jsonify({'data': res, "message": '接口调用成功', 'code': 0}))
        return response
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=48050)