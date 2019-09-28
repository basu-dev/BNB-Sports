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
    path("videos/",views.videos),
    path("add_video/<int:id>",views.add_video),
    path("edit_event/<int:id>",views.edit_event),
    path("delete_image/<int:id>",views.delete_photo),
    path("delete_video/<int:id>",views.delete_video),
    path("more_videos/<int:id>",views.more_videos)
]

