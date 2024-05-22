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

    def test_getevent_by_id(self):
        response = self.app.get("/events/21")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("PSU" in response.data.decode())

if __name__ == "__main__":
    unittest.main()