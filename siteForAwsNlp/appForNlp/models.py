from django.db import models

# Create your models here.

class Comment(models.Model):
    comment_text = models.CharField(max_length=1000)
    person_id = models.CharField(max_length=2000, default=0) #comes in an ID format that the rasberry decides
    comment_day = models.CharField(max_length=1000, default = '0')
    comment_month = models.CharField(max_length=1000, default = '0')
    comment_year = models.CharField(max_length=1000, default = '0')

class Analysis(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    comment_absa_result = models.CharField(max_length=1000)
    comment_sa_result = models.CharField(max_length=200)