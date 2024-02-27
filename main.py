from app.course_service_impl import CourseServiceImpl

if __name__ == "__main__":
  course_service = CourseServiceImpl()

  # Start receiving requests...  
  
  # running course CRUD
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
  
  mylsit = [100, 200, 300]
  
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
  course_service.dropout_student(3, 0)
  
  print(course_service.get_students_by_course_id(0))
  print(course_service.get_students_by_course_id(2))