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

    def update_course(self, new_course: dict):
        print("update_course()", new_course["course_id"])
        old_course = self.get_course(new_course["course_id"])
        course = update_course_attributes(old_course, new_course)
        print("Course", course)
        # Write to bucket
        self.s3.put_object(
            Body=bytes(course.json(), "utf-8"),
            Key=f"courses/{course.course_id}.json",
            Bucket=settings.COURSE_BUCKET,
        )
        return course

    def get_course(self, course_id: str):
        print("get_course()", course_id)
        obj = self.s3.get_object(
            Key=f"courses/{course_id}.json", Bucket=settings.COURSE_BUCKET
        )
        course = Course(**json.loads(obj["Body"].read().decode()))
        return course


def update_course_attributes(old_course, new_course):
    if new_course["course_name"] != "":
        old_course.course_name = new_course["course_name"]
    if new_course["industry_standards"] != "":
        old_course.industry_standards = new_course["industry_standards"]
    if new_course["competancy"] != "":
        old_course.competancy = new_course["competancy"]
    if new_course["location"] != "":
        old_course.location = new_course["location"]
    if new_course["date"] != "":
        old_course.date = new_course["date"]
    if new_course["availablity"] != "":
        old_course.availablity = new_course["availablity"]
    if new_course["hours_per_week"] != "":
        old_course.hours_per_week = new_course["hours_per_week"]
    if new_course["duration"] != "":
        old_course.duration = new_course["duration"]
    if new_course["fees_from"] != "":
        old_course.fees_from = new_course["fees_from"]
    return old_course
