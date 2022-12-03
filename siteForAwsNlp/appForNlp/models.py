from django.db import models

# Create your models here.

class Comment(models.Model):
    comment_text = models.CharField(max_length=1000)
    person_id = models.IntegerField(default=0) #comes in an ID format that the rasberry decides

class Analysis(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    comment_absa_result = models.CharField(max_length=1000)
    comment_sa_result = models.CharField(max_length=200)