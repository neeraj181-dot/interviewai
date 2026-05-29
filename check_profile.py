import django, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'interviewai.settings'
django.setup()
from django.test import Client
c = Client()
c.post('/login/', {'username':'admin','password':'admin123'})
r = c.get('/profile/')
print('Profile status:', r.status_code)
content = r.content.decode('utf-8')
checks = [
    ('Resume Analyzer AI', 'AI card header'),
    ('resumeDropZone', 'Drop zone element'),
    ('resumeFileCard', 'File card element'),
    ('atsCircle', 'ATS ring SVG'),
    ('atsScoreVal', 'ATS score value'),
    ('upload-progress-bar', 'Progress bar'),
    ('triggerAnalysis', 'Analyze button JS'),
    ('removeResumeBtn', 'Remove button'),
    ('ATS Readiness Score', 'Benefits list'),
    ('Skill Analysis', 'Skill analysis section'),
    ('AI Recommendations', 'Recommendations section'),
    ('color-swatch', 'Color picker'),
    ('avatarInput', 'Avatar input'),
    ('resumeInput', 'Resume input'),
    ('interview_prep', 'Interview prep link'),
]
all_ok = True
for text, label in checks:
    found = text in content
    if not found:
        all_ok = False
    status = 'OK     ' if found else 'MISSING'
    print(f'  {status}  {label}')
print()
print('All checks passed!' if all_ok else 'SOME CHECKS FAILED')
