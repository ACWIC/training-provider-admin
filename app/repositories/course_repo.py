import abc


class CourseRepo(abc.ABC):
    @abc.abstractmethod
    def save_course(self, input_course: dict) -> None:
        pass

    @abc.abstractmethod
    def update_course(self, course: dict) -> None:
        pass
