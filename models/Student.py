class Student:
    def __init__(self, student_id: str, name: str, course: str, year_level: str, status: str = "Enrolled"):
        self.student_id = str(student_id).strip()
        self.name = str(name).strip()
        self.course = str(course).strip()
        self.year_level = str(year_level).strip()
        self.status = str(status).strip()

    @property
    def is_enrolled(self) -> bool:
        return self.status.lower() == "enrolled"
    
    def to_dict(self) -> dict:
        return {
            "student ID": self.student_id, 
            "name": self.name,
            "course": self.course,
            "year level": self.year_level,
            "status": self.status
        }