# UT Tyler API tests

import unittest
from mysecret import USERNAME, PASSWORD
from ut_api import app
import json

class UTTylerAPITests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_grades(self):
        r = self.app.post('/1.0/grades', data={
            "username":USERNAME,
            "password":PASSWORD
        })
        self.assertEqual(200, r.status_code)

        grades = json.loads(r.data)
        self.assertIsNotNone(grades, "grades key not in JSON response")

        g = grades['grades']
        self.assertTrue(len(g) > 0, "no grades were found")

        course = g[0]
        self.assertEqual(len(course), 2, "invalid course grades structure")

        courseName, courseGrades = course
        self.assertIs(type(courseName), unicode)
        self.assertIs(type(courseGrades), list)

        grade = courseGrades[0]
        gradeKeys = set(['grade', 'date', 'timestamp', 'title'])

        self.assertEqual(gradeKeys, set(grade.keys()), "grade dict keys incorrect")



if __name__ == "__main__":
    unittest.main(verbosity=2)
