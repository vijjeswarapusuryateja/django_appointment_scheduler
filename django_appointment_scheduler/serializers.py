from rest_framework import serializers
from .models import GenericAvailability, GenericAppointmentSlot, GenericAppointment

# ✅ Generic Availability Serializer
class GenericAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericAvailability
        fields = '__all__'

    def validate(self, data):
        # Validate time range
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be earlier than end time.")

        # Validate break times if provided
        breaks = [
            ('break1_start', 'break1_end'),
            ('break2_start', 'break2_end'),
            ('break3_start', 'break3_end')
        ]
        for start, end in breaks:
            if data.get(start) and data.get(end):
                if data[start] >= data[end]:
                    raise serializers.ValidationError(f"{start.replace('_', ' ').title()} must be earlier than {end.replace('_', ' ').title()}.")

        # Validate slot duration
        if data['slot_duration'] <= 0:
            raise serializers.ValidationError("Slot duration must be a positive integer.")

        return data

# ✅ Generic Appointment Slot Serializer
class GenericAppointmentSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericAppointmentSlot
        fields = '__all__'

    def validate(self, data):
        # Ensure start time is earlier than end time
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be earlier than end time.")
        return data

# ✅ Generic Appointment Serializer
class GenericAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericAppointment
        fields = '__all__'

    def validate(self, data):
        # Check if the slot is already booked
        slot = data.get('slot')
        if slot and slot.is_booked:
            raise serializers.ValidationError("This slot is already booked.")

        # Check if the entity exists
        if not slot:
            raise serializers.ValidationError("Invalid slot or entity not found.")

        return data
