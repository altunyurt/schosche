# coding: utf-8
from django import forms 
from main.models import *

class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom

class CourseTypeForm(forms.ModelForm):
    class Meta:
        model = CourseType

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course

class LecturerForm(forms.ModelForm):
    class Meta:
        model = Lecturer

class ClassRoomTypeForm(forms.ModelForm):
    class Meta:
        model = ClassRoomType
