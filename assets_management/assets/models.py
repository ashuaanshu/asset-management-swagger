from django.db import models

class Assets(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    service_time = models.DateTimeField()
    expire_time = models.DateTimeField()
    is_serviced = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    assets = models.ForeignKey('Assets', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=100)
    messages = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assets.name} - {self.notification_type}"


class Violation(models.Model):
    assets = models.ForeignKey('Assets', on_delete=models.CASCADE)
    violation_type = models.CharField(max_length=100)
    messages = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assets.name} - {self.violation_type}"
