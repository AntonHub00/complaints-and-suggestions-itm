from django.contrib import admin
from .models import (ComplaintState, StrategicProcess, SubdivisionReponsible,
                     Complaint, StudentComplaint, StaffComplaint,
                     ExternalRelatedComplaint)

admin.site.register(ComplaintState)
admin.site.register(StrategicProcess)
admin.site.register(SubdivisionReponsible)
admin.site.register(Complaint)
admin.site.register(StudentComplaint)
admin.site.register(StaffComplaint)
admin.site.register(ExternalRelatedComplaint)
