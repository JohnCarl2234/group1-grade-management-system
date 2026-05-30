class Grades:

    PASSING_GRADE = 3.0

    VALID_GRADES = [round(x * 0.1, 1) for x in range(10, 51)]

    GRADE_DESCRIPTIONS = {
        **{round(x * 0.1, 1): "Excellent"    for x in range(10, 13)},  # 1.0 - 1.2
        **{round(x * 0.1, 1): "Very Good"    for x in range(13, 16)},  # 1.3 - 1.5
        **{round(x * 0.1, 1): "Good"         for x in range(16, 19)},  # 1.6 - 1.8
        **{round(x * 0.1, 1): "Satisfactory" for x in range(19, 22)},  # 1.9 - 2.1
        **{round(x * 0.1, 1): "Fair"         for x in range(22, 25)},  # 2.2 - 2.4
        **{round(x * 0.1, 1): "Passing"      for x in range(25, 31)},  # 2.5 - 3.0
        **{round(x * 0.1, 1): "Failed"       for x in range(31, 51)},  # 3.1 - 5.0
    }

    def __init__(
        self,
        student_id: str,
        semester: str,
        subject: str,
        grade: float | str,
    ):
        self.student_id = str(student_id).strip()
        self.semester   = str(semester).strip()
        self.subject    = str(subject).strip()
        self.grade      = float(grade)

    

    @property
    def is_passing(self) -> bool:
        
        return self.grade <= self.PASSING_GRADE

    @property
    def remarks(self) -> str:

        return "✅ Passed" if self.is_passing else "❌ Failed"

    @property
    def description(self) -> str:
     
        return self.GRADE_DESCRIPTIONS.get(self.grade, "—")

    @property
    def is_valid(self) -> bool:
    
        return self.grade in self.VALID_GRADES


    @classmethod
    def compute_average(cls, grades: list["Grades"]) -> float:
       
        if not grades:
            return 0.0
        return round(sum(g.grade for g in grades) / len(grades), 2)

    @classmethod
    def average_remarks(cls, average: float) -> str:
 
        return "✅ Passed" if average <= cls.PASSING_GRADE else "❌ Failed"

    @classmethod
    def average_description(cls, average: float) -> str:

        nearest = min(cls.VALID_GRADES, key=lambda v: abs(v - average))
        return cls.GRADE_DESCRIPTIONS.get(nearest, "—")

    # ── Conversion helpers ────────────────────────────────────────────────────

    def to_dict(self) -> dict:

        return {
            "student_id": self.student_id,
            "semester":   self.semester,
            "subject":    self.subject,
            "grade":      self.grade,
        }

    @staticmethod
    def from_dict(data: dict) -> "Grades":

        return Grades(
            student_id=data.get("student_id", ""),
            semester=data.get("semester", ""),
            subject=data.get("subject", ""),
            grade=data.get("grade", 5.0),
        )


    def __repr__(self) -> str:
        return (
            f"Grade(student_id='{self.student_id}', semester='{self.semester}', "
            f"subject='{self.subject}', grade={self.grade})"
        )

    def __str__(self) -> str:
        return f"{self.subject} ({self.semester}): {self.grade} — {self.description}"
