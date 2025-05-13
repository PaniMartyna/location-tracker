from django.contrib.auth import get_user_model
from rest_framework import serializers

from devices.models import DeviceAssignment, Location, Device

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class AssignDeviceSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')

    def create(self, validated_data):
        device = self.context['device']
        user = validated_data.get('user')

        if DeviceAssignment.objects.filter(device=device, unassigned_at__isnull=True).exists():
            assignment = DeviceAssignment.objects.get(device=device, unassigned_at__isnull=True)
            if assignment.user_id == user.id:
                return assignment
            else:
                assignment.unassign()

        return DeviceAssignment.objects.create(device=device, **validated_data)


class UnassignDeviceSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        instance.unassign()
        return instance


class DeviceAssignmentStatusSerializer(serializers.ModelSerializer):
    device_type = serializers.CharField(source='get_device_type_display')
    assigned = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ['device_id', 'device_type', 'assigned']

    def get_assigned(self, obj):
        return obj.is_assigned()


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude', 'timestamp']


class LastLocationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Location
        fields = ['user', 'device', 'latitude', 'longitude', 'timestamp']


class LocationPingSerializer(serializers.ModelSerializer):
    ping_time = serializers.DateTimeField(source='timestamp')

    class Meta:
        model = Location
        fields = ['latitude', 'longitude', 'ping_time']

    def create(self, validated_data):
        device = self.context['device']
        return Location.objects.create(device=device, **validated_data)




