from typing import List
from app.course_service import CourseService

# using a manual id generator for simplicity rather than using uuid

class CourseServiceImpl(CourseService):
  def __init__(self):
    self.courses = {} # {course_id : course_object}
    self.id_generator = 0

  def get_courses(self):
    if self.courses:
      return [course.name for course in self.courses.values()]
    else:
      raise LookupError("No courses found")
  
  def get_course_by_id(self, course_id):
    if self.courses[course_id]:
      return self.courses[course_id].name
    else:
       raise KeyError(f"Course with ID {course_id} not found")
  
  def create_course(self, course_name):
    new_course = Course(course_name)
    self.courses[self.id_generator] = new_course
    self.id_generator+=1
  
  def delete_course(self, course_id):
    if self.courses[course_id]:
      self.courses.pop(course_id)
    else:
      raise KeyError(f"Course with ID {course_id} not found")

  def create_assignment(self, course_id, assignment_name):
    """
    Creates a new assignment for a course.
    """
    pass

  def enroll_student(self, course_id, student_id):
    """
    Enrolls a student in a course.
    """
    pass

  def dropout_student(self, course_id, student_id):
    """
    Drops a student from a course.
    """
    pass

  def submit_assignment(self, course_id, student_id, assignment_id, grade: int):
    """
    Submits an assignment for a student. A grade of an assignment will be an integer between 0 and 100 inclusive.
    """
    pass

  def get_assignment_grade_avg(self, course_id, assignment_id) -> int:
    """
    Returns the average grade for an assignment. Floors the result to the nearest integer.
    """
    pass

  def get_student_grade_avg(self, course_id, student_id) -> int:
    """
    Returns the average grade for a student in a course. Floors the result to the nearest integer.
    """
    pass

  def get_top_five_students(self, course_id) -> List[int]:
    """
    Returns the IDs of the top 5 students in a course based on their average grades of all assignments.
    """
    pass

class Course():
  def __init__(self, course_name):
    self.id = "course_id" #auto-generated
    self.name = course_name
    self.details = {"student-id" : "assignment-id"} #added by a setter  

class Student():
  def __init__(self, student_id, course_id, assignment_id):
    self.id = student_id
    self.course_ids = ["course_id"] #added by a setter
  
class Assignments():
  def __init__(self, assignment_id, assignment_name, assignment_grade):
    self.id = assignment_id
    self.name = assignment_name
    self.grade = ["assignment-grades"] 
