from turtle import title
from django.http import HttpResponseRedirect
from django.shortcuts import render
from first_app.models import Degree, Student
from .forms import DegreeForm, StudentForm, SearchForm
import json
from django.db.models import Q

# import
# Create your views here.

degree_values = Degree.objects.all()
student_values = Student.objects.all()


# def index(request):
#     # global student_values
#     my_dict = {"degree_rows": degree_values, "student_values": student_values}
#     return render(request, "index.html", context=my_dict)


# def forms(request):
#     return render(request, "forms.html")


def index(request):
    global student_values
    # search_name = request.GET.get("search_name")
    # form = SearchForm()
    form = SearchForm()
    my_dict = {
        "degree_rows": degree_values,
        "student_values": student_values,
        "search_form": form,
    }
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            fromdate = form.cleaned_data["dateFrom"]
            todate = form.cleaned_data["dateTo"]
            sort = form.cleaned_data["sort"]

            print(fromdate, todate, name, sort)
            if fromdate and todate:
                student_values = Student.objects.filter(
                    Q(name__icontains=name) & Q(dob__range=(fromdate, todate))
                )
            else:
                student_values = Student.objects.filter(Q(name__icontains=name))
            if sort:
                print("HI")
                student_values = student_values.order_by("name")

        my_dict["student_values"] = student_values
        return render(request, "index.html", context=my_dict)
    # if search_name:
    #     student_values = Student.objects.filter(Q(name__icontains=search_name))
    else:
        return render(request, "index.html", context=my_dict)


def get_degree(request):
    data = ""
    if request.method == "POST":
        form = DegreeForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            branch = form.cleaned_data["branch"]
            print(title, branch)

            d = Degree(title=title, branch=branch)
            d.save()

            f = request.FILES.get("file")
            if f:
                data = json.load(f)
                for deg in data["degree"]:
                    t = deg["title"]
                    b = deg["branch"]
                    d1 = Degree(title=t, branch=b)
                    d1.save()

            return HttpResponseRedirect("/forms/")
    else:
        form = DegreeForm()
        return render(request, "forms.html", {"degree_form": form})


def get_student(request):
    data = ""
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        # print("Hi")
        if form.is_valid():
            roll = form.cleaned_data["roll_number"]
            name = form.cleaned_data["name"]
            year = form.cleaned_data["year"]
            dob = form.cleaned_data["dob"]
            degree = form.cleaned_data["degree"]

            print(roll, name)

            s = Student(roll_number=roll, name=name, year=year, dob=dob, degree=degree)
            s.save()

            f = request.FILES.get("file")
            if f:
                data = json.load(f)
                for st in data["student"]:
                    r = st["roll_number"]
                    n = st["name"]
                    y = st["year"]
                    dob = st["dob"]
                    deg = st["degree"]
                    # d1 = Degree(title=deg[0]["title"], branch=deg[0]["branch"])
                    degree = Degree.objects.get(branch=deg[0]["branch"])
                    s1 = Student(roll_number=r, name=n, year=y, dob=dob, degree=degree)
                    s1.save()

            return HttpResponseRedirect("/student/")

    else:
        form = StudentForm()
        return render(request, "student.html", {"student_form": form})
