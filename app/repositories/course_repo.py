import abc

from app.domain.entities.course import Course
from app.requests.create_course_request import NewCourseRequest
from app.requests.update_course_request import UpdateCourseRequest


class CourseRepo(abc.ABC):
    @abc.abstractmethod
    def create_course(self, create_course_request: NewCourseRequest) -> Course:
        pass

    @abc.abstractmethod
    def update_course(self, update_course_request: UpdateCourseRequest) -> Course:
        pass

    @abc.abstractmethod
    def get_course(self, course_id: str) -> Course:
        pass

    @abc.abstractmethod
    def course_exists(self, course_id: str) -> bool:
        pass
