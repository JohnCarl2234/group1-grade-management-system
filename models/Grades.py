

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

    # ── Properties (grading logic lives here, not in pages) ──────────────────

    @property
    def is_passing(self) -> bool:
        """Return True if the grade is passing (3.0 or below)."""
        return self.grade <= self.PASSING_GRADE

    @property
    def remarks(self) -> str:
        """Return a human-readable pass/fail remark.

        Example:
            grade = 1.5  →  "✅ Passed"
            grade = 5.0  →  "❌ Failed"
        """
        return "✅ Passed" if self.is_passing else "❌ Failed"

    @property
    def description(self) -> str:
        """Return the descriptive equivalent of the grade.

        Example:
            grade = 1.5  →  "Very Good"
            grade = 3.0  →  "Passing"
            grade = 5.0  →  "Failed"
        """
        return self.GRADE_DESCRIPTIONS.get(self.grade, "—")

    @property
    def is_valid(self) -> bool:
        """Return True if the grade is in the accepted values list."""
        return self.grade in self.VALID_GRADES

    # ── Class-level helpers ───────────────────────────────────────────────────

    @classmethod
    def compute_average(cls, grades: list["Grades"]) -> float:
        """Compute the average of a list of Grade objects.

        Args:
            grades: list of Grade instances

        Returns:
            Rounded average to 2 decimal places, or 0.0 if list is empty

        Example:
            avg = Grade.compute_average([g1, g2, g3])
        """
        if not grades:
            return 0.0
        return round(sum(g.grade for g in grades) / len(grades), 2)

    @classmethod
    def average_remarks(cls, average: float) -> str:
        """Return pass/fail remark for a computed average.

        Args:
            average: the computed semester or overall average

        Returns:
            "✅ Passed" or "❌ Failed"
        """
        return "✅ Passed" if average <= cls.PASSING_GRADE else "❌ Failed"

    @classmethod
    def average_description(cls, average: float) -> str:
        """Return the description closest to the computed average.

        Since averages may not land exactly on a valid grade value,
        this finds the nearest valid grade and returns its description.

        Args:
            average: the computed average

        Returns:
            Description string (e.g. "Good", "Satisfactory")
        """
        nearest = min(cls.VALID_GRADES, key=lambda v: abs(v - average))
        return cls.GRADE_DESCRIPTIONS.get(nearest, "—")

    # ── Conversion helpers ────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Convert the Grade object to a plain dictionary.

        Used when writing back to grades.csv via file_handler.
        """
        return {
            "student_id": self.student_id,
            "semester":   self.semester,
            "subject":    self.subject,
            "grade":      self.grade,
        }

    @staticmethod
    def from_dict(data: dict) -> "Grades":
        """Create a Grade object from a dictionary.

        Used when reading a row from grades.csv via file_handler.

        Args:
            data: dict with keys student_id, semester, subject, grade

        Returns:
            Grade instance

        Example:
            row = {"student_id": "2025-00001", "semester": "1st Semester", ...}
            grade = Grade.from_dict(row)
        """
        return Grades(
            student_id=data.get("student_id", ""),
            semester=data.get("semester", ""),
            subject=data.get("subject", ""),
            grade=data.get("grade", 5.0),
        )

    # ── String representation ─────────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"Grade(student_id='{self.student_id}', semester='{self.semester}', "
            f"subject='{self.subject}', grade={self.grade})"
        )

    def __str__(self) -> str:
        return f"{self.subject} ({self.semester}): {self.grade} — {self.description}"
