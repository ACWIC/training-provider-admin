import json
from typing import Any

import boto3

from app.config import settings
from app.domain.entities.course import Course
from app.repositories.course_repo import CourseRepo


class S3CourseRepo(CourseRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.params = {
            "aws_access_key_id": settings.S3_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.S3_SECRET_ACCESS_KEY,
            "endpoint_url": settings.S3_ENDPOINT_URL,
        }
        self.s3 = boto3.client("s3", **self.params)

    def create_course(self, input_course: dict):
        course = Course(**input_course)
        try:
            self.s3.put_object(  # Write to bucket
                Body=bytes(course.json(), "utf-8"),
                Key=f"courses/{course.course_id}.json",
                Bucket=settings.COURSE_BUCKET,
            )
        except Exception as exception:
            raise exception
        return course

    def update_course(self, new_course: dict):
        old_course = self.get_course(new_course["course_id"])
        old_course = vars(old_course)  # to dict
        old_course.update((k, v) for k, v in new_course.items() if v is not None)
        course = Course(**old_course)
        try:
            self.s3.put_object(  # Write to bucket
                Body=bytes(course.json(), "utf-8"),
                Key=f"courses/{course.course_id}.json",
                Bucket=settings.COURSE_BUCKET,
            )
        except Exception as exception:
            raise exception
        return course

    def get_course(self, course_id: str):
        try:
            obj = self.s3.get_object(  # Get from bucket
                Key=f"courses/{course_id}.json", Bucket=settings.COURSE_BUCKET
            )
        except Exception as exception:
            raise exception
        course = Course(**json.loads(obj["Body"].read().decode()))
        return course
