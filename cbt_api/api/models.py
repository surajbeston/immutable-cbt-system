from django.db import models

class Examiner(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField(unique = True)
    exam_id = models.CharField(max_length = 100)
    exam_taken = models.BooleanField(default = False)
    datetime_created = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class Examiner_score(models.Model):
    user = models.ForeignKey(Examiner, on_delete = models.CASCADE)
    score = models.FloatField()
    datetime_created = models.DateTimeField(auto_now = True)
    hashed = models.CharField(max_length = 100)

    def __str__(self):
        return self.user.name
