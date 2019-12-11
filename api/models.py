from django.db import models


class ComplaintState(models.Model):
    """This a model class which represents a complaint state"""

    DEFAULT_STATE_ID = 1
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"


class StrategicProcess(models.Model):
    """This a model class which represents a strategic process"""

    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"


class SubdivisionReponsible(models.Model):
    """This a model class which represents a subdivision responsible"""

    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"


class Complaint(models.Model):
    """This a model class which represents a general complaint"""

    #TODO title field
    folio = models.BigIntegerField(null=True, blank=True)
    compliant_state = models.ForeignKey('ComplaintState',
                                        default=ComplaintState.DEFAULT_STATE_ID,
                                        on_delete=models.CASCADE)
    complaint_content = models.TextField(null=False, blank=False)

    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=10,null=False, blank=False)

    received_date = models.DateField(auto_now=True)
    opening_date = models.DateField(null=True, blank=True)
    strategic_process = models.ForeignKey('StrategicProcess', null=True,
                                          blank=True,
                                          on_delete=models.CASCADE) # Select (6 options)
    subdivision_responsible = models.ForeignKey('SubdivisionReponsible',
                                                null=True, blank=True,
                                                on_delete=models.CASCADE) # Select (3 options)
    responsible_delivery_date = models.DateField(null=True, blank=True) # Manual
    responsible_response_date = models.DateField(null=True, blank=True) # Both manual and automatic
    complainer_response_date = models.DateField(null=True, blank=True) # Manual

    def __str__(self):
        return f"{self.name}'s general complaint"


class StudentComplaint(models.Model):
    """This a model class which represents a student complaint"""

    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE,
                                     related_name='student_complaint',
                                     primary_key= True)
    control_number = models.CharField(max_length=10, null=False, blank=False)
    career = models.CharField(max_length=50, null=False, blank=False)
    semester = models.CharField(max_length=2, null=False, blank=False)
    group = models.CharField(max_length=10, null=False, blank=False)
    turn = models.CharField(max_length=11, null=False, blank=False)
    classroom = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return f"{self.complaint.name}'s student complaint"


class StaffComplaint(models.Model):
    """This a model class which represents a staff complaint"""

    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE,
                                     related_name='staff_complaint',
                                     primary_key=True)
    rfc = models.CharField(max_length=13, null=False, blank=False)
    department = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.complaint.name}'s staff complaint"


class ExternalRelatedComplaint(models.Model):
    """This a model class which represents a external related complaint"""

    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE,
                                     related_name='external_related_complaint',
                                     primary_key=True)
    relation = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.complaint.name}'s external related complaint"
