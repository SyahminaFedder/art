from django.db import models


# Create your models here.
class Course(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    desc = models.TextField()
    
class Student(models.Model):
    sid = models.CharField(max_length=4, primary_key=True)
    sname = models.TextField()
    spass = models.CharField(max_length=10)
    gender = models.CharField(max_length=8)
    sphno = models.CharField(max_length=20)
    code = models.ForeignKey(Course, on_delete = models.CASCADE)

class Staff(models.Model):
    tid = models.CharField(max_length=4, primary_key=True)
    tname = models.TextField()
    tpass = models.CharField(max_length=10)
    role = models.TextField()
    tphno = models.CharField(max_length=20)

class Event(models.Model):
    eid = models.CharField(max_length=4, primary_key=True)
    ename = models.TextField()
    sdate = models.DateField()
    edate = models.DateField()
    tid = models.ForeignKey(Staff, on_delete = models.CASCADE)
    venue = models.TextField(default=None)

class Attendace(models.Model):
    aid = models.AutoField(primary_key=True, default=None)
    sid = models.ForeignKey(Student, on_delete = models.CASCADE)
    eid = models.ForeignKey(Event, on_delete = models.CASCADE)