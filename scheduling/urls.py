from django.urls import path
from . import views

urlpatterns=[
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("", views.index, name="index"),
    path("addDetails", views.addDetails, name="addDetails"),
    path("coursesOffered", views.coursesOffered, name="coursesOffered"),
    path("addClassroom", views.addClassRoom, name="addClassroom"),
    path("addCoures", views.addCourses, name="addCoures"),
    path("timeSlots", views.addTimeSlots, name="timeSlots"),
    path("schedule", views.schedule, name="schedule"),
    path("removetime/<str:itemid>", views.removeTime, name="removetime"),
    path("removecourses/<str:itemid>", views.removeCourses, name="removcourses"),
    path("removeclasses/<str:itemid>", views.removeClasses, name="removeclasses"),
    path("removecoursesoffered/<str:itemid>", views.removeCoursesOffered, name="removecoursesoffered"),
    
]