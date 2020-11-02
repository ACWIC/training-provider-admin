import abc

from app.requests.create_course_request import NewCourseRequest


class CourseRepo(abc.ABC):
    @abc.abstractmethod
    def create_course(self, create_course_request: NewCourseRequest):  # -> None:
        """"""

    @abc.abstractmethod
    def update_course(self, new_course: dict):  # -> None:
        """"""

    @abc.abstractmethod
    def get_course(self, course_id: str):  # -> None:
        """"""
