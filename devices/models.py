from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Device(models.Model):
    A = 'a'
    B = 'b'
    C = 'c'

    DEVICE_TYPE_CHOICES = [
        (A, 'A'),
        (B, 'B'),
        (C, 'C'),
    ]

    device_id = models.CharField(max_length=50)
    device_type = models.CharField(max_length=2, choices=DEVICE_TYPE_CHOICES)

    def __str__(self):
        return f"Device {self.device_id} (type: {self.get_device_type_display()})"

    def is_assigned(self):
        return DeviceAssignment.objects.filter(device=self, unassigned_at__isnull=True).exists()

    def get_last_location(self):
        return self.location_set.order_by('-timestamp').first()


class DeviceAssignment(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="assignments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignments")
    assigned_at = models.DateTimeField(auto_now_add=True)
    unassigned_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        description = f"Device {self.device.pk} assigned to user {self.user.username} at {self.assigned_at}"
        if self.unassigned_at:
            description += f", unassigned at {self.unassigned_at}"
        return description

    def unassign(self):
        if not self.unassigned_at:
            self.unassigned_at = timezone.now()
            self.save()
        

class Location(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Location at ({self.latitude}, {self.longitude}) on {self.timestamp}"
