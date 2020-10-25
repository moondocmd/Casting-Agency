import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from app import app
from models import setup_db, Movie, Actor

CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFZQmgyLWx0SHlZLUVzYXRXRGF3NSJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stMjAyMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ODVhMTI5YzUxMDYwMDZkZTE3NDI5IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYwMzU5ODg4NiwiZXhwIjoxNjAzNjg1Mjg2LCJhenAiOiJzVEpHNWlWTEE4dHg4bG9ldDc1SnJLWXBUQm1XVGV0WSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.UlkYDHvvSezNJD5Js2emWe7J8uuNvgseQlYal7Z_KCuqV4NTMPBVuFXm3EbgBtypEEqLCyPYqt2Ys8XMtURUeaiqtLj7xICw5v1zxIY_4Iz4wXIquFB9deov6hm9HTbxVGhnsDAfMhvSFLVeelQMmwQQpjU3urnPRQVqCLzyAVMXO30OvNtK8GlbBZRDK_7Lchx47Q52iPWMIvkePSRP6UVN-FMEAj2ypIwXlHy20HobGKa0QUd6guIbZAJRPmLY8xeum35eOvr7LE0Z7WYDwljq2YjqbFLMtIeMl5tWthDhVH6Vst2BNArGCHMjWd5cMAgkZi6GoM4-TrfpduxDdA'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFZQmgyLWx0SHlZLUVzYXRXRGF3NSJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stMjAyMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0NDg4ODFjNjQ3OGIwMDY3ZDgwZTEwIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYwMzU5NDM1NSwiZXhwIjoxNjAzNjgwNzU1LCJhenAiOiJzVEpHNWlWTEE4dHg4bG9ldDc1SnJLWXBUQm1XVGV0WSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.DLX30d3izUE2hPlMUOm1sdC2X5EXgGCyHY7a8848i1BAXBlqBo4VH8Ad5RasOmRY1XIAro-EEl7cp3lfJ0A18WaYICXGCsMxvCCnLJWe_FnoTddYed_VyEFiu0ISgLV8qATLldS3_gjoe8MuTUZSS-xyv56jMYq1WQjjN1vrYf_rWkgkit28UvLOs-w_IuTpHp1pVLJlF8o_EDZqdmtxCilo3kveYNnIjYIvA09fhHSEsam97Fy5kj6AcV_DjTuwn9R34OQBcCNhmQqCQekmhBKt1mAtW9ZhXJiWnGZFXWQS8-b8PIkfAMzAAnq6wdpWn2fFFS8-usUeYSdyv5XlmA'
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFZQmgyLWx0SHlZLUVzYXRXRGF3NSJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stMjAyMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY5NDc0OTllN2JmNTUwMDZmZGZhNmE2IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYwMzU5OTAxMiwiZXhwIjoxNjAzNjg1NDEyLCJhenAiOiJzVEpHNWlWTEE4dHg4bG9ldDc1SnJLWXBUQm1XVGV0WSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.VqKVz_vXw9sBpf7mJk1hs_xwHmYXWtfjWOcrXvuVPZOadJrTswebuZ-H5CmN-dhs83j0JyYAeY_JIsUSmZobYy9RM4q-7k5DJfmWw9gM3FBe5R9ivk-VXUCJA5gP1adM9JRnScubn4QNzyzERbygP6or4CGROGPXBq6eV1WMuY-5KIu3xHYvbYTLNrLrKfaRopuhjioSqd12GQltM26i5vTY5ycDvRM4DTNTs24nMeOfoVy9yehoVFwhCjlni3P3XPNTaGTFURdJpYqR1Nap7KITos1ncxsk1ctP_ziikNYx22ISKxlLdBHO4zM9phFV1-u6i0T8EgYX5_7oetp0vA'


def get_headers(token):
    return {'Authorization': f'Bearer {token}'}

class CastingTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.app = app
        self.client = self.app.test_client
        self.database_name = "test_casting_agency"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','pass', 'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        self.new_actor = {
            'fname': 'Jason',
            'lname': 'Johnson',
            'age': 55,
            'gender': 'male'
        }

        self.new_movie = {
            'id': '7000',
            'title': 'Blues Brothers', 
            'release': '10/01/1990'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Test Cases for 
    GET
    /actors and movies
    /actors/id and movies/id
    """

    def test_get_movies(self):
        response = app.test_client(self).get('/movies', headers=get_headers(CASTING_ASSISTANT))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        print ("running movies test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_actors(self):
        response = app.test_client(self).get('/actors', headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(response.data)
        print ("running actors test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    
    def test_fail_get_actors(self):
        res = app.test_client(self).get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertEqual(data['success'], False)

    def test_fail_get_movies(self):
        res = app.test_client(self).get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')
        self.assertEqual(data['success'], False)

    """
    Test Cases for 
    POST
    /actors and movies
    """
    def test_create_actors(self):
        res = app.test_client(self).post('/actors', 
            headers=get_headers(CASTING_DIRECTOR), json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movies(self):
        res = app.test_client(self).post('/movies', 
            headers=get_headers(EXECUTIVE_PRODUCER), json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # RBAC test, only executive producer can create movies
    def test_fail_create_movies(self):
        res = app.test_client(self).post('/movies', 
            headers=get_headers(CASTING_DIRECTOR), json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_create_actors(self):
        res = app.test_client(self).post('/actors', 
            headers=get_headers(CASTING_DIRECTOR), json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # RBAC test, Casting Assistant cannot add actors
    def test_fail_create_actors(self):
        res = app.test_client(self).post('/actors', 
            headers=get_headers(CASTING_ASSISTANT), json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    """
    Test Cases for 
    PATCH
    /actors and movies
    """
    def test_patch_movie(self):
        res = app.test_client(self).patch('/movies/1',
            json={
                'title' : 'Blues Brothers 2000',
                'release' : '1/2/2000'
                }, 
                headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #RBAC Test, assistant should not be able to update
    def test_patch_fail_movie(self):
        res = app.test_client(self).patch('/movies/1',
            json={
                'title' : 'Blues Brothers 2020',
                'release' : '1/2/2020'
                }, 
                headers=get_headers(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_patch_actor(self):
        res = app.test_client(self).patch('/actors/1',
            json={
                'fname' : 'Jassssooon',
                }, 
                headers=get_headers(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Test Failure - send payload without header
    def test_patch_fail_actor(self):
        res = app.test_client(self).patch('/actors/1',
            json={'fname' : 'Test'})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


    """
    Test Cases for 
    DELETE
    /actors and movies
    """
    def test_delete_movie(self): 
        res = app.test_client(self).delete('/movies/1', headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_delete_fail_movie(self): 
        res = app.test_client(self).delete('/movies/1111111', headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_actor(self): 
        res = app.test_client(self).delete('/actors/2', headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    def test_delete_fail_actor(self): 
        res = app.test_client(self).delete('/actors/1111111', headers=get_headers(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable') 

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()