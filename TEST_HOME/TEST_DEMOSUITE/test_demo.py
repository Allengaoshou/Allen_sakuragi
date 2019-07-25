#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import unittest
from view import app,db
from model.Local_db import Link_home,Category,Duty,User

class TestClass(unittest.TestCase):
    def setup_class(self):
        """测试开始时候执行, 用来做准备工作，一般用来初始化资源。"""
        app.config['TESTING'] = True  # 这将会使得处理请求时的错误捕捉失效，以便于在进行对应用发出请求的测试时获得更好的错误反馈。
        # 测试客户端将会给我们一个通向应用的简单接口，我们可以激发 对向应用发送请求的测试，并且此客户端也会帮我们记录 Cookie 的 动态。
        self.app = app.test_client()
        self.db = db

    def teardown_class(self):
        """测试结束时执行， 用来做收尾工作， 一般用来关闭资源"""
        pass


    def test_changebegin_time(self):
        # response = self.app.get('/login')
        # activityId = self.app.
        response = app.test_client().post('/marketing_activity/change_activity_begintime', data={"activityid": "410"})
        name = "testname"
        t = Category(name)
        db.session.add(t)
        db.session.commit()
        # json_dict = json.loads(json_data)
        print("ok")
        print(response)
        self.assertEqual('<Response streamed [302 FOUND]>','{}'.format(response))
        # self.assertEqual(json_dict['errcode'], -1, '状态码返回错误')



        # assert b'<Response streamed [200 OK]>' == '{}'.format(expected)



# params = [
#     (2, 3, 5),
#     (4, 5, 9),
#     (6, 7, 12)
# ]
#



#
# @pytest.fixture(scope="module")
# def test_01_BORROWER_INFO():
#     print("guess it")
#
#
# @pytest.fixture(params=[1, 2, 3])
# def test_data(request):
#     return request.param
#
#
# def test_not_2(test_data):
#     assert test_data != 2
#
#
# @pytest.mark.parametrize('a, b, expected', params)
# def test_01_BORROWER_INFO():
#     print("guess it")