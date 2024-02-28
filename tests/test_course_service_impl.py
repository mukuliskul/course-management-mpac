import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.course_service_impl import CourseServiceImpl, Course

class CourseServiceTests(unittest.TestCase):
    def setUp(self):
        self.course_service = CourseServiceImpl()

    def test_get_courses_empty(self):
        with self.assertRaises(LookupError):
            self.course_service.get_courses()
                
    def test_get_courses_existing(self):  
        course1 = Course("Course1", 0)
        course2 = Course("Course2", 1)
        self.course_service.courses[0] = course1
        self.course_service.courses[1] = course2

        expected_courses = [course1, course2]
        actual_courses = self.course_service.get_courses()
        self.assertEqual(expected_courses, actual_courses, "The list of courses should match the expected output.")
        
    def test_get_course_by_id_non_existing(self):
        self.course_service.create_course("Course1") # id = 0 (auto-generated)
        self.course_service.create_course("Course2") # id = 1 (auto-generated)
        self.course_service.create_course("Course3") # id = 2 (auto-generated)
        with self.assertRaises(KeyError):
            self.course_service.get_course_by_id(99)
                
    def test_get_course_by_id_existing(self):  
        course4 = Course("Course4", 3)
        self.course_service.courses[3] = course4
        expected_courses = course4
        actual_courses = self.course_service.get_course_by_id(3)
        self.assertEqual(expected_courses, actual_courses, "The course should match the expected output.")

    def test_create_course(self):
        course_name = "New Course"
        course_id = 0
        self.course_service.create_course(course_name)
        self.assertTrue(any(course_id == c_id for c_id in self.course_service.courses.keys()), "New course should be created and found in courses list.")

    def test_delete_course_non_existing(self):
        with self.assertRaises(KeyError):
            self.course_service.delete_course(99)
            
    def test_delete_course_existing(self):
        course_id = 0
        self.course_service.create_course("Test Course")
        self.assertTrue(course_id in self.course_service.courses)
        self.course_service.delete_course(course_id)
        self.assertFalse(course_id in self.course_service.courses, "Course should be deleted.")

    def test_create_assignment(self):
        course_id = 0
        assignment_name = "Test Assignment"
        self.course_service.create_course("Test Course")
        self.course_service.create_assignment(course_id, assignment_name)
        course = self.course_service.get_course_by_id(course_id)
        self.assertTrue(any(assignment.name == assignment_name for assignment in course.assignments.values()), "Assignment should be created in the course.")

    def test_create_assignment_non_existing_course(self):
        course_id = 0
        assignment_name = "Test Assignment"
        with self.assertRaises(KeyError):
            self.course_service.create_assignment(99, assignment_name)
            
    def test_enroll_student(self):
        course_id = 0
        student_id = 1
        self.course_service.create_course("Test Course")
        self.course_service.enroll_student(course_id, student_id)
        course = self.course_service.get_course_by_id(course_id)
        self.assertTrue(any(s_id == student_id for s_id in course.students_enrolled.keys()), "Student should be enrolled in the course")
    
    def test_enroll_student_non_existing_course(self):
        student_id = 1
        with self.assertRaises(KeyError):
            self.course_service.enroll_student(99, student_id)
    
    def test_enroll_student_existing_student(self):
        course_id = 0
        student_id = 1
        self.course_service.create_course("Test Course")
        self.course_service.enroll_student(course_id, student_id)
        with self.assertRaises(ValueError):
            self.course_service.enroll_student(course_id, student_id)
        
    def test_dropout_student_non_existing(self):
        course_id = 0
        self.course_service.create_course("Test Course")
        with self.assertRaises(KeyError):
            self.course_service.dropout_student(0, 99)
            
    def test_dropout_student_non_existing_course(self):
        student_id = 0
        self.course_service.create_course("Test Course")
        with self.assertRaises(KeyError):
            self.course_service.dropout_student(99, student_id)
        
    def test_dropout_student(self):
        course_id = 0
        student_id = 1
        self.course_service.create_course("Test Course")
        self.course_service.enroll_student(course_id, student_id)
        self.course_service.dropout_student(course_id, student_id)
        course = self.course_service.get_course_by_id(course_id) 
        self.assertFalse(any(s_id == student_id for s_id in course.students_enrolled.keys()), "Student should be dropped from the course")
    
    def test_submit_assignment(self):
        course_id = 0
        assignment_id = 0
        student_id = 1
        grade = 100
        self.course_service.create_course("Test Course")
        self.course_service.create_assignment(course_id, "Test Assignment")
        self.course_service.enroll_student(course_id, student_id)
        self.course_service.submit_assignment(course_id, student_id, assignment_id, grade)
        course = self.course_service.get_course_by_id(course_id)
        actual_grade = course.grades.get((student_id, assignment_id))
        self.assertIsNotNone(actual_grade, "Grade should be submitted.")
        self.assertEqual(grade, actual_grade, "Submitted grade should match the expected")

    def test_submit_assignment_non_existing_course(self):
        assignment_id = 0
        student_id = 1
        with self.assertRaises(KeyError):
            self.course_service.submit_assignment(99, student_id, assignment_id, 100)
    
    def test_submit_assignment_out_of_range_grade(self):
        course_id = 0
        assignment_id = 0
        student_id = 1
        self.course_service.create_course("Test Course")
        self.course_service.create_assignment(course_id, "Test Assignment")
        self.course_service.enroll_student(course_id, student_id)
        with self.assertRaises(ValueError):
            self.course_service.submit_assignment(course_id, student_id, assignment_id, 101)
        with self.assertRaises(ValueError):
            self.course_service.submit_assignment(course_id, student_id, assignment_id, -1)
    
    def test_submit_assignment_non_existing_student(self):
        course_id = 0
        assignment_id = 0
        self.course_service.create_course("Test Course")
        self.course_service.create_assignment(course_id, "Test Assignment")
        with self.assertRaises(KeyError):
            self.course_service.submit_assignment(course_id, 99, assignment_id, 100)
    
    def test_submit_assignment_non_existing_assignment(self):
        course_id = 0
        student_id = 1
        self.course_service.create_course("Test Course")
        self.course_service.enroll_student(course_id, student_id)
        with self.assertRaises(KeyError):
            self.course_service.submit_assignment(course_id, student_id, 99, 100)
    
    def test_submit_assignment_existing_assignment(self):
        course_id = 0
        assignment_id = 0
        student_id = 1
        grade = 100
        self.course_service.create_course("Test Course")
        self.course_service.create_assignment(course_id, "Test Assignment")
        self.course_service.enroll_student(course_id, student_id)
        self.course_service.submit_assignment(course_id, student_id, assignment_id, grade)
        with self.assertRaises(ValueError):
            self.course_service.submit_assignment(course_id, student_id, assignment_id, grade)
        
    def test_get_assignment_grade_avg(self):
        course_id = 0
        assignment_id = 0
        student_ids = [1,2,3,4,5]
        grades = [10, 20, 30, 40, 50]
        expected_average = 30 # total of grades / total of students
        self.course_service.create_course("Test Course")
        self.course_service.create_assignment(course_id, "Test Assignment")
        for i in range(len(student_ids)):
            self.course_service.enroll_student(course_id, student_ids[i]) # enrolling 5 students
            self.course_service.submit_assignment(course_id, student_ids[i], assignment_id, grades[i]) # submitting 1 assignment each
        actual_assignment_average = self.course_service.get_assignment_grade_avg(course_id, assignment_id)
        self.assertEqual(actual_assignment_average, expected_average, f"Average for Assignment should match the expected (f{expected_average})")
        
    def test_get_assignment_grade_avg_float_grades(self):
        course_id = 0
        assignment_id = 0
        student_ids = [1,2,3,4,5]
        grades = [10.2, 20.5, 30.3, 40.9, 50.1]
        expected_average = 30 # total of grades / total of students = 30.4 but should get floor'd to 30
        self.course_service.create_course("Test Course")
        self.course_service.create_assignment(course_id, "Test Assignment")
        for i in range(len(student_ids)):
            self.course_service.enroll_student(course_id, student_ids[i]) # enrolling 5 students
            self.course_service.submit_assignment(course_id, student_ids[i], assignment_id, grades[i]) # submitting 1 assignment each
        actual_assignment_average = self.course_service.get_assignment_grade_avg(course_id, assignment_id)
        self.assertEqual(actual_assignment_average, expected_average, f"Average for Assignment should match the expected (f{expected_average})")
        
    def test_get_assignment_grade_avg_non_existing_course(self):
        assignment_id = 0
        with self.assertRaises(KeyError):
            self.course_service.get_assignment_grade_avg(99, assignment_id)
        
    def test_get_assignment_grade_avg_non_existing_assignment(self):
        course_id = 0
        self.course_service.create_course("Test Course")
        with self.assertRaises(KeyError):
            self.course_service.get_assignment_grade_avg(course_id, 99)
    
    def test_get_student_grade_avg(self):
        course_id = 0
        assignment_ids = [0, 1, 2, 3, 4] 
        student_id = 1
        grades = [10, 20, 30, 40, 50]
        expected_average = 30 # total of grades / total of assignments
        self.course_service.create_course("Test Course")
        self.course_service.enroll_student(course_id, student_id)
        for i in range(len(assignment_ids)):
            self.course_service.create_assignment(course_id, assignment_ids[i]) # creating 5 assignments
            self.course_service.submit_assignment(course_id, student_id, assignment_ids[i], grades[i]) # submitting 1 assignment each
        actual_assignment_average = self.course_service.get_student_grade_avg(course_id, student_id)
        self.assertEqual(actual_assignment_average, expected_average, f"Average for Student should match the expected (f{expected_average})")
        
    def test_get_student_grade_avg_float_grades(self):
        course_id = 0
        assignment_ids = [0, 1, 2, 3, 4] 
        student_id = 1
        grades = [10.2, 20.5, 30.3, 40.9, 50.1]
        expected_average = 30 # total of grades / total of assignments = 30.4 but should get floor'd to 30
        self.course_service.create_course("Test Course")
        self.course_service.enroll_student(course_id, student_id)
        for i in range(len(assignment_ids)):
            self.course_service.create_assignment(course_id, assignment_ids[i]) # creating 5 assignments
            self.course_service.submit_assignment(course_id, student_id, assignment_ids[i], grades[i]) # submitting 1 assignment each
        actual_assignment_average = self.course_service.get_student_grade_avg(course_id, student_id)
        self.assertEqual(actual_assignment_average, expected_average, f"Average for Student should match the expected (f{expected_average})")
                
    def test_get_student_grade_avg_non_existing_course(self):
        student_id = 0
        with self.assertRaises(KeyError):
            self.course_service.get_student_grade_avg(99, student_id)
    
    def test_get_student_grade_avg_non_existing_student(self):
        course_id = 0
        self.course_service.create_course("Test Course")
        with self.assertRaises(KeyError):
            self.course_service.get_student_grade_avg(course_id, 99)
                
    def test_get_top_five_students(self):
        course_id = 0
        assignment_ids = [0, 1, 2, 3, 4, 5, 6] 
        # student_id : [grades over 7 assignments]
        
        student_grades = {
            1 : [100, 100, 100, 100, 100, 100, 100], # Total : 700
            2 : [10, 10, 10, 10, 10, 10, 10], # Total : 70
            3 : [10, 20, 30, 40, 50, 60, 70], # Total : 280
            4 : [90, 90, 90, 90, 90, 90, 90], # Total : 630 
            5 : [50, 50, 50, 50, 50, 50, 50], # Total : 350 
            6 : [40, 50, 60, 70, 80, 90, 100], # Total : 490 
            7 : [100, 90, 100, 90, 80, 60, 60] # Total : 580 
        }

        expected_top_five = [1, 4, 7, 6, 5]  # based on total grades in student_grades
        self.course_service.create_course("Test Course")

        for assignment_id in range(len(assignment_ids)):  # Assuming assignment_id is just an integer starting from 0
            self.course_service.create_assignment(course_id, f"Assignment{assignment_id}")
            
        for student_id, grades in student_grades.items():
            self.course_service.enroll_student(course_id, student_id)
            for assignment_id, grade in enumerate(grades):
                self.course_service.submit_assignment(course_id, student_id, assignment_id, grade)

        top_five_students = self.course_service.get_top_five_students(course_id)
        top_five_students_id = []
        
        for student in top_five_students:
            top_five_students_id.append(student.id)

        self.assertEqual(top_five_students_id, expected_top_five, f"Top five students should match the expected list ({expected_top_five}")
                
    def test_get_top_five_students_not_enough_students(self):
        course_id = 0
        assignment_ids = [0, 1, 2, 3] 
        
        # only 4 students (less than the expected minimum of 5)
        # student_id : [grades over 4 assignments]
        student_grades = {
            1 : [100, 100, 100, 100], # Total : 400
            2 : [10, 10, 10, 10], # Total : 40
            3 : [10, 20, 30, 40], # Total : 100
            4 : [90, 90, 90, 90], # Total : 360
        }
        
        expected_top_five = [1, 4, 3, 2]  # based on total grades in student_grades
        self.course_service.create_course("Test Course")

        for assignment_id in range(len(assignment_ids)):  # Assuming assignment_id is just an integer starting from 0
            self.course_service.create_assignment(course_id, f"Assignment{assignment_id}")
            
        for student_id, grades in student_grades.items():
            self.course_service.enroll_student(course_id, student_id)
            for assignment_id, grade in enumerate(grades):
                self.course_service.submit_assignment(course_id, student_id, assignment_id, grade)

        top_five_students = self.course_service.get_top_five_students(course_id)
        top_five_students_id = []
        
        for student in top_five_students:
            top_five_students_id.append(student.id)

        self.assertEqual(top_five_students_id, expected_top_five, f"Top five students should match the expected list ({expected_top_five}")
                
    def test_get_top_five_students_no_students(self):
        course_id = 0
        assignment_ids = [0, 1, 2, 3] 

        self.course_service.create_course("Test Course")

        for assignment_id in range(len(assignment_ids)):  # Assuming assignment_id is just an integer starting from 0
            self.course_service.create_assignment(course_id, f"Assignment{assignment_id}")
        
        with self.assertRaises(ValueError):
            self.course_service.get_top_five_students(course_id)
                
    def test_get_top_five_students_non_existing_course(self):
        with self.assertRaises(KeyError):
            self.course_service.get_top_five_students(99)

if __name__ == '__main__':
    unittest.main()