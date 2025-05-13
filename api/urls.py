from django.urls import path
from . import views

urlpatterns = [
    path('devices/<str:device_id>/assign/', views.AssignDeviceView.as_view(), name='device-assign'),
    path('devices/<str:device_id>/unassign/', views.UnassignDeviceView.as_view(), name='device-unassign'),
    path('devices/<str:device_id>/location/', views.SendLocationView.as_view(), name='send-location'),
    path('devices/assignments/statuses/', views.DeviceAssignmentStatusListView.as_view(), name='device-assignment-statuses'),
    path('users/<int:user_id>/location/', views.GetUserLastLocationView.as_view(), name='user-last-location'),
    path('map/', views.MapView.as_view(), name='map'),
]
