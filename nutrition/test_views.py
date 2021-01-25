import os
from unittest import TestCase

import requests


class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        url = "http://localhost:8000/api/food/"
        payload=''
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTE2NjAxMjcsInVzZXJfaWQiOjIsInVzZXJuYW1lIjoibmV3X3VzZXIiLCJyb2xlIjowLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwiZW1haWwiOiIifQ.AGBtQUY1Zcz7Jb6yKdJppkHXP7g71vyV3xo7XbEJ9r471vaBqo7qdbnKrWbXs4qnq7eB0PLnGfUMhBjQoifm6Id6AC4IeVOfbw_VB8o4JceTYQmWuDDz_PJuQ2tLUqJgcyGFHrTEWLCv2bYEn4jh3EuP7AnRwK4i0JzOlWY_qX9Ueeai',
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)



class TestFoodReserveViewSet(TestCase):

    def test_perform_create_ok(self):
        url = "http://localhost:8000/api/food-reserve/"

        payload = "{\n    \"food_id\": \"1\",\n    \"user_id\": \"1\",\n}"
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTE2NjAxMjcsInVzZXJfaWQiOjIsInVzZXJuYW1lIjoibmV3X3VzZXIiLCJyb2xlIjowLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwiZW1haWwiOiIifQ.AGBtQUY1Zcz7Jb6yKdJppkHXP7g71vyV3xo7XbEJ9r471vaBqo7qdbnKrWbXs4qnq7eB0PLnGfUMhBjQoifm6Id6AC4IeVOfbw_VB8o4JceTYQmWuDDz_PJuQ2tLUqJgcyGFHrTEWLCv2bYEn4jh3EuP7AnRwK4i0JzOlWY_qX9Ueeai',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)


    def test_perform_create_no_userid(self):
        url = "http://localhost:8000/api/food-reserve/"

        payload = "{\n    \"food_id\": 1,\n}"
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTE2NjAxMjcsInVzZXJfaWQiOjIsInVzZXJuYW1lIjoibmV3X3VzZXIiLCJyb2xlIjowLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwiZW1haWwiOiIifQ.AGBtQUY1Zcz7Jb6yKdJppkHXP7g71vyV3xo7XbEJ9r471vaBqo7qdbnKrWbXs4qnq7eB0PLnGfUMhBjQoifm6Id6AC4IeVOfbw_VB8o4JceTYQmWuDDz_PJuQ2tLUqJgcyGFHrTEWLCv2bYEn4jh3EuP7AnRwK4i0JzOlWY_qX9Ueeai',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertNotEqual(response.status_code, 200)

    def test_perform_create_no_userid_no_foodid(self):
        url = "http://localhost:8000/api/food-reserve/"

        payload = ""
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTE2NjAxMjcsInVzZXJfaWQiOjIsInVzZXJuYW1lIjoibmV3X3VzZXIiLCJyb2xlIjowLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwiZW1haWwiOiIifQ.AGBtQUY1Zcz7Jb6yKdJppkHXP7g71vyV3xo7XbEJ9r471vaBqo7qdbnKrWbXs4qnq7eB0PLnGfUMhBjQoifm6Id6AC4IeVOfbw_VB8o4JceTYQmWuDDz_PJuQ2tLUqJgcyGFHrTEWLCv2bYEn4jh3EuP7AnRwK4i0JzOlWY_qX9Ueeai',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertNotEqual(response.status_code, 200)

    def test_perform_create_wrong_token(self):
        url = "http://localhost:8000/api/food-reserve/"

        payload = "{\n    \"user_id\": \"3\",\n    \"food_id\": 1,\n}"
        headers = {
            'Authorization': 'im the king of this city',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertNotEqual(response.status_code, 200)

    def test_perform_create_food_id_string(self):
        url = "http://localhost:8000/api/food-reserve/"

        payload = "{\n    \"user_id\": \"3\",\n    \"food_id\": abgusht,\n}"
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTE2NjAxMjcsInVzZXJfaWQiOjIsInVzZXJuYW1lIjoibmV3X3VzZXIiLCJyb2xlIjowLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwiZW1haWwiOiIifQ.AGBtQUY1Zcz7Jb6yKdJppkHXP7g71vyV3xo7XbEJ9r471vaBqo7qdbnKrWbXs4qnq7eB0PLnGfUMhBjQoifm6Id6AC4IeVOfbw_VB8o4JceTYQmWuDDz_PJuQ2tLUqJgcyGFHrTEWLCv2bYEn4jh3EuP7AnRwK4i0JzOlWY_qX9Ueeai',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertNotEqual(response.status_code, 200)


class TestLogin(TestCase):
    def test_retrieve_user_exist(self):
        url = "http://localhost:8000/api/login/"

        payload = "{\n    \"username\": \"new_user\",\n    \"password\": \"1234\",\n}"
        headers = {

            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)



    def test_retrieve_user_does_not_exist(self):
        url = "http://localhost:8000/api/login/"

        payload = "{\n    \"username\": \"u2\",\n    \"password\": 123,\n}"
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertNotEqual(response.status_code, 200)


class TestAdminLogin(TestCase):
    def test_retrieve_admin_exist(self):
        url = "http://localhost:9090/api/login/"

        payload = "{\n    \"username\": \"amk\",\n    \"password\": pbkdf2_sha256$216000$enx34qYnqQv7$59zQR7P7KCXGWY4Q5CiD2LJW8Wa8xsAzYlMy52oOzHU=,\n}"
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_admin__admin_not_exist(self):
        url = "http://localhost:9090/api/login/"

        payload = "{\n    \"username\": \"admin2\",\n    \"password\": admin,\n}"
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertNotEqual(response.status_code, 200)


class TestCharge(TestCase):
    def test_retrieve(self):
        url = "http://localhost:8000/api/charge/"

        payload = 'charge=1200000'
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTE2NjAxMjcsInVzZXJfaWQiOjIsInVzZXJuYW1lIjoibmV3X3VzZXIiLCJyb2xlIjowLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwiZW1haWwiOiIifQ.AGBtQUY1Zcz7Jb6yKdJppkHXP7g71vyV3xo7XbEJ9r471vaBqo7qdbnKrWbXs4qnq7eB0PLnGfUMhBjQoifm6Id6AC4IeVOfbw_VB8o4JceTYQmWuDDz_PJuQ2tLUqJgcyGFHrTEWLCv2bYEn4jh3EuP7AnRwK4i0JzOlWY_qX9Ueeai',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_retrieve_price_string(self):
        url = "http://localhost:8000/api/charge/"

        payload = 'charge=ziad'
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTE2NjAxMjcsInVzZXJfaWQiOjIsInVzZXJuYW1lIjoibmV3X3VzZXIiLCJyb2xlIjowLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwiZW1haWwiOiIifQ.AGBtQUY1Zcz7Jb6yKdJppkHXP7g71vyV3xo7XbEJ9r471vaBqo7qdbnKrWbXs4qnq7eB0PLnGfUMhBjQoifm6Id6AC4IeVOfbw_VB8o4JceTYQmWuDDz_PJuQ2tLUqJgcyGFHrTEWLCv2bYEn4jh3EuP7AnRwK4i0JzOlWY_qX9Ueeai',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertNotEqual(response.status_code, 200)

    def test_retrieve_price_large_number(self):
        url = "http://localhost:8000/api/charge/"

        payload = 'charge=9999999999999'
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTE2NjAxMjcsInVzZXJfaWQiOjIsInVzZXJuYW1lIjoibmV3X3VzZXIiLCJyb2xlIjowLCJmaXJzdF9uYW1lIjoiIiwibGFzdF9uYW1lIjoiIiwiZW1haWwiOiIifQ.AGBtQUY1Zcz7Jb6yKdJppkHXP7g71vyV3xo7XbEJ9r471vaBqo7qdbnKrWbXs4qnq7eB0PLnGfUMhBjQoifm6Id6AC4IeVOfbw_VB8o4JceTYQmWuDDz_PJuQ2tLUqJgcyGFHrTEWLCv2bYEn4jh3EuP7AnRwK4i0JzOlWY_qX9Ueeai',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertNotEqual(response.status_code, 200)



    def test_retrieve_price_no_auth_token(self):
        url = "http://localhost:8000/api/charge/"

        payload = 'charge=120000'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertNotEqual(response.status_code, 200)

    def test_retrieve_price_wrong_authorized(self):
        url = "http://localhost:8000/api/charge/"

        payload = 'charge=120000'
        headers = {
            'Authorization': 'this is token',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertNotEqual(response.status_code, 200)
