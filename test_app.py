import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from app import app
from models import setup_db, Movie, Actor

CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFZQmgyLWx0SHlZLUVzYXRXRGF3NSJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stMjAyMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ODVhMTI5YzUxMDYwMDZkZTE3NDI5IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYwMzY1NzUxOSwiZXhwIjoxNjAzNzQzOTE5LCJhenAiOiJzVEpHNWlWTEE4dHg4bG9ldDc1SnJLWXBUQm1XVGV0WSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.V6vAI2VNJ2COutatvui7Rwj_kDLEW6Brpe5oLZI1sr71xuJTHaXaNnrQdvAKTHOp7eu05HMO1mQPYQTB9ZsNbrOAL4G7PwDuHIwLjkhP-2iItfnr0mruBxxlwVPL4Xzpo8P8vRuP_JRunTOV48nI-Vx3kw8zOF7JoEi-0PPg2-dWvmUxPX7F1ekznKeeUUgvFoZJzvbvkLEijU5G6GmM9Z1nd7NzZ2GUK4Oo6Ik2TlFHD122zWNxbCfk7HMuwhvB7DeZrtF_lf0MRsTP3vg0_wsNKU3Tf1eHjvE_ACpx8KXwGeoIxWK_05q7uKoBkXQgo1Vfd0tvGC8UHS_xzP2qBw'                    
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFZQmgyLWx0SHlZLUVzYXRXRGF3NSJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stMjAyMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0NDg4ODFjNjQ3OGIwMDY3ZDgwZTEwIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYwMzY1NzcxNiwiZXhwIjoxNjAzNzQ0MTE2LCJhenAiOiJzVEpHNWlWTEE4dHg4bG9ldDc1SnJLWXBUQm1XVGV0WSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.AjBvm6kfEWmPSTPvY8LqfzuuSjSpJzgB4bKPTGkUxA5Ju3sKDNHHgqPkzp3tT2Qfi2XSTk7w4HdNRMwODqN6lUc5GOx3O6KLabjVlNgDQU7BVlJb7y7BFK22UsLnrTfTaWrMZy9sPn_9UrWhDYoa6PAVfx00FAs2yEX9ubRHq11WxFyzfPb34Xdd4ePWbB7Ko_yDaGzlfuT6WK-HYORoymy297ErIBCPn7ihpjafRTQ4d4QblPNpfXcHJmXZka3vlJX_8Mt2pMJn6NbXvAgfoJcoIEIsGB900lOJpzUSyO_rcu8_qEX4fvjnaHqTFF6LMrPWllBP-CdModxK6BReQg'
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFZQmgyLWx0SHlZLUVzYXRXRGF3NSJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stMjAyMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY5NDc0OTllN2JmNTUwMDZmZGZhNmE2IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYwMzY1NzQ1NiwiZXhwIjoxNjAzNzQzODU2LCJhenAiOiJzVEpHNWlWTEE4dHg4bG9ldDc1SnJLWXBUQm1XVGV0WSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.hwL_DnUmSRMU-LSANZmiuI_yPQScFkJ7FCen0i8aKrtg1AYlq9mSvX8rBiiV-usycEe9RmnSb-0fKF41w9SISQkAIXwhK8Ex-ZkpYxFKv7I0ySU3LYAK3akZU7OXc0VMXUQi9g0TSyF5YwT_ICx1MlATLXM7x10NMLE3MGW5NId1dlFwhZGlXq90nZ5je1MQoqVgB7UChbus_JIHUdODS7QB5lVUGRYrP92IMLwKDR7Mv_EKegYanTBSSnPH9vwZF6TxZTucOy9po6KUlJUDcCXptAjaTVhEhg6Aw5k6kb6ZtI0eWnDGkscakb7Sa02apMAnzlsfd8d7mtbYleBMwA'


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
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'pass', 'localhost:5432', self.database_name
            )

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
        response = app.test_client(self).get(
            '/movies', headers=get_headers(CASTING_ASSISTANT)
            )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_actors(self):
        response = app.test_client(self).get(
            '/actors', headers=get_headers(CASTING_ASSISTANT)
            )
        data = json.loads(response.data)
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
        res = app.test_client(self).post(
            '/actors',
            headers=get_headers(CASTING_DIRECTOR), json=self.new_actor
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movies(self):
        res = app.test_client(self).post(
            '/movies',
            headers=get_headers(EXECUTIVE_PRODUCER), json=self.new_movie
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # RBAC test, only executive producer can create movies
    def test_fail_create_movies(self):
        res = app.test_client(self).post(
            '/movies',
            headers=get_headers(CASTING_DIRECTOR), json=self.new_movie
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_create_actors(self):
        res = app.test_client(self).post(
            '/actors',
            headers=get_headers(CASTING_DIRECTOR), json=self.new_actor
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # RBAC test, Casting Assistant cannot add actors
    def test_fail_create_actors(self):
        res = app.test_client(self).post(
            '/actors',
            headers=get_headers(CASTING_ASSISTANT), json=self.new_actor
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    """
    Test Cases for
    PATCH
    /actors and movies
    """
    def test_patch_movie(self):
        res = app.test_client(self).patch(
            '/movies/2',
            json={
                'title': 'Blues Brothers 2000',
                'release': '1/2/2000'
                }, headers=get_headers(CASTING_DIRECTOR)
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # RBAC Test, assistant should not be able to update
    def test_patch_fail_movie(self):
        res = app.test_client(self).patch(
            '/movies/1',
            json={
                'title': 'Blues Brothers 2020',
                'release': '1/2/2020'
                }, headers=get_headers(CASTING_ASSISTANT)
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_patch_actor(self):
        res = app.test_client(self).patch(
            '/actors/1',
            json={
                'fname': 'Jassssooon',
                }, headers=get_headers(CASTING_DIRECTOR)
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test Failure - send payload without header
    def test_patch_fail_actor(self):
        res = app.test_client(self).patch(
            '/actors/1',
            json={'fname': 'Test'}
            )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """
    Test Cases for
    DELETE
    /actors and movies
    """
    def test_delete_movie(self):
        res = app.test_client(self).delete(
            '/movies/2', headers=get_headers(EXECUTIVE_PRODUCER)
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    def test_delete_fail_movie(self):
        res = app.test_client(self).delete(
            '/movies/1111111', headers=get_headers(EXECUTIVE_PRODUCER)
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_actor(self):
        res = app.test_client(self).delete(
            '/actors/1', headers=get_headers(EXECUTIVE_PRODUCER)
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_delete_fail_actor(self):
        res = app.test_client(self).delete(
            '/actors/1111111', headers=get_headers(EXECUTIVE_PRODUCER)
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
