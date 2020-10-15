import json
from typing import Any

import boto3

from app.config import settings
from app.domain.entities.course import Course
from app.domain.entities.course_filter import CourseFilters
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

    def update_course(self, input_course: dict):
        print("save_course()", input_course)
        course = Course(**input_course)
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

    def course_search(self, course_filters: dict):
        course_filters = CourseFilters(**course_filters)
        # print("course_filters", type(course_filters), course_filters)
        # get courses
        courses_objects_list = self.s3.list_objects(
            Bucket=settings.COURSE_BUCKET  # Prefix="{}/".format(enrolment_id)
        )
        # print("courses_objects_list", courses_objects_list)
        courses_list = []
        # If there have been 0 courses, the list should be empty.
        if "Contents" not in courses_objects_list:
            return {"courses_list": courses_list}
        # 1 by 1
        for row in courses_objects_list["Contents"]:
            obj = self.s3.get_object(Key=row["Key"], Bucket=settings.COURSE_BUCKET)
            course = Course(**json.loads(obj["Body"].read().decode()))
            if if_filter(course, course_filters):
                courses_list.append({"Course": course})
        return {"courses_list": courses_list}


def if_filter(course, course_filters):
    filter_by = True
    # industry_standards, competancy, location, date, availablity
    if (
        course.industry_standards != course_filters.industry_standards
        and course_filters.industry_standards != ""
    ):
        filter_by = False
    elif (
        course.competancy != course_filters.competancy
        and course_filters.competancy != ""
    ):
        filter_by = False
    elif course.location != course_filters.location and course_filters.location != "":
        filter_by = False
    elif course.date != course_filters.date and course_filters.date != "":
        filter_by = False
    elif (
        course.availablity != course_filters.availablity
        and course_filters.availablity != ""
    ):
        filter_by = False
    return filter_by
