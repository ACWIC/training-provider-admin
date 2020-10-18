import abc


class CourseRepo(abc.ABC):
    @abc.abstractmethod
    def create_course(self, input_course: dict):  # -> None:
        pass

    @abc.abstractmethod
    def update_course(self, new_course: dict):  # -> None:
        pass

    @abc.abstractmethod
    def get_course(self, course_id: str):  # -> None:
        pass
