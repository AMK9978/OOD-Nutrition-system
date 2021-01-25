from unittest import TestCase

import grpc
import requests
from rest_framework.test import APIClient

import auth_pb2
import auth_pb2_grpc


class TestAdminLogin(TestCase):
    def test_retrieve(self):
        channel = grpc.insecure_channel('localhost:50051')
        stub = auth_pb2_grpc.AuthStub(channel)
        stub.Login(auth_pb2.Credentials)


class TestFoodViewSet(TestCase):
    def test_list(self):
        import os
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", __file__)
        import django
        django.setup()

        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NutritionSystem.settings")
        client = APIClient()
        client.credentials(
            HTTP_AUTHORIZATION='Token ' + "eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTE2MTg2NzcsInVzZXJfaWQiOjIsInVzZXJuYW1lIjoibmV3X3VzZXIiLCJyb2xlIjowLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwiZW1haWwiOiIifQ.AV1UVEcmkb__bgbp8pvTuSPvhhOkANOD_26Q1KHbbiuCDWAGwzBoHAxi2WfH_gsfkLFwKFtPVw7kfbv-dFrLyh2bAVZxQqOLo-JWI0RzNLKciF8c1Qs5EoM-0fJFF6f-MbXH2i9js6346PpSLk6nhSLYbV73Pn_sEyLAdaFmR2zjMUxC")
        response = client.get('/food-list/', {'title': 'new idea'}, format='json')
        self.assertEqual(response.status_code, 200)


class TestCharge(TestCase):
    def test_retrieve(self):
        self.assertEqual(2, 2)


from django.test import TestCase


class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        url = "http://localhost:8000/api/food/"

        payload = "{\n    \"name\": \"Abb\",\n    \"price\": 1,\n     \"meal\": \"dinner\",\n     \"capacity\": 1000,\n     \"pub_date\": \"2021-1-29\"\n}"
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTE2NjAxMjcsInVzZXJfaWQiOjIsInVzZXJuYW1lIjoibmV3X3VzZXIiLCJyb2xlIjowLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwiZW1haWwiOiIifQ.AGBtQUY1Zcz7Jb6yKdJppkHXP7g71vyV3xo7XbEJ9r471vaBqo7qdbnKrWbXs4qnq7eB0PLnGfUMhBjQoifm6Id6AC4IeVOfbw_VB8o4JceTYQmWuDDz_PJuQ2tLUqJgcyGFHrTEWLCv2bYEn4jh3EuP7AnRwK4i0JzOlWY_qX9Ueeai',
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
        print(response)
        self.assertEquals(response.status_code, 200)


class TestLogin(TestCase):
    def test_retrieve(self):
        self.assertEquals(2,2)
