from django.db import models

# Create your models here.
class joboffer (models.Model):
    job_position = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    company_name= models.CharField(max_length=250)
    date_posted= models.CharField(max_length=250)
    job_link= models.TextField()

    def __str__(self):
        return self.job_position
    
