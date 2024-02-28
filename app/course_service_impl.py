from typing import List
from app.course_service import CourseService

# Business Logic Assumptions in the code :
# 1. Using a manual id generator for simplicity and readability rather than using uuid
# 2. Dictionary operations are wrapped in try-catch block to override with custom exceptions
# 3. Re-submission of assignments are not allowed
# 4. Creation of assignments with same name is permitted but assignment_id always stays unique

class Assignment:
  """
  Represents an assignment within a course.
  """
  def __init__(self, name: str, assignment_id: int):
    """
    Initializes a new instance of Assignment.

    Parameters:
        name (str): The name of the assignment.
        assignment_id (int): The unique identifier for the assignment.
    """
    self.name = name
    self.id = assignment_id
    
    
class Student:
  """
  Represents a student enrolled in a course.
  """
  def __init__(self, student_id: int):
      """
      Initializes a new instance of Student.

      Parameters:
          student_id (int): The unique identifier for the student.
      """
      self.id = student_id


class Course:
  """
  Represents a course, including its assignments, enrolled students, and grades.
  """
  def __init__(self, name: str, course_id: int):
    """
    Initializes a new instance of Course.

    Parameters:
        name (str): The name of the course.
        course_id (int): The unique identifier for the course.
    """
    self.name = name
    self.id = course_id
    self.assignments = {}  # Stores assignments with their IDs as keys
    self.assignment_id = 0  # Generator for assignment IDs
    self.students_enrolled = {}  # Stores enrolled students with their IDs as keys
    self.grades = {}  # Stores grades with (student_id, assignment_id) as keys

  def create_course_assignment(self, assignment_name: str):
    """
    Creates an assignment for the course.

    Parameters:
        assignment_name (str): The name of the assignment.
    """
    new_assignment = Assignment(assignment_name, self.assignment_id)
    self.assignments[self.assignment_id] = new_assignment
    self.assignment_id += 1

  def enroll_student_in_course(self, student_id: int):
    """
    Enrolls a student in the course.

    Parameters:
        student_id (int): The ID of the student to enroll.

    Raises:
        ValueError: If student with the given ID already exists.
    """
    if student_id in self.students_enrolled.keys():
      raise ValueError(f"Student with ID {student_id} is already enrolled in Course: {self.name} (id:{self.id})")

    new_student = Student(student_id)
    self.students_enrolled[student_id] = new_student

  def drop_student_from_course(self, student_id: int, course_id: int):
    """
    Drops a student from the course.

    Parameters:
        student_id (int): The ID of the student to drop.
        course_id (int): The ID of the course from which to drop the student.
    """
    if student_id in self.students_enrolled:
        del self.students_enrolled[student_id]
    else:
        raise ValueError(f"Student {student_id} is not enrolled in course {course_id}")

  def get_assignment_by_id(self, assignment_id: int) -> Assignment:
    """
    Retrieves an assignment by its ID.

    Parameters:
        assignment_id (int): The ID of the assignment to retrieve.
    
    Returns:
        Assignment: The assignment object associated with the given ID.
    
    Raises:
        KeyError: If no assignment with the given ID is found.
    """
    try:
        assignment = self.assignments[assignment_id]
        return assignment
    except KeyError:
        raise KeyError(f"Assignment with ID {assignment_id} not found in course {self.id}")
      
  def get_student_by_id(self, student_id):
    """
    Retrieves a student by its ID.

    Parameters:
        student_id (int): The ID of the student to retrieve.
    
    Returns:
        Student: The student object associated with the given ID.
    
    Raises:
        KeyError: If no student with the given ID is found.
    """
    try:
      student = self.students_enrolled[student_id]
      return student
    except KeyError:
      raise KeyError(f"Student with ID {student_id} not found in Course: {self.name} (id:{self.id})")


