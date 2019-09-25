from django.urls import path
from eventapp import views

app_name = "gallery"

urlpatterns = [
    path("gallery/", views.index, name="gallery"),
    path("post/", views.post, name="eventpost"),
    path("event_detail/<int:id>/", views.event_detail, name="eventdetail"),
    path("upcoming_events/", views.upcoming_events, name="upcoming"),
    path("", views.homePage),
    path("completedevents/", views.completed_events, name="completed"),
    path("delete/<int:id>/", views.deletepost, name="delete"),
    path("eventapp/add_members/<int:id>", views.add_members, name="addmember"),
    path("eventapp/add_member/<int:pid>/<int:mid>", views.add_member, name="addmember"),
    path("postimage/", views.memberimage),
    path("more_events/<str:c>/<int:id>/", views.more_events),
]

