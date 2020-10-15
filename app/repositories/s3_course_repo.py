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

    def save_course(self, input_course: dict):
        print("save_course()", input_course)
        course = Course(**input_course)
        # Write to bucket
        self.s3.put_object(
            Body=bytes(course.json(), "utf-8"),
            Key=f"courses/{course.course_id}.json",
            Bucket=settings.COURSE_BUCKET,
        )
        return course
