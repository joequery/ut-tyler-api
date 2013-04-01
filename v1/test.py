# UT Tyler API tests

import unittest
import scrape

class UTTylerAPITests(unittest.TestCase):
    def test_parse_announcement_html(self):
        f = open("testfiles/announcements.html")
        announcementHTML = f.read()
        f.close()

        expectedAnnouncements = [
            {
                'date': 'Friday, March 29, 2013', 
                'timestamp': 1364533200, 
                'course': 'MATH 3336.001', 
                'details': None, 
                'title': 'Homework #11 is posted'
            }, 
            {
                'date': 'Thursday, March 21, 2013', 
                'timestamp': 1363842000, 
                'course': 'MATH 3336.001', 
                'details': 'Homework #10 has been posted.', 
                'title': 'Homework #10 is posted'
            }
        ]
        announcements = scrape.parse_announcement_html(announcementHTML)
        self.assertEqual(expectedAnnouncements, announcements)

    def test_parse_grades_html(self):
        f = open("testfiles/grades.html")
        gradesHTML = f.read()
        f.close()

        grades = scrape.parse_grades_html(gradesHTML)
        expectedGrades = [
            {
                'grade': '69.00 /70', 
                'date': 'Mar 18, 2013 11:28 AM', 
                'timestamp': 1363624080, 
                'title': 'Assignment #2'
            }, 
            {
                'grade': '90.00 /100', 
                'date': 'Mar 2, 2013 3:29 PM', 
                'timestamp': 1362259740, 
                'title': 'Exam I'
            }, 
            {
                'grade': '70.00 /70', 
                'date': 'Feb 20, 2013 10:20 AM', 
                'timestamp': 1361377200, 
                'title': 'Assignment #1'
            }
        ]
        self.assertEqual(expectedGrades, grades)



if __name__ == "__main__":
    unittest.main(verbosity=2)
