# Streamlit Restructuring Checklist

## ✅ Completed: New Directory Structure Created
- [x] `src/` directory with `__init__.py`
- [x] `src/controllers/` directory with `__init__.py`
- [x] `src/models/` directory with `__init__.py`
- [x] `src/utils/` directory with `__init__.py`
- [x] `pages/` directory ready for page files
- [x] `.streamlit/` directory with default `config.toml`
- [x] Migration guide created: `RESTRUCTURING_GUIDE.md`

## 📋 Next Steps: File Migration

### Phase 1: Move Backend Files
- [ ] Copy `controllers/*` → `src/controllers/`
- [ ] Copy `models/*` → `src/models/`
- [ ] Copy `utils/*` → `src/utils/`

### Phase 2: Create Pages
- [ ] Create `pages/1_Dashboard.py` from `views/dashboard_view.py`
- [ ] Create `pages/2_Students.py` from `views/student_view.py`
- [ ] Create `pages/3_Grades.py` from `views/grade_view.py`
- [ ] Create `pages/4_Reports.py` from `views/report_view.py`

### Phase 3: Update Main App
- [ ] Rename `streamlit_app.py` → `app.py`
- [ ] Update imports in `app.py` (e.g., `from src.controllers...`)
- [ ] Ensure `auth.py` imports are correct

### Phase 4: Fix Import Paths
- [ ] Update imports in `src/controllers/*.py`
- [ ] Update imports in `src/models/*.py`
- [ ] Update imports in `src/utils/*.py`
- [ ] Update imports in `pages/*.py`
- [ ] Update relative paths for CSV file access

### Phase 5: Testing & Cleanup
- [ ] Test: `streamlit run app.py`
- [ ] Verify all pages load correctly
- [ ] Verify data files are accessible
- [ ] Optional: Archive or remove old `views/`, `controllers/`, `models/`, `utils/` dirs

## 📚 Key Import Changes

**Example - Update in src files:**
```python
# Old
from models.student import Student

# New (absolute)
from src.models.student import Student

# New (relative - preferred in src/)
from ..models.student import Student
```

**Example - Update in page files:**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.controllers.grade_controller import GradeController
# Or use relative path adjustment
```

**Example - Update in app.py:**
```python
# Old
from auth import auth
from controllers.grade_controller import GradeController

# New
from auth import auth
from src.controllers.grade_controller import GradeController
```

## 🔍 File Path References

For accessing `data/` directory from different locations:
```python
from pathlib import Path

# From src/ files (2 levels up)
data_path = Path(__file__).resolve().parents[2] / "data"

# From pages/ files (2 levels up)
data_path = Path(__file__).resolve().parents[2] / "data"

# From root/app.py (1 level up)
data_path = Path(__file__).resolve().parent / "data"
```

## 💡 Streamlit Specifics

- Pages are automatically discovered in `pages/` directory
- Numeric prefix determines sidebar order: `1_`, `2_`, `3_`, `4_`
- `config.toml` in `.streamlit/` applies to the entire app
- Each page can have its own `st.set_page_config()` call
- Session state persists across pages automatically

---

**Reference:** See `RESTRUCTURING_GUIDE.md` for detailed migration instructions.
