from django.contrib import admin

from .models import Examiner, Examiner_score

class ExaminerAdmin(admin.ModelAdmin):
    pass
    # readonly_fields = ["name", "email", "exam_id"]

class Examiner_scoreAdmin(admin.ModelAdmin):
    readonly_fields = ["user", "score", "datetime_created", "hashed"]

admin.site.register(Examiner, ExaminerAdmin)
admin.site.register(Examiner_score, Examiner_scoreAdmin)
