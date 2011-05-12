# coding: utf-8
from django import forms 
from main.models import *

class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor

class ClassRoomTypeForm(forms.ModelForm):
    class Meta:
        model = ClassRoomType
