from django.db import models


class Quiz(models.Model):
    question_one = models.CharField(max_length=50)
    question_two = models.CharField(max_length=50)
    question_three = models.CharField(max_length=50)
    question_four = models.CharField(max_length=50)
    question_five = models.CharField(max_length=50)
    question_six = models.CharField(max_length=50)
    question_seven = models.CharField(max_length=50)
    question_eight = models.CharField(max_length=50)
    question_nine = models.CharField(max_length=50)
    question_ten = models.CharField(max_length=50)
    owner = models.ForeignKey(
        "jwt_auth.User", related_name="quiz", on_delete=models.CASCADE)
