from django.contrib import admin
from.models import Course, Student, Staff, Event, Attendace

# Register your models here.
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Event)
admin.site.register(Attendace)