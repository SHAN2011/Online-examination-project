# TODO: Camera Output - Exam Monitoring Terms Only

## Plan
- [x] Read and understand `face_detection.py`, `take_exam.html`, `student_routes.py`
- [x] Update `face_detection.py` — remove emotion outputs, return only exam monitoring fields (`face_detected`, `confidence`, `monitoring_status`)
- [x] Update `templates/student/take_exam.html` — update `updateFaceStatus()` JS to show only exam monitoring terms on camera badge
- [x] Verify changes are consistent and test-ready
- [x] Fix `admin_routes.py` IntegrityError on user deletion (reassign exams, delete assignments/submissions)

## Expected Camera Badge Output
- Face present → `Normal` (green)
- Processing / grace period → `Checking...` (yellow)
- Face missing (3+ failures) → `Cheating` (red)
- Error → `Error` (yellow)

