from django.urls import path
from .views import (
    SetGenericAvailabilityView,
    GenerateSlotsView,
    BookAppointmentView,
    CancelAppointmentView,
)

urlpatterns = [
    # Set or update availability for a given entity
    path('<str:entity_name>/<int:entity_id>/set-availability/', SetGenericAvailabilityView.as_view(), name='set-availability'),
    
    # Generate slots for a given entity
    path('<str:entity_name>/<int:entity_id>/generate-slots/', GenerateSlotsView.as_view(), name='generate-slots'),
    
    # Book an appointment for a specific slot
    path('<str:entity_name>/<int:entity_id>/book-appointment/<int:slot_id>/', BookAppointmentView.as_view(), name='book-appointment'),
    
    # Cancel an appointment for a specific slot
    path('<str:entity_name>/<int:entity_id>/cancel-appointment/<int:slot_id>/', CancelAppointmentView.as_view(), name='cancel-appointment'),
]
