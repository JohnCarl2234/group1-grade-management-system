# Streamlit Project Restructuring Guide

This guide outlines how to reorganize your grade management system to follow Streamlit app conventions.

## New Project Structure

```
group1-grade-management-system/
├── app.py                    # Main Streamlit app entry point (rename from streamlit_app.py)
├── auth.py                   # Authentication module (keep at root level)
├── requirements.txt
├── data/                     # Unchanged - data files
│   ├── grades.csv
│   ├── students.csv
│   └── users.json
├── src/                      # Backend logic
│   ├── __init__.py
│   ├── controllers/          # Business logic controllers
│   │   ├── __init__.py
│   │   ├── grade_controller.py
│   │   ├── report_controller.py
│   │   └── student_controller.py
│   ├── models/              # Data models
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── student.py
│   │   └── user.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── exporter.py
│       ├── file_handler.py
│       └── grade_calculator.py
├── pages/                   # Multi-page app pages (Streamlit convention)
│   ├── 1_Dashboard.py      # From views/dashboard_view.py
│   ├── 2_Students.py       # From views/student_view.py
│   ├── 3_Grades.py         # From views/grade_view.py
│   └── 4_Reports.py        # From views/report_view.py
├── views/                  # Keep for reference (can be deprecated later)
│   └── ... (existing view files)
└── .streamlit/
    └── config.toml         # Streamlit configuration
```

## Migration Steps

### 1. Move Backend Logic
Copy the following directories to `src/`:
- `controllers/` → `src/controllers/`
- `models/` → `src/models/`
- `utils/` → `src/utils/`

```bash
# Example using PowerShell
Copy-Item -Path .\controllers\* -Destination .\src\controllers\ -Recurse
Copy-Item -Path .\models\* -Destination .\src\models\ -Recurse
Copy-Item -Path .\utils\* -Destination .\src\utils\ -Recurse
```

### 2. Create Page Templates
Create page files in the `pages/` directory. Each page should:
- Import from `src.controllers`, `src.models`, and `src.utils`
- Have a numbered prefix (1_, 2_, 3_, 4_) for page ordering in Streamlit
- Import authentication/session state from main app

**Example: pages/1_Dashboard.py**
```python
import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.controllers.grade_controller import GradeController
from src.utils.file_handler import FileHandler

st.set_page_config(page_title="Dashboard", layout="wide")

def main():
    # Your dashboard code here
    pass

if __name__ == "__main__":
    main()
```

### 3. Rename Main App File
Rename `streamlit_app.py` to `app.py` and update imports:

**Update imports from:**
```python
from controllers.grade_controller import ...
from utils.file_handler import ...
```

**To:**
```python
from src.controllers.grade_controller import ...
from src.utils.file_handler import ...
```

### 4. Update Import Statements
In all moved files, update relative imports:

**Old (from controllers/grade_controller.py):**
```python
from models.student import Student
from utils.grade_calculator import calculate_gpa
```

**New:**
```python
from src.models.student import Student
from src.utils.grade_calculator import calculate_gpa
```

Or use relative imports:
```python
from ..models.student import Student
from ..utils.grade_calculator import calculate_gpa
```

### 5. Keep Data Files at Root
The `data/` directory should remain at the project root. Update file paths in code:

**Use this pattern (as noted in repo memory):**
```python
from pathlib import Path
data_path = Path(__file__).resolve().parents[1] / "data" / "students.csv"
# Or for src files:
data_path = Path(__file__).resolve().parents[2] / "data" / "students.csv"
```

### 6. Run the App
After migration, run:
```bash
streamlit run app.py
```

## Benefits of New Structure

✅ **Follows Streamlit Conventions** - Organized as per official Streamlit best practices
✅ **Scalable** - Easy to add more pages using the numbered prefix system
✅ **Clear Separation** - Backend logic separated from UI pages
✅ **Multi-page Support** - Streamlit automatically discovers and organizes pages
✅ **Configuration Management** - `.streamlit/config.toml` for centralized settings

## Optional: Clean Up

After verifying everything works:
```bash
# Remove old directory structure if no longer needed
Remove-Item -Path .\views -Recurse -Force
Remove-Item -Path .\controllers -Recurse -Force
Remove-Item -Path .\models -Recurse -Force
Remove-Item -Path .\utils -Recurse -Force
```

## Notes

- `auth.py` is kept at root level as it's typically imported by the main app
- File paths using `Path(__file__).resolve().parents[1]` may need adjustment based on new file location
- Pages are discovered automatically by Streamlit in the `pages/` directory
- Numbered prefixes (1_, 2_, etc.) determine the order pages appear in the sidebar
