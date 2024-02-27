from typing import List
from app.course_service import CourseService

# using a manual id generator for simplicity and readability rather than using uuid
# dictionary operations are wrapped in try-catch block to override with custom exceptions

class CourseServiceImpl(CourseService):
  def __init__(self):
    self.courses = {} # {course_id : course_object}
    self.course_id = 0 # course id generator

  #TODO: SHOW ALL DETAILS ABOUT COURSE
  def get_courses(self):
    if self.courses:
      # returning course.name as the dictionary stores course object in value
      return [course.name for course in self.courses.values()] 
    else:
      raise LookupError("No courses found")
  
  #TODO: SHOW ALL DETAILS ABOUT COURSE
  def get_course_by_id(self, course_id):
    try:
      course = self.courses[course_id]
      return course
    except KeyError:
       raise KeyError(f"Course with ID {course_id} not found")
     
  #TODO : might remove this function
  def get_students_by_course_id(self, course_id):
    course = self.get_course_by_id(course_id)
    return [student.id for student in course.students_enrolled]
  
  def create_course(self, course_name):
    new_course = Course(course_name)
    self.courses[self.course_id] = new_course
    self.course_id+=1
  
  def delete_course(self, course_id):
    course = self.get_course_by_id(course_id)
    self.courses.pop(course_id)

  def create_assignment(self, course_id, assignment_name):
    course = self.get_course_by_id(course_id)
    course.create_course_assignment(assignment_name)

  def enroll_student(self, course_id, student_id):
    course = self.get_course_by_id(course_id)
    course.enroll_student_in_course(student_id)
    

  def dropout_student(self, course_id, student_id):
    course = self.get_course_by_id(course_id)
    course.drop_student_from_course(student_id, course_id) 
  
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
    self.name = course_name
    self.assignments = {} # {assignment_id : assignment_object}
    self.assignment_id = 0 # assignment id generator
    self.students_enrolled = []
    
  def create_course_assignment(self, assignment_name):
    new_assignment = Assignment(assignment_name)
    self.assignments[self.assignment_id] = new_assignment
    new_assignment += 1 
    
  def enroll_student_in_course(self, student_id):
    new_student = Student(student_id)
    self.students_enrolled.append(new_student)
    
  def drop_student_from_course(self, student_id, course_id):
    remove_student = None # student to be removed
    for student in self.students_enrolled:
      if student.id == student_id:
        remove_student = student
        break
    
    if(remove_student):
      self.students_enrolled.remove(remove_student)
    else:
      raise ValueError(f"Student id: {student_id} not found in Course: {self.name} (id:{course_id})")
    
class Assignment():
  def __init__(self, assignment_name, assignment_grade = None):
    self.name = assignment_name
    self.grade = ["assignment-grades"] 
    
class Student():
  def __init__(self, student_id):
    self.id = student_id
    #self.course_ids = ["course_id"] #added by a setter
  
