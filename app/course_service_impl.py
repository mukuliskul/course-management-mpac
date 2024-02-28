from typing import List
from app.course_service import CourseService

# using a manual id generator for simplicity and readability rather than using uuid
# dictionary operations are wrapped in try-catch block to override with custom exceptions
# re-submission are not allowed

#TODO: DEFINE ALL GETTERS AND SETTERS FOR CLASSES : COURSE, STUDENT, ASSIGNMENT
#TODO: ADD FINAL COMMENTS

class CourseServiceImpl(CourseService):
  def __init__(self):
    self.courses = {} # {course_id : course_object}
    self.course_id = 0 # course id generator

  #TODO: ADD GRADES
  def get_courses(self):
    if not self.courses:
        raise LookupError("No courses found")
    else:
      return [course for course in self.courses.values()]
  
  #TODO: SHOW ALL DETAILS ABOUT COURSE
  def get_course_by_id(self, course_id):
    try:
      course = self.courses[course_id]
      return course
    except KeyError:
       raise KeyError(f"Course with ID {course_id} not found")
  
  def create_course(self, course_name):
    new_course = Course(course_name, self.course_id)
    self.courses[self.course_id] = new_course
    self.course_id+=1
  
  def delete_course(self, course_id):
    course = self.get_course_by_id(course_id)
    self.courses.pop(course_id)

  def create_assignment(self, course_id, assignment_name):
    # creation of assignments with same name is permitted since id is always unique
    course = self.get_course_by_id(course_id)
    course.create_course_assignment(assignment_name)

  def enroll_student(self, course_id, student_id):
    course = self.get_course_by_id(course_id)
    course.enroll_student_in_course(student_id)
    
  def dropout_student(self, course_id, student_id):
    course = self.get_course_by_id(course_id)
    course.drop_student_from_course(student_id, course_id) 
  
  #TODO : check if assignment is not already submitted
  def submit_assignment(self, course_id, student_id, assignment_id, grade: int):
    if grade < 0 or grade > 100:
      raise ValueError("Grade must be between 0 and 100 inclusive.")

    course = self.get_course_by_id(course_id)
    student = course.get_student_by_id(student_id)
    assignment = course.get_assignment_by_id(assignment_id)   
    
    # ensuring there are no re-submissions
    existing_grade = course.grades.get((student_id, assignment_id))
    if existing_grade is not None:
        raise ValueError(f"Student ID: {student_id} has already submitted {course.assignments[assignment_id].name} (id:{assignment_id}) in Course: {course.name} (id:{course_id})")

    course.grades[(student.id, assignment.id)] = grade

  def get_assignment_grade_avg(self, course_id, assignment_id) -> int:
    course = self.get_course_by_id(course_id)
    assignment = course.get_assignment_by_id(assignment_id) # to ensure assignment exists
    total_grade, total_count = 0, 0
    
    for (s_id, a_id), grade in course.grades.items():
      if a_id == assignment.id:
        total_grade += grade
        total_count += 1
        
    return int(total_grade//total_count)
    
  def get_student_grade_avg(self, course_id, student_id) -> int:
    course = self.get_course_by_id(course_id)
    student = course.get_student_by_id(student_id) # to ensure student exists
    total_grade, total_count = 0, 0
    
    for (s_id, a_id), grade in course.grades.items():
      if s_id == student.id:
        total_grade += grade
        total_count += 1
    
    return int(total_grade//total_count)

  def get_top_five_students(self, course_id) -> List[int]:
    course = self.get_course_by_id(course_id)
    student_grades = {} # {student_id : total_grade}
    
    if not course.students_enrolled:
        raise ValueError(f"No students are enrolled in the course with ID {course_id}.")
    
    for student_id in course.students_enrolled.keys():
      student_grades[student_id] = self.get_student_grade_avg(course_id, student_id)
    
    sorted_student_grades = sorted(student_grades.items(), key=lambda x: x[1], reverse=True) # using grades to sort in Descending order
    top_student_ids = [student_id for student_id, student_object in sorted_student_grades[:5]] # slicing top 5 from sorted grades
    top_students = [ course.students_enrolled[student_id] for student_id in top_student_ids ] # getting the object for top 5 students
    
    return top_students

class Course():
  def __init__(self, course_name, course_id):
    self.id = course_id
    self.name = course_name
    self.assignment_id = 0 # assignment id generator
    self.assignments = {} # {assignment_id : assignment_object}
    self.students_enrolled = {} # {student_id : student_object}
    self.grades = {} # {(student_id, assignment_id) : grade} 
  
  def get_student_by_id(self, student_id):
    try:
      student = self.students_enrolled[student_id]
      return student
    except KeyError:
      raise KeyError(f"Student with ID {student_id} not found in Course: {self.name} (id:{self.id})")
  
  def get_assignment_by_id(self, assignment_id):
    try:
      assignment = self.assignments[assignment_id]
      return assignment
    except KeyError:
      raise KeyError(f"Assignment with ID {assignment_id} not found in Course: {self.name} (id:{self.id})")
    
  def create_course_assignment(self, assignment_name):
    new_assignment = Assignment(assignment_name, self.assignment_id)
    self.assignments[self.assignment_id] = new_assignment
    self.assignment_id += 1 
    
  def enroll_student_in_course(self, student_id):
    if student_id in self.students_enrolled.keys():
      raise ValueError(f"Student with ID {student_id} is already enrolled in Course: {self.name} (id:{self.id})")
    
    new_student = Student(student_id)
    self.students_enrolled[student_id] = new_student
    
  def drop_student_from_course(self, student_id, course_id):
    try:
      self.students_enrolled.pop(student_id)
    except KeyError:
      raise KeyError(f"Student with ID {student_id} not found in Course: {self.name} (id:{self.id})")
    
class Assignment():
  def __init__(self, assignment_name, assignment_id):
    self.id = assignment_id
    self.name = assignment_name
    
class Student():
  def __init__(self, student_id):
    self.id = student_id
    
