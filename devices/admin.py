from django.contrib import admin

from devices.models import Location, Device, DeviceAssignment


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'device_type')


@admin.register(DeviceAssignment)
class DeviceAssignmentAdmin(admin.ModelAdmin):
    list_display = ('device', 'user', 'assigned_at', 'unassigned_at')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('device', 'latitude', 'longitude', 'timestamp')
