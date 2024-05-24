import unittest
import warnings
from api import app

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

###UPDATE

###DELETE   
    
    

if __name__ == "__main__":
    unittest.main()