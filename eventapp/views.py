from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.core.files.storage import FileSystemStorage
from accountapp.models import About
from django.http import Http404, JsonResponse

from django.contrib import messages
from .models import *
import json

from eventapp import models
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ImageForm, PostForm, Personimageform
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.templatetags.static import static
from django.views import generic


def edit_event(request, id):
    if request.method == "POST":
        if request.user.is_authenticated:
            date = request.POST["date"]
            title = request.POST["title"]
            description = request.POST["description"]
            event = Postevent.objects.get(id=id)
            try:
                completed = request.POST["completed"]
                event.completed = True
            except:
                event.completed = False
            if title:
                event.title = title
            if date:
                event.date = date
            if description:
                event.description = description
            event.save()
            return redirect("/")
    elif request.method == "GET":
        try:
            event = event = models.Postevent.objects.get(id=id)
            if event.completed:
                event.checked = "checked"
            else:
                event.checked = "unchecked"
        except:
            return redirect("/")

        return render(request, "edit_event.html", {"event": event})


def add_video(request, id):
    if request.method == "POST":
        if request.user.is_authenticated:
            post = models.Postevent.objects.get(id=id)
            title = request.POST["video_title"]
            url = request.POST["video_url"]
            if title and url:
                video = Videos()
                video.title = title
                video.url = url
                video.save()
                return redirect("/admin_page")

    elif request.method == "GET":
        return render(request, "video_add.html", {"id": id})
    return redirect("/")


def index(request):
    events = models.Postevent.objects.order_by("-created_date")
    images = []
    for event in events:
        event.images = models.Images.objects.all().order_by("-id")
        break
    return render(request, "gallery.html", {"events": events})


@login_required
def post(request):

    ImageFormSet = modelformset_factory(models.Images, form=ImageForm, extra=10)
    #'extra' means the number of photos that you can upload   ^
    if request.method == "POST":
        postForm = PostForm(request.POST)
        formset = ImageFormSet(
            request.POST, request.FILES, queryset=models.Images.objects.none()
        )

        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()
            id = str(post_form.id)
            for form in formset.cleaned_data:

                if form:
                    image = form["image"]
                    photo = models.Images(post=post_form, image=image)
                    photo.save()
            messages.success(request, "Go to homepage to see changes")
            return redirect("/add_video/"+id)
        else:
            print(postForm.errors, formset.errors)
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=models.Images.objects.none())
    return render(
        request, "gallery/eventbase.html", {"postForm": postForm, "formset": formset}
    )


def memberimage(request):
    if request.method == "POST":
        form = Personimageform(request.POST, request.FILES)
        if form.is_valid():
            imagestored = models.People()
            imagestored.image = form.cleaned_data["personimage"]
            imagestored.save()
    else:
        form = Personimageform()

    return render(request, "postimage.html", locals())


def homePage(request):
    videos = models.Videos.objects.all().order_by("-id")[:3]
    try:
        about = About.objects.all().order_by("-id")[0]
    except:
        about = About()
        about.body = "This is about page"

    people = People.objects.all()
    upcoming_events = models.Postevent.objects.filter(completed=False).order_by(
        "-created_date"
    )[:4]
    for event in upcoming_events:
        event.images = models.Images.objects.filter(post=event)[:1]
        try:
            memberobjs = models.Members.objects.filter(post=event)
            for memberobj in memberobjs:
                event.person = models.People.objects.get(id=memberobj.person.id)
        except:
            pass
    completed_events = models.Postevent.objects.filter(completed=True).order_by(
        "-created_date"
    )[:4]
    for event in completed_events:
        event.images = models.Images.objects.filter(post=event)[:1]
        try:
            memberobjs = models.Members.objects.filter(post=event)
            for memberobj in memberobjs:
                event.person = models.People.objects.get(id=memberobj.person.id)
        except:
            pass
    return render(
        request,
        "home.html",
        {
            "team": people,
            "upcoming_events": upcoming_events,
            "completed_events": completed_events,
            "videos": videos,
            "about": about,
        },
    )


def event_detail(request, id):
    try:
        eventdetail = models.Postevent.objects.get(id=id)

        eventdetail.images = models.Images.objects.filter(post=eventdetail)
    except:
        eventdetail = []
    return render(request, "event_detail.html", {"event": eventdetail})


def upcoming_events(request):
    more = False
    ids = []
    events = models.Postevent.objects.filter(completed=False).order_by("-created_date")[
        :10
    ]
    count = events.count()
    if count == 10:
        more = True
    for i in events:
        ids.append(i.id)
        i.reduceddescription = i.description[:100]
        i.images = models.Images.objects.filter(post=i)
    if len(ids):
        ids.sort()
        smallest_id = ids[0]
    else:
        smallest_id = 0
    return render(
        request,
        "events.html",
        {"events": events, "smallest_id": smallest_id, "completed": "u", "more": more},
    )


