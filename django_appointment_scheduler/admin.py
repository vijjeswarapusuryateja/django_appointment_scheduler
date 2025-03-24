from django.contrib import admin
from .models import GenericAvailability, GenericAppointmentSlot, GenericAppointment

# Register GenericAvailability model
class GenericAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('entity', 'start_date', 'end_date', 'start_time', 'end_time', 'slot_duration', 'weekly_offs')
    search_fields = ('entity__name', 'start_date', 'end_date')

# Register GenericAppointmentSlot model
class GenericAppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ('entity', 'date', 'start_time', 'end_time', 'is_booked')
    search_fields = ('entity__name', 'date')

# Register GenericAppointment model
class GenericAppointmentAdmin(admin.ModelAdmin):
    list_display = ('entity', 'customer_name', 'slot', 'booked_by', 'created_at')
    search_fields = ('customer_name', 'slot__date', 'entity__name')

# Register models with the admin panel
admin.site.register(GenericAvailability, GenericAvailabilityAdmin)
admin.site.register(GenericAppointmentSlot, GenericAppointmentSlotAdmin)
admin.site.register(GenericAppointment, GenericAppointmentAdmin)
