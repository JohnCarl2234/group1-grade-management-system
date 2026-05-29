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
    
    @staticmethod
    def get_data(data: dict) -> "Student":
        return Student(
            student_id = data.get("student ID", ""),
            name = data.get("name", ""),
            course = data.get("course", ""),
            year_level = data.get("year level", ""),
            status = data.get("status", "Enrolled")
        )
    
    def does_match(self, student_id: str, name: str, course: str, year_level: str) -> bool:
        return (
            self.student_id.lower() == student_id.lower().strip() and
            self.name.lower() == name.lower().strip() and
            self.course.lower() == course.lower().strip() and
            self.year_level.lower() == year_level.lower().strip()
        )
    
    def __repr__(self) -> str:
        return (
            f"Student ID='{self.student_id}', name='{self.name}', "
            f"course='{self.course}', year_level='{self.year_level}', "
            f"status='{self.status}')"
        )
 
    def __str__(self) -> str:
        return f"{self.name.capitalize()} ({self.student_id}) — {self.course.upper()}, {self.year_level}"
    
s1 = Student("01938", "skfls", "jadka", "jadfla")
    
print(s1)