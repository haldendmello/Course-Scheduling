from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class classRooms(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=6)
    class_capacity = models.IntegerField(blank=True)

class Course(models.Model):

    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=20)
    checkgraduate = models.CharField(max_length=20, blank=True)


class Time(models.Model):

    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.CharField(max_length=20)


class coursesoffered(models.Model):

    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    coursePre = models.ForeignKey(Course, on_delete=models.CASCADE)
    studentEnrollment = models.IntegerField(blank=False)
    times = models.ManyToManyField(Time, blank=True)
