import grpc

import course_service_pb2_grpc
import course_service_pb2

# Устанавливаем соединение с сервером
channel = grpc.insecure_channel('localhost:50051')
stub = course_service_pb2_grpc.CourseServiceStub(channel)

# Отправляем запрос
response = stub.GetCourse(course_service_pb2.GetCourseRequest(course_id = "api-course"))
print(f'course_id: "{response.course_id}"', f'title: "{response.title}"', f'description: "{response.description}"', sep="\n")  