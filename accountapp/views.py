from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from eventapp.models import People
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError


def team_profile(request, id):
    try:
        person = People.objects.get(id=id)

        return render(request, "team_profile.html", {"person": person})
    except:
        return redirect("/")


def newTeamMember(request):
    if request.method == "GET":
        return render(request, "new_team_member.html")

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        position = request.POST["position"]

        description = request.POST["description"]
        contact_no = request.POST["contact_no"]
        if request.FILES:
            image = request.FILES["image"]
        else:
            image = False
        person = People()
        person.first_name = first_name
        person.last_name = last_name
        person.position = position
        if contact_no:
            person.contact_no = contact_no
        if description:
            person.description = description
        if image:
            person.image = image

        person.save()
        return redirect("/")


class formerror:
    def __init__(self):
        self.username_error = ""
        self.password_error = ""
        self.name_error = ""


def signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    fe = formerror()
    ne = ""
    pe = ""
    ue = ""
    newuser = User()
    if request.method == "POST":
        newuser.username = request.POST["username"]
        newuser.password1 = request.POST["password1"]
        newuser.password2 = request.POST["password2"]
        newuser.first_name = request.POST["first_name"]
        newuser.last_name = request.POST["last_name"]
        validation = 1
        if newuser.password1 == newuser.password2:
            if len(newuser.password1) < 6:
                fe.password_error = "Password must be grater than 6 digits!"
                pe = "is-invalid"
                validation = 0

        else:
            fe.password_error = "Two password didnot match!"
            pe = "is-invalid"
            validation = 0
        try:
            user = User.objects.filter(username=newuser.username).get()
        except:
            user = 0
            ue = "is-valid"
        if user:
            fe.username_error = "User already exits!"
            validation = 0
            ue = "is-invalid"
        if newuser.first_name and newuser.last_name:
            v = 1
        else:
            validation = 0
            fe.name_error = "First and last name is required!"
            ne = "is-invalid"
        if validation:
            newuser.set_password(newuser.password1)
            newuser.save()
            return redirect("/login/")
        else:
            return render(
                request,
                "registration/signup.html",
                {
                    "page_title": "Signup",
                    "formerror": fe,
                    "username": ue,
                    "password": pe,
                    "first_name": ne,
                    "data": newuser,
                },
            )

    else:
        return render(
            request,
            "registration/signup.html",
            {"page_title": "signup", "formerror": fe},
        )


def login_view(request):
    fe = formerror()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/post/")
        else:
            fe.message = "Username/password error please provede correct credentials"
            return render(
                request,
                "registration/login.html",
                {"page_title": "Login", "formerror": fe},
            )
    else:
        return render(
            request, "registration/login.html", {"page_title": "Login", "formerror": fe}
        )

