from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from .models import GenericAvailability, GenericAppointmentSlot, GenericAppointment
from .serializers import GenericAvailabilitySerializer, GenericAppointmentSlotSerializer, GenericAppointmentSerializer
from datetime import timedelta, datetime

# ✅ Set Generic Availability View
class SetGenericAvailabilityView(APIView):
    def post(self, request, entity_name, entity_id):
        content_type = ContentType.objects.get(model=entity_name)

        # ✅ Add content_type and object_id to the data before validation
        data = request.data.copy()
        data['content_type'] = content_type.id
        data['object_id'] = entity_id

        serializer = GenericAvailabilitySerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        slot_duration = data.get("slot_duration")
        weekly_offs = data.get("weekly_offs", []) or []
        is_off = "Off" in [off.title() for off in weekly_offs]

        # ✅ Handle "Off" Case
        if is_off:
            print(f"🛑 Marking entire range {start_date} to {end_date} as 'Off'")
            GenericAppointmentSlot.objects.filter(
                content_type=content_type, object_id=entity_id,
                date__gte=start_date, date__lte=end_date
            ).delete()

            GenericAvailability.objects.create(
                content_type=content_type,
                object_id=entity_id,
                start_date=start_date,
                end_date=end_date,
                start_time=start_time,
                end_time=end_time,
                slot_duration=slot_duration,
                weekly_offs=weekly_offs,
            )
            return Response({"message": f"Marked as 'Off' from {start_date} to {end_date}."}, status=200)

        # ✅ Delete old slots
        GenericAppointmentSlot.objects.filter(
            content_type=content_type, object_id=entity_id,
            date__gte=start_date, date__lte=end_date
        ).delete()

        # ✅ Create new availability record
        new_availability = GenericAvailability.objects.create(
            content_type=content_type,
            object_id=entity_id,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time,
            slot_duration=slot_duration,
            weekly_offs=weekly_offs,
        )
        print(f"Updated availability: {new_availability}")

        # ✅ Generate Slots After Updating Availability
        auto_generate_slots = GenerateSlotsView()
        auto_generate_slots.post(request, entity_name, entity_id)

        return Response({"message": f"Updated schedule from {start_date} to {end_date}."}, status=200)


# ✅ Generate Slots View
class GenerateSlotsView(APIView):
    def post(self, request, entity_name, entity_id):
        content_type = ContentType.objects.get(model=entity_name)
        availability = GenericAvailability.objects.filter(
            content_type=content_type, object_id=entity_id
        ).first()

        if not availability:
            return Response({"error": "Availability not found"}, status=404)

        # Clear existing slots
        GenericAppointmentSlot.objects.filter(
            content_type=content_type, object_id=entity_id
        ).delete()

        # Generate new slots
        slots = []
        current_date = availability.start_date
        while current_date <= availability.end_date:
            if current_date.strftime("%A") not in availability.weekly_offs:
                current_time = availability.start_time
                while current_time < availability.end_time:
                    end_time = (datetime.combine(current_date, current_time) + timedelta(minutes=availability.slot_duration)).time()
                    if end_time > availability.end_time:
                        break
                    slots.append(GenericAppointmentSlot(
                        content_type=content_type,
                        object_id=entity_id,
                        date=current_date,
                        start_time=current_time,
                        end_time=end_time,
                    ))
                    current_time = end_time

            current_date += timedelta(days=1)

        # Bulk create slots
        GenericAppointmentSlot.objects.bulk_create(slots)
        return Response({"message": f"Slots generated for {entity_name} ID {entity_id}."}, status=201)

# ✅ Book Appointment View
class BookAppointmentView(APIView):
    def post(self, request, entity_name, entity_id, slot_id):
        content_type = ContentType.objects.get(model=entity_name)
        slot = GenericAppointmentSlot.objects.get(id=slot_id)

        if slot.is_booked:
            return Response({"error": "Slot already booked"}, status=400)

        data = request.data
        appointment = GenericAppointment.objects.create(
            content_type=content_type,
            object_id=entity_id,
            slot=slot,
            patient_name=data.get("patient_name"),
            booked_by=data.get("booked_by")
        )

        slot.is_booked = True
        slot.save()

        serializer = GenericAppointmentSerializer(appointment)
        return Response(serializer.data, status=201)

# ✅ Cancel Appointment View
class CancelAppointmentView(APIView):
    def delete(self, request, entity_name, entity_id, slot_id):
        content_type = ContentType.objects.get(model=entity_name)
        appointment = GenericAppointment.objects.get(
            content_type=content_type, object_id=entity_id, slot_id=slot_id
        )
        slot = appointment.slot
        slot.is_booked = False
        slot.save()
        appointment.delete()

        return Response({"message": "Appointment canceled successfully"}, status=200)
