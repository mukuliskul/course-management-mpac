# This file was used for tests while developing the various functionalities, it is raw documentation of all the tests I was conducting during development to ensure ideal output
# it also contains two print functions which appropriately print the course object return by functions (get_courses() and get_course_by_id())
# These print functions were used to ensure the intended data was being added/removed from the Course object
# This is not the file for unit tests, the testing file can be found in tests/test_course_service_implementation.py

from app.course_service_impl import CourseServiceImpl


def print_all_courses(course_service):
  courses_list = course_service.get_courses() 
  print("\nRUNNING: Printing all courses")
  print("-" * 20)
  for course in courses_list:
    course_info = (
      f"course_id: {course.id}\n"
      f"course_name: {course.name}\n"
      f"course_students_enrolled: {[student for student in course.students_enrolled.keys()]}\n"
      f"course_assignments: {[f'{assignment.id} : {assignment.name}' for assignment in course.assignments.values()]}\n"
      f"course_grades: {[f'student_id={s_id}, assignment_id={a_id}) : grade={grade}' for (s_id, a_id), grade in course.grades.items()]}\n"
    )
    print(course_info)

def print_course_by_id(course_service, id):
  course = course_service.get_course_by_id(id)
  print(f"\nRUNNING: Printing course with id: {course.id}")
  print("-" * 20)
  course_info = (
      f"course_id: {course.id}\n"
      f"course_name: {course.name}\n"
      f"course_students_enrolled: {[student.id for student in course.students_enrolled]}\n"
      f"course_assignments: {[assignment.name for assignment in course.assignments.values()]}\n"
  )
  print(course_info)


if __name__ == "__main__":
  course_service = CourseServiceImpl()

  # Start receiving requests...  
  
  # adding courses
  course_service.create_course("Course1") # id = 0 (auto-generated)
  course_service.create_course("Course2") # id = 1 (auto-generated)
  course_service.create_course("Course3") # id = 2 (auto-generated)
  
  # printing all courses
  print_all_courses(course_service)
  
  # printing course by id
  print_course_by_id(course_service, 0)
  print_course_by_id(course_service, 1)
  print_course_by_id(course_service, 2)
  
  # deleting the course and then viewing all courses
  course_service.delete_course(1)
  print_all_courses(course_service)

  
  # enrolling students
  course_service.enroll_student(0, 10)
  course_service.enroll_student(0, 20)
  course_service.enroll_student(0, 30)
  
  # Raises error since Student id : 30 already exists in course id 0
  # course_service.enroll_student(0, 30)
  
  # Raises error since Course id : 1 was removed
  # course_service.enroll_student(1, 11)
  
  course_service.enroll_student(2, 12)
  course_service.enroll_student(2, 22)
  course_service.enroll_student(2, 32)
  course_service.enroll_student(2, 42)
  course_service.enroll_student(2, 52)
  
  # checking if the students were ADDED by printing the course objects
  print_all_courses(course_service)
  
  # removing students
  course_service.dropout_student(0, 10)
  course_service.dropout_student(2, 42)
  course_service.dropout_student(2, 52)
  
  # Raises error since Student id : 10 does not exist
  # course_service.enroll_student(0, 10)  
  # Raises error since Course id : 3 does not exist
  # course_service.enroll_student(3, 13)  
  
  # checking if the students were REMOVED by printing the course objects
  print_all_courses(course_service)
  
  # creating assignments
  course_service.create_assignment(0, "Assignment00")
  course_service.create_assignment(0, "Assignment01")
  course_service.create_assignment(0, "Assignment02")
  course_service.create_assignment(0, "Assignment02")
  
  course_service.create_assignment(2, "Assignment20")
  course_service.create_assignment(2, "Assignment21")
  
  # Raises error since Course id : 3 does not exist
  # course_service.create_assignment(3, "Assignment30")
  
  # checking if the assignments were ADDED by printing the course objects
  print_all_courses(course_service)
  
  # submitting assignments (course_id, student_id, assignment_id, grade)
  course_service.submit_assignment(2, 12, 0, 10)
  course_service.submit_assignment(2, 12, 1, 10)
  
  
  course_service.submit_assignment(2, 22, 0, 20)
  course_service.submit_assignment(2, 22, 1, 20)
  course_service.submit_assignment(2, 32, 0, 20)
  
  # Raises error since Assignment id : 2 does not exist in course id : 2
  # course_service.submit_assignment(2, 12, 2, 10)
  
  # checking if the assignments were SUBMITTED by printing the course objects
  print_all_courses(course_service)
  
  # getting assignment averages
  # creating a new course_service
  new_course_service = CourseServiceImpl()
  course_id = 0
  assignment_id = 0
  student_ids = [1,2,3,4,5]
  grades = [10, 20, 30, 40, 50] # expected average is 30 (total of grades / total of students)
  
  new_course_service.create_course("Test Course")
  new_course_service.create_assignment(course_id, "Test Assignment")
  for i in range(len(student_ids)):
      new_course_service.enroll_student(course_id, student_ids[i]) # enrolling 5 students
      new_course_service.submit_assignment(course_id, student_ids[i], assignment_id, grades[i]) # submitting 1 assignment each
  actual_assignment_average = new_course_service.get_assignment_grade_avg(course_id, assignment_id)
  print(actual_assignment_average) # outputs 30 which is same as expected
  
  # getting assignment averages
  # creating a new course_service
  new_course_service = CourseServiceImpl()
  course_id = 0
  assignment_id = 0
  student_ids = [1,2,3,4,5]
  grades = [10.2, 20.5, 30.3, 40.9, 50.1] # expected average is 30 (total of grades / total of students)
  
  new_course_service.create_course("Test Course")
  new_course_service.create_assignment(course_id, "Test Assignment")
  for i in range(len(student_ids)):
      new_course_service.enroll_student(course_id, student_ids[i]) # enrolling 5 students
      new_course_service.submit_assignment(course_id, student_ids[i], assignment_id, grades[i]) # submitting 1 assignment each
  actual_assignment_average = new_course_service.get_assignment_grade_avg(course_id, assignment_id)
  print(actual_assignment_average) # outputs 30 which is same as expected
  
  # remaining function tests can be found in tests/test_course_service_implementation
  
  # Raises error since Course id : 3 does not exist  
  # print(course_service.get_assignments_by_course_id(3))


  