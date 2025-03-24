from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from datetime import time

# ✅ Generic Availability Model
class GenericAvailability(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey('content_type', 'object_id')
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(default=time(0, 0))
    end_time = models.TimeField(default=time(23, 59))
    slot_duration = models.PositiveIntegerField(default=30)
    weekly_offs = models.JSONField(default=list, blank=True)
    break1_start = models.TimeField(null=True, blank=True)
    break1_end = models.TimeField(null=True, blank=True)
    break2_start = models.TimeField(null=True, blank=True)
    break2_end = models.TimeField(null=True, blank=True)
    break3_start = models.TimeField(null=True, blank=True)
    break3_end = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Availability for {self.entity} from {self.start_date} to {self.end_date}"

# ✅ Generic Appointment Slot Model
class GenericAppointmentSlot(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey('content_type', 'object_id')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Slot for {self.entity} on {self.date} ({self.start_time} - {self.end_time})"

# ✅ Generic Appointment Model
class GenericAppointment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey('content_type', 'object_id')
    slot = models.ForeignKey(GenericAppointmentSlot, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    booked_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.entity} on {self.slot.date} ({self.slot.start_time} - {self.slot.end_time})"
