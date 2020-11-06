import datetime
import json
from typing import Any

import boto3

from app.config import settings
from app.domain.entities.course import Course
from app.repositories.course_repo import CourseRepo
from app.requests.create_course_request import NewCourseRequest
from app.requests.update_course_request import UpdateCourseRequest
from app.utils import Random
from app.utils.error_handling import handle_s3_errors


class S3CourseRepo(CourseRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.s3 = boto3.client("s3", **settings.s3_configuration)

    def create_course(self, create_course_request: NewCourseRequest) -> Course:
        input_course = create_course_request.dict()
        input_course["course_id"] = Random.get_uuid()
        input_course["created"] = datetime.datetime.now()
        course = Course(**input_course)
        with handle_s3_errors():
            self.s3.put_object(
                Body=bytes(course.json(), "utf-8"),
                Key=f"courses/{course.course_id}.json",
                Bucket=settings.COURSE_BUCKET,
            )
        return course

    def update_course(self, update_course_request: UpdateCourseRequest) -> Course:
        new_course = update_course_request.dict()
        old_course = self.get_course(new_course["course_id"])
        old_course = old_course.dict()
        old_course.update((k, v) for k, v in new_course.items() if v is not None)
        course = Course(**old_course)
        with handle_s3_errors():
            self.s3.put_object(
                Body=bytes(course.json(), "utf-8"),
                Key=f"courses/{course.course_id}.json",
                Bucket=settings.COURSE_BUCKET,
            )
        return course

    def get_course(self, course_id: str) -> Course:
        with handle_s3_errors():
            obj = self.s3.get_object(
                Key=f"courses/{course_id}.json", Bucket=settings.COURSE_BUCKET
            )
        course = Course(**json.loads(obj["Body"].read().decode()))
        return course

    def course_exists(self, course_id: str) -> bool:
        try:
            self.s3.get_object(
                Key=f"courses/{course_id}.json",
                Bucket=settings.COURSE_BUCKET,
            )
            return True
        except Exception:
            return False
