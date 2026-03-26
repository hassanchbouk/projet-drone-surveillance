from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("sites/", views.site_list, name="site_list"),
    path("missions/", views.mission_list, name="mission_list"),
    path("missions/<int:mission_id>/", views.mission_detail, name="mission_detail"),
    path("missions/create-demo/", views.create_demo_mission, name="create_demo_mission"),
    path("missions/<int:mission_id>/launch/", views.launch_mission, name="launch_mission"),
    path("missions/<int:mission_id>/advance/", views.advance_mission, name="advance_mission"),
]