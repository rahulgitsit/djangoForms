from cProfile import label
from tkinter.tix import Select
from django import forms
from first_app.models import Degree
import datetime


class DegreeForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=20,
    )
    branch = forms.CharField(label="Branch", max_length=50)
    file = forms.FileField(
        label="Select a JSON file", help_text="Max. 2 MB", required=False
    )


class StudentForm(forms.Form):
    roll_number = forms.CharField(label="Roll Number", max_length=20)
    name = forms.CharField(label="Name", max_length=50)
    year = forms.IntegerField(label="Year")
    dob = forms.DateField(label="Date of Birth")
    degree = forms.ModelChoiceField(queryset=Degree.objects.all())
    file = forms.FileField(
        label="Select a JSON file",
        help_text="Max. 2 MB",
        required=False,
    )


class SearchForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50, required=False)
    dateFrom = forms.DateField(
        label="From", required=False, initial=(datetime.date.min)
    )
    dateTo = forms.DateField(label="To", required=False, initial=datetime.date.today)
    sort = forms.BooleanField(label="Sort", required=False)
    # start_date = forms.DateField(
    #     widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    #     lookup_expr="gt",
    #     label="From",
    # )
    # end_date = forms.DateFilter(
    #     widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    #     lookup_expr="lt",
    #     label="To",
    # )
