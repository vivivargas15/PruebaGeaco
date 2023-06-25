from django.db import models

# Create your models here.


class Document(models.Model):
	item=models.IntegerField()
	title=models.CharField(max_length=20)
	uploadedFile=models.FileField(upload_to= "Uploaded Files/")
	dateTimeOfUpload= models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.title

