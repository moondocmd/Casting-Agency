import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Movie, Actor

CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFZQmgyLWx0SHlZLUVzYXRXRGF3NSJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stMjAyMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0NDg4ODFjNjQ3OGIwMDY3ZDgwZTEwIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYwMzU2OTk4MiwiZXhwIjoxNjAzNTc3MTgyLCJhenAiOiJzVEpHNWlWTEE4dHg4bG9ldDc1SnJLWXBUQm1XVGV0WSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.BmBWrfMO6k8E3QP6Dhx5e3iuqNFVjgjkZmnIWxa1vBOwTbQU-zp6RoAzn1JLvru90QqNfbHyQmyhJmOk2OQX8WZRGZgOhdBc5BdOnCJ4HRHx65ODVMTUaIWhtILCHto-LNqxwvGO7xUXrXZCl7f6kYdS8dO5cEbnNCMLMBVLOQOzmTxXuDSr7-5TDe_r-zmI7j-2oPTbGnQYZUfEZrM97BDMP2KvNLYgA4JrKgVlgvJT6nVQSXSHEetBJbcAfQVHz4BNJ4cETlqP-AgCBHICQ8Pap4myvRaDnTEgX_lMqrrnilpDl_fCxMKipigFw-gmHKIN5A_GSEVjhuAJLUEOJQ'

def get_headers(token):
    print("GETTING A HEADER")
    return {'Authorization': f'Bearer {token}'}

class FlaskTestCase(unittest.TestCase):

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_movies(self):
        tester = app.test_client(self)
        response = tester.get('/movies', headers=get_headers(CASTING_DIRECTOR))
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_actors(self):
        tester = app.test_client(self)
        print(get_headers(CASTING_DIRECTOR))
        response = tester.get('/actors', headers=get_headers(CASTING_DIRECTOR))
        print(response)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()