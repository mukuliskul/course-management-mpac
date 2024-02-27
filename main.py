from app.course_service_impl import CourseServiceImpl

if __name__ == "__main__":
  course_service = CourseServiceImpl()

  # Start receiving requests...  
  
  # running course CRUD
  print("\nRUNNING : Course CRUD")
  print("-"*20)
  course_service.create_course("Testing0")
  course_service.create_course("Testing1")
  course_service.create_course("Testing2")
  
  print(course_service.get_courses())
  print(course_service.get_course_by_id(2))
  
  course_service.delete_course(1)
  
  print(course_service.get_courses())
  
  course_service.create_course("Testing3")
  course_service.create_course("Testing4")
  
  print(course_service.get_courses())
  
  # running student CRUD 
  print("\nRUNNING : Student CRUD")
  print("-"*20)
  course_service.enroll_student(0, 000)
  course_service.enroll_student(0, 100)
  course_service.enroll_student(0, 200)
  
  course_service.enroll_student(2, 222)
  course_service.enroll_student(2, 223)
  course_service.enroll_student(2, 224)
  course_service.enroll_student(2, 225)
  course_service.enroll_student(2, 226)
  
  print(course_service.get_students_by_course_id(0))
  print(course_service.get_students_by_course_id(2))
  
  course_service.dropout_student(0, 100)
  course_service.dropout_student(2, 222)
  
  print(course_service.get_students_by_course_id(0))
  print(course_service.get_students_by_course_id(2))
  
  # running assignment CRUD
  print("\nRUNNING : Assignment CRUD")
  print("-"*20)
  course_service.create_assignment(0, "Assignment00")
  course_service.create_assignment(0, "Assignment01")
  course_service.create_assignment(0, "Assignment02")
  course_service.create_assignment(2, "Assignment20")
  course_service.create_assignment(2, "Assignment21")
  course_service.create_assignment(3, "Assignment30")
  course_service.create_assignment(3, "Assignment31")
  course_service.create_assignment(3, "Assignment32")
  course_service.create_assignment(3, "Assignment33")
  course_service.create_assignment(3, "Assignment34")
  
  print(course_service.get_assignments_by_course_id(0))
  print(course_service.get_assignments_by_course_id(2))
  print(course_service.get_assignments_by_course_id(3))

  print("\nRUNNING : Grades CRUD")
  #TODO: Run functions for calculating average and top5 students