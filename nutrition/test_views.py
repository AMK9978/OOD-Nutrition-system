from unittest import TestCase

import grpc
from django.test import Client
from django.urls import reverse

import auth_pb2
import auth_pb2_grpc
from rest_framework.test import APIClient


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
        self.assertEqual(2,2)
