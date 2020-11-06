import datetime

from app.domain.entities.course import Course
from app.requests.create_course_request import NewCourseRequest
from app.requests.update_course_request import UpdateCourseRequest


class CourseDataProvider:  # (BaseModel):
    sample_course: Course
    sample_course_dict: dict
    sample_update_course_request: UpdateCourseRequest
    sample_update_course_request_dict: dict
    sample_create_course_request: NewCourseRequest
    sample_create_course_request_dict: dict
    sample_course_id: str
    sample_course_date: datetime

    def __init__(self):
        # course_id = str(uuid4())
        course_id = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
        date_time_str = "2018-06-29 08:15:27.243860"
        date = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")
        self.created = date
        self.sample_course_id = course_id
        self.sample_course_date = date

        # Course Sample
        self.sample_course = Course(
            course_id=course_id,
            course_name="Bachelor of Community Services (HE20528)",
            industry_standards="Police Check",
            competency="top rated",
            location="Sydney",
            date=date,
            availability=True,
            hours_per_week=10,
            duration="2 months",
            fees_from=200,
            created=self.created,
        )
        self.sample_course_dict = vars(self.sample_course)

        # UpdateCourseRequest Sample
        self.sample_update_course_request = UpdateCourseRequest(
            course_id=course_id,
            course_name="Bachelor of Community Services (HE20528)",
            industry_standards="Police Check",
            competency="top rated",
            location="Sydney",
            date=date,
            availability=True,
            hours_per_week=10,
            duration="2 months",
            fees_from=200,
        )
        self.sample_update_course_request_dict = vars(self.sample_update_course_request)

        # NewCourseRequest Sample
        self.sample_create_course_request = NewCourseRequest(
            course_name="Bachelor of Community Services (HE20528)",
            industry_standards="Police Check",
            competency="top rated",
            location="Sydney",
            date=date,
            availability=True,
            hours_per_week=10,
            duration="2 months",
            fees_from=200,
        )
        self.sample_create_course_request_dict = vars(self.sample_create_course_request)
