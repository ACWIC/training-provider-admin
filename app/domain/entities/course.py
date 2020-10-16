from pydantic import BaseModel


class Course(BaseModel):
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
    created: str


# https://www.tafensw.edu.au/courses/aged-care-and-nursing-courses

# course_name:
# Bachelor of Community Services (HE20528)
# Diploma of Leisure and Health (CHC53415)
# Diploma of Community Services (Case Management) (CHC52015)
# Certificate IV in Ageing Support (CHC43015)

# location: Sydney, Grafton, Ballina, Meadowbank
# industry_standards: Police Check, drivers licence

# {
#   "course_id": "1",
#   "course_name": "Health care",
#   "industry_standards": "",
#   "competancy": "string",
#   "location": "string",
#   "date": "string",
#   "availablity": "string"
# }
