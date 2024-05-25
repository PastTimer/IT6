import unittest
import warnings
from api import app
from flask_testing import TestCase
from flask import Flask, jsonify
import json

class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        
        warnings.simplefilter("ignore", category=DeprecationWarning)
    
    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

###GET TESTS

    def test_getevent(self):
        response = self.app.get("/events")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Writing Short Story" in response.data.decode())
    
    def test_getHOBBY(self):
        response = self.app.get("/hobbies_and_pasttime")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Cooking" in response.data.decode())
    
    def test_getmembers(self):
        response = self.app.get("/members")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Francisco" in response.data.decode())
    
    def test_getmemberships(self):
        response = self.app.get("/memberships")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("131" in response.data.decode())
    
    def test_getorg(self):
        response = self.app.get("/organizations")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Poem Club" in response.data.decode())
        
###GET SPECIFIC

    def test_getevent_by_id(self):
        response = self.app.get("/events/21")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("PSU" in response.data.decode())
        
###GET FANCY

    def test_getHOBBYspec(self):
        response = self.app.get("/hobbies_and_pasttime/Baking/members")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Sheila" in response.data.decode())

###POST

    def test_add_hobby(self):
        data = {"hobby_code": "Go", "hobby_desc": "eeasy mode chess"}
        response = self.app.post('/hobbies_and_pasttime/add', data=json.dumps(data), headers = {'Content-Type':'application/json'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

    def test_add_member(self):
        data = {"first_name": "Dara", "last_name": "Raya", "address" : "PPC", "other_details" : ""}
        response = self.app.post('/hobbies_and_pasttime/add', data=json.dumps(data), headers = {'Content-Type':'application/json'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
    
    def test_add_organization(self):
        data = {"organization_id": "Robotics Club", "organization_details": "you robot"}
        response = self.app.post('/organizations/add', data=json.dumps(data), headers = {'Content-Type':'application/json'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
    
    def test_add_event(self):
        data = {"event_name": "Checkers", "event_description": "ala", "location" : "PPC", "other_details" : ""}
        response = self.app.post('/events/add', data=json.dumps(data), headers = {'Content-Type':'application/json'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
    
    def test_add_membership(self):
        data = {"level_of_ability": "8", "hobby_code": "Poem Writing", "member_id" : "21", "organisation_id" : "Poem Club"}
        response = self.app.post('/hobbies_and_pasttime/add', data=json.dumps(data), headers = {'Content-Type':'application/json'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
    
##PUT TEST

    def test_update_event(self):
        headers = self.headers_with_token()
        url = f'{self.base_url}/events/update/1'
        data = {
            "event_name": "Updated Event Name",
            "event_description": "Updated Event Description",
            "location": "Updated Location",
            "other_details": "Updated Details"
        }
        response = requests.put(url, json=data, headers=headers)
        self.assertEqual(response.status_code, 200)

##DEL TEST

    def test_delete_organization(self):
        headers = self.headers_with_token()
        url = f'{self.base_url}/organizations/del/1'
        response = requests.delete(url, headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()