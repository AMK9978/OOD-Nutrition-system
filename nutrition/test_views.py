import os
from unittest import TestCase

import grpc
import requests

import auth_pb2_grpc, auth_pb2


class TestAdminLogin(TestCase):
    def test_retrieve(self):

        channel = grpc.insecure_channel('localhost:50051')
        stub = auth_pb2_grpc.AuthStub(channel)
        stub.Login(auth_pb2.Credentials)
