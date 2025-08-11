from django.db import models
from django.contrib.auth.models import User

# This assumes id is an integer in SQL Server
class GroundwaterPlace(models.Model):
    id = models.IntegerField(primary_key=True)  # Explicitly declare if you're managing this manually
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    district = models.CharField(max_length=100)
    name_hi = models.CharField(max_length=100, null=True, blank=True)
    district_hi = models.CharField(max_length=100, null=True, blank=True)


    class Meta:
        managed = False  # This table exists in SQL Server
        db_table = 'GroundwaterPlace'

class GroundwaterData(models.Model):
    place = models.ForeignKey(GroundwaterPlace, on_delete=models.CASCADE, db_column='place_id')
    parameter = models.CharField(max_length=100)
    value = models.FloatField()
    unit = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    sample_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'GroundwaterData'

class GroundwaterPDF(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='pdf_uploads/')

    def __str__(self):
        return f"PDF uploaded at {self.uploaded_at}"

    class Meta:
        managed = True

        # models.py
class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    place = models.ForeignKey(GroundwaterPlace, on_delete=models.SET_NULL, null=True)
    place_type = models.CharField(max_length=20, choices=[('village', 'Village'), ('town', 'Town')])

    def __str__(self):
        return f"{self.user.username} - {self.place_type} - {self.place.name if self.place else 'None'}"


