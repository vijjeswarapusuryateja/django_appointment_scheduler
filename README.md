# Appointment Scheduler

**Appointment Scheduler** is a generic and flexible appointment scheduling package for Django applications. It is designed to work with any model (e.g., doctor, room, equipment) and provides a robust and efficient way to manage availability, slots, and appointments.

---

## Features
- **Generic and Flexible:** Works with any Django model using GenericForeignKey.
- **Advanced Slot Management:** Create, update, and delete slots dynamically.
- **Robust Booking System:** Book and cancel appointments seamlessly.
- **Efficient Slot Generation:** Automatically generate slots based on availability and slot duration.
- **Customizable Weekly Offs:** Configure off days and handle "Off" periods.
- **Conflict Resolution:** Prevents overlapping slots and handles cancellations gracefully.

---

## Installation

You can install the package using pip:

```bash
pip install appointment-scheduler
