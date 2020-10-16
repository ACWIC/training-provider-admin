from app.requests import ValidRequest


class UpdateCourseRequest(ValidRequest):
    course_id: str
    course_name: str
    industry_standards: str
    competancy: str
    location: str
    date: str
    availablity: str
    hours_per_week: str
    duration: str
    fees_from: str
    # created: str