class CourseServiceImpl(CourseService):
  """
  Implementation of CourseService that manages courses, assignments, and student enrollments.
  """
  def __init__(self):
    """
    Initializes a new instance of CourseServiceImpl.
    """
    self.courses = {}  # Stores courses with their IDs as keys
    self.course_id = 0  # Generator for course IDs

  def get_courses(self) -> List[Course]:
    """
    Retrieves all courses.

    Returns:
        List[Course]: A list of all courses.
    
    Raises:
        LookupError: If no courses are found.
    """
    if not self.courses:
        raise LookupError("No courses found")
    else:
        return [course for course in self.courses.values()]

  def get_course_by_id(self, course_id: int) -> Course:
    """
    Retrieves a course by its ID.

    Parameters:
        course_id (int): The ID of the course to retrieve.
    
    Returns:
        Course: The course object associated with the given ID.

    Raises:
        KeyError: If no course with the given ID is found.
    """
    try:
        course = self.courses[course_id]
        return course
    except KeyError:
        raise KeyError(f"Course with ID {course_id} not found")

  def create_course(self, course_name: str):
    """
    Creates a new course with a given name.

    Parameters:
        course_name (str): The name of the course to create.
    """
    new_course = Course(course_name, self.course_id)
    self.courses[self.course_id] = new_course
    self.course_id += 1

  def delete_course(self, course_id: int):
    """
    Deletes a course by its ID.

    Parameters:
        course_id (int): The ID of the course to delete.
    """
    self.get_course_by_id(course_id)  # Ensures the course exists before deletion
    self.courses.pop(course_id)

  def create_assignment(self, course_id: int, assignment_name: str):
    """
    Creates an assignment for a course.

    Parameters:
        course_id (int): The ID of the course.
        assignment_name (str): The name of the assignment.
    """
    course = self.get_course_by_id(course_id)
    course.create_course_assignment(assignment_name)

  def enroll_student(self, course_id: int, student_id: int):
    """
    Enrolls a student in a course.

    Parameters:
        course_id (int): The ID of the course.
        student_id (int): The ID of the student.
    """
    course = self.get_course_by_id(course_id)
    course.enroll_student_in_course(student_id)

  def dropout_student(self, course_id: int, student_id: int):
    """
    Drops a student from a course.

    Parameters:
        course_id (int): The ID of the course.
        student_id (int): The ID of the student.
    """
    course = self.get_course_by_id(course_id)
    course.drop_student_from_course(student_id, course_id)

  def submit_assignment(self, course_id: int, student_id: int, assignment_id: int, grade: int):
    """
    Submits an assignment for a student with a given grade.

    Parameters:
        course_id (int): The ID of the course.
        student_id (int): The ID of the student.
        assignment_id (int): The ID of the assignment.
        grade (int): The grade of the submission.

    Raises:
        ValueError: If the grade is not between 0 and 100, or if the assignment has already been submitted.
    """
    if grade < 0 or grade > 100:
      raise ValueError("Grade must be between 0 and 100 inclusive.")

    course = self.get_course_by_id(course_id)
    student = course.get_student_by_id(student_id) # Ensures student with student_id does exist
    assignment = course.get_assignment_by_id(assignment_id) # Ensures assignment with assignment_id does exist
    
    # ensuring there are no re-submissions
    existing_grade = course.grades.get((student_id, assignment_id))
    if existing_grade is not None:
        raise ValueError(f"Student ID: {student_id} has already submitted {course.assignments[assignment_id].name} (id:{assignment_id}) in Course: {course.name} (id:{course_id})")

    course.grades[(student.id, assignment.id)] = grade

  def get_assignment_grade_avg(self, course_id: int, assignment_id: int) -> int:
    """
    Calculates the average grade for an assignment in a course.

    Parameters:
        course_id (int): The ID of the course.
        assignment_id (int): The ID of the assignment.
    
    Returns:
        int: The average grade for the assignment.
    """
    course = self.get_course_by_id(course_id)
    assignment = course.get_assignment_by_id(assignment_id)  # Ensures the assignment exists
    total_grade, total_count = 0, 0

    for (_, a_id), grade in course.grades.items():
        if a_id == assignment.id:
            total_grade += grade
            total_count += 1

    return int(total_grade // total_count)
    
  def get_student_grade_avg(self, course_id: int, student_id: int) -> int:
    """
    Calculates the average grade for a student in a course.

    Parameters:
        course_id (int): The ID of the course.
        student_id (int): The ID of the student.
    
    Returns:
        int: The average grade of the student across all assignments in the course.
    """
    course = self.get_course_by_id(course_id)
    student = course.get_student_by_id(student_id) # Ensures the student exists
    total_grade, total_count = 0, 0
    
    for (s_id, a_id), grade in course.grades.items():
      if s_id == student.id:
        total_grade += grade
        total_count += 1
    
    return int(total_grade//total_count)

  def get_top_five_students(self, course_id: int) -> List[int]:
    """
    Retrieves the top five students based on their average grades in a course.

    Parameters:
        course_id (int): The ID of the course.
    
    Returns:
        List[Student]: A list of the top five students in the course.
    
    Raises:
        ValueError: If no students are enrolled in the course.
    """

    course = self.get_course_by_id(course_id)
    student_grades = {} # {student_id : total_grade}
    
    if not course.students_enrolled:
        raise ValueError(f"No students are enrolled in the course with ID {course_id}.")
    
    for student_id in course.students_enrolled.keys():
      student_grades[student_id] = self.get_student_grade_avg(course_id, student_id)
    
    sorted_student_grades = sorted(student_grades.items(), key=lambda x: x[1], reverse=True) # using grades to sort in Descending order
    top_student_ids = [student_id for student_id, student_object in sorted_student_grades[:5]] # slicing top 5 from sorted grades

    return top_student_ids


    
