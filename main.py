from app.course_service_impl import CourseServiceImpl

if __name__ == "__main__":
  course_service = CourseServiceImpl()

  # Start receiving requests...  
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