def completed_events(request):
    more = False
    ids = []
    events = models.Postevent.objects.filter(completed=True).order_by("-created_date")[
        :10
    ]
    count = events.count()
    if count == 10:
        more = True
    for i in events:
        ids.append(i.id)
        i.reduceddescription = i.description[:100]
        i.images = models.Images.objects.filter(post=i)
    if len(ids):
        ids.sort()
        smallest_id = ids[0]
    else:
        smallest_id = 0
    return render(
        request,
        "events.html",
        {"events": events, "smallest_id": smallest_id, "completed": "c", "more": more},
    )


def more_events(request, c, id):
    ids = []
    more = False
    if c == "c":
        try:
            events = (
                Postevent.objects.filter(id__lte=id)
                .filter(completed=True)
                .order_by("-created_date")[:10]
            )
            count = events.count()
            if count == 10:
                more = True
            for i in events:
                ids.append(i.id)
                i.reduceddescription = i.description[:100]
                i.images = models.Images.objects.filter(post=i)
            if len(ids):
                ids.sort()
                smallest_id = ids[0]
            else:
                smallest_id = 0
        except:
            events = []

        return render(
            request,
            "events.html",
            {
                "events": events,
                "smallest_id": smallest_id,
                "completed": "c",
                "more": more,
            },
        )
    elif c == "u":

        events = (
            Postevent.objects.filter(id__lte=id)
            .filter(completed=False)
            .order_by("-created_date")[:10]
        )
        count = events.count()
        if count == 10:
            more = True

        for i in events:
            ids.append(i.id)
            i.reduceddescription = i.description[:100]
            i.images = models.Images.objects.filter(post=i)
        if len(ids):
            ids.sort()
            smallest_id = ids[0]
        else:
            smallest_id = 0
        return render(
            request,
            "events.html",
            {
                "events": events,
                "smallest_id": smallest_id,
                "completed": "c",
                "more": more,
            },
        )
    else:
        return redirect("/")


@login_required
def deletepost(request, id):
    deleted = models.Postevent.objects.get(id=id)
    deleted.delete()
    return redirect("/")


def videos(request):
    if request.method == "GET":
        more = False
        ids = []
        videos = models.Videos.objects.all().order_by("-id")[:10]
        for video in videos:
            ids.append(video.id)
        count = videos.count()
        if count == 10:
            more = True

        if len(ids):
            ids.sort()
            smallest_id = ids[0]
        else:
            smallest_id = 0
        return render(
            request,
            "videos.html",
            {"videos": videos, "smallest_id": smallest_id, "more": more},
        )
  

    elif request.method == "POST":
        if request.user.is_authenticated:
            title = request.POST["video_title"]
            url = request.POST["video_url"]
            video = models.Videos()
            if title:
                video.title = title
                if url:
                    link_id = []
                    index = 0
                    for i in url:
                        index += 1
                        if i == "=":
                            link_id = url[index : len(url)]
                            video.url = link_id
                            video.save()
                            break

                    return redirect("/")

        else:
            return HttpResponse("There was an error.. Try again!!!")
        return redirect("/")
def more_videos(request, id):
    more = False
    videos=models.Videos.objects.filter(id__lteid).order_by("-id")[:10]
    for video in videos:
        ids.append(video.id)
    count = videos.count()
    if count == 10:
        more = True

    if len(ids):
        ids.sort()
        smallest_id = ids[0]
    else:
        smallest_id = 0
    return render(
        request,
        "videos.html",
        {"videos": videos, "smallest_id": smallest_id, "more": more},
    )


@login_required
def add_members(request, id):
    people = models.People.objects.all()
    try:
        event = models.Postevent.objects.get(id=id)
        for person in people:
            try:
                member = models.Members.objects.filter(event=event).get(person=person)
                if member:
                    person.truth = True
            except:
                person.truth = False
    except:
        return redirect("/")
    return render(request, "gallery/add_members.html", {"people": people, "pid": id})


@login_required
def add_member(request, pid, mid):
    if request.method == "POST":
        try:
            event = models.Postevent.objects.get(id=pid)
            try:
                person = models.People.objects.get(id=mid)
                try:

                    member = models.Members.objects.filter(person=person).get(
                        event=event
                    )
                    if member:
                        member.delete()
                        truth = "false"
                        return JsonResponse({"data": truth})
                except:

                    nmember = models.Members()
                    nmember.person = person
                    nmember.event = event
                    nmember.save()

                    return JsonResponse({"data": "true"})
            except:
                return redirect("/")
        except:
            return redirect("/")


@login_required
def delete_photo(request, id):
    if request.method == "POST":
        url = request.POST["url"]
        if request.user.is_authenticated:
            try:
                photo = Images.objects.get(id=id)

                photo.delete()

                return redirect(url)
            except:

                return redirect(url)
    return redirect("/")


def delete_video(request, id):
    if request.method == "POST":
        url = request.POST["url"]
        if request.user.is_authenticated:
            try:
                photo = Videos.objects.get(id=id)
                photo.delete()
                return redirect(url)
            except:
                return redirect(url)
    return redirect("/")
