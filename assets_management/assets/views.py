from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import timedelta

from .models import Assets, Notification, Violation
from .serializers import AssetsSerializer, NotificationSerializer, ViolationSerializer


class AssetsView(viewsets.ModelViewSet):
    queryset = Assets.objects.all()
    serializer_class = AssetsSerializer


class NotificationView(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class ViolationView(viewsets.ReadOnlyModelViewSet):
    queryset = Violation.objects.all()
    serializer_class = ViolationSerializer


@api_view(['GET'])
def run_chk(request):
    now = timezone.now()
    upcoming_time = now + timedelta(minutes=15)

    assets = Assets.objects.all()

    notifications_created = []
    violations_created = []

    for asset in assets:
       
        if asset.service_time and now <= asset.service_time <= upcoming_time:
            Notification.objects.create(
                assets=asset,
                notification_type='Service Reminder',
                messages=f"Service due for {asset.name} at {asset.service_time}"
            )
            notifications_created.append(f"{asset.name} (Service)")

        if asset.expire_time and now <= asset.expire_time <= upcoming_time:
            Notification.objects.create(
                assets=asset,
                notification_type='Expiry Reminder',
                messages=f"{asset.name} is expiring at {asset.expire_time}"
            )
            notifications_created.append(f"{asset.name} (Expiry)")

        if not asset.is_serviced and asset.service_time and now > asset.service_time:
            Violation.objects.create(
                assets=asset,
                violation_type='Service Missed',
                messages=f"Service was missed for {asset.name} at {asset.service_time}"
            )
            violations_created.append(f"{asset.name} (Service Missed)")


        if asset.expire_time and now > asset.expire_time:
            Violation.objects.create(
                assets=asset,
                violation_type='Expired Asset',
                messages=f"{asset.name} expired at {asset.expire_time}"
            )
            violations_created.append(f"{asset.name} (Expired)")

    return Response({
        "notifications_created": notifications_created,
        "violations_created": violations_created
    }, status=status.HTTP_200_OK)
