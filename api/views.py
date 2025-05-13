from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import AssignDeviceSerializer, LocationPingSerializer, LocationSerializer, \
    UnassignDeviceSerializer, DeviceAssignmentStatusSerializer
from devices.models import Device, DeviceAssignment

User = get_user_model()


class AssignDeviceView(APIView):
    def post(self, request, device_id):
        device = get_object_or_404(Device, device_id=device_id)

        serializer = AssignDeviceSerializer(data=request.data, context={'device': device})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnassignDeviceView(APIView):
    def put(self, request, device_id):
        device = get_object_or_404(Device, device_id=device_id)

        assignment = DeviceAssignment.objects.filter(device=device, unassigned_at__isnull=True).first()
        if not assignment:
            return Response({"detail": "This device is not currently assigned to anyone."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = UnassignDeviceSerializer(instance=assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Device unassigned successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendLocationView(APIView):
    def post(self, request, device_id):
        device = get_object_or_404(Device, device_id=device_id)

        if not device.is_assigned():
            return Response(
                {"detail": "Device is currently not assigned to any user and can't accept location pings."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = LocationPingSerializer(data=request.data, context={'device': device})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserLastLocationView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        assignment = DeviceAssignment.objects.filter(user=user, unassigned_at__isnull=True).first()
        if not assignment:
            return Response(
                {"detail": "This user currently has no device assigned."},
                status=status.HTTP_404_NOT_FOUND
            )

        device = assignment.device
        last_location = device.get_last_location()

        if not last_location or last_location.timestamp < assignment.assigned_at:
            return Response(
                {"detail": "No location data has been received for this user yet."},
                status=status.HTTP_204_NO_CONTENT
            )

        serializer = LocationSerializer(last_location)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MapView(APIView):
    def get(self, request):
        assignments = (
            DeviceAssignment.objects
            .filter(unassigned_at__isnull=True)
            .select_related('user', 'device')
        )

        device_type = request.GET.get('device_type')
        if device_type:
            assignments = assignments.filter(device__device_type=device_type)

        response_data = []

        for assignment in assignments:
            device = assignment.device
            last_location = device.get_last_location()

            if last_location and last_location.timestamp > assignment.assigned_at:
                response_data.append({
                    "user": {
                        "id": assignment.user.id,
                        "name": assignment.user.username
                    },
                    "device_id": device.device_id,
                    "latitude": last_location.latitude,
                    "longitude": last_location.longitude,
                    "timestamp": last_location.timestamp
                })

        return Response(response_data, status=status.HTTP_200_OK)


class DeviceAssignmentStatusListView(APIView):
    def get(self, request):
        devices = Device.objects.all()
        serializer = DeviceAssignmentStatusSerializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
