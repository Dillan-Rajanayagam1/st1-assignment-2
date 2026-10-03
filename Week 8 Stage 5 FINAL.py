import json
import os


# Domain Layer

class Patient:
    def __init__(self, patient_id, name, contact_details):
        if not name:
            raise ValueError("Patient name cannot be empty.")

        self.patient_id = patient_id
        self.name = name
        self.contact_details = contact_details

    def update_details(self, name, contact_details):
        if not name:
            raise ValueError("Patient name cannot be empty.")

        self.name = name
        self.contact_details = contact_details

    def get_details(self):
        return (
            f"Patient ID: {self.patient_id} | "
            f"Name: {self.name} | "
            f"Contact: {self.contact_details}"
        )


class Practitioner:
    def __init__(self, practitioner_id, name, speciality):
        if not name:
            raise ValueError("Practitioner name cannot be empty.")

        self.practitioner_id = practitioner_id
        self.name = name
        self.speciality = speciality

    def get_details(self):
        return (
            f"Practitioner ID: {self.practitioner_id} | "
            f"Name: {self.name} | "
            f"Speciality: {self.speciality}"
        )


class Appointment:
    def __init__(
        self,
        appointment_id,
        patient,
        practitioner,
        appointment_time,
        status="Booked"
    ):
        if not appointment_time:
            raise ValueError("Appointment time is required.")

        self.appointment_id = appointment_id
        self.patient = patient
        self.practitioner = practitioner
        self.appointment_time = appointment_time
        self.status = status

    def cancel(self):
        self.status = "Cancelled"

    def update_status(self, status):
        self.status = status

    def get_details(self):
        return (
            f"Appointment ID: {self.appointment_id} | "
            f"Patient: {self.patient.name} | "
            f"Practitioner: {self.practitioner.name} | "
            f"Time: {self.appointment_time} | "
            f"Status: {self.status}"
        )


# PERSISTENCE LAYER


class JsonStorage:
    def __init__(self, filename="appointments.json"):
        self.filename = filename

    def save(self, appointments):
        data = []

        for appointment in appointments:
            data.append({
                "appointment_id": appointment.appointment_id,
                "patient_id": appointment.patient.patient_id,
                "patient_name": appointment.patient.name,
                "patient_contact": appointment.patient.contact_details,
                "practitioner_id": appointment.practitioner.practitioner_id,
                "practitioner_name": appointment.practitioner.name,
                "practitioner_speciality": appointment.practitioner.speciality,
                "appointment_time": appointment.appointment_time,
                "status": appointment.status
            })

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def load(self):
        if not os.path.exists(self.filename):
            return []

        with open(self.filename, "r") as file:
            data = json.load(file)

        appointments = []

        for item in data:
            patient = Patient(
                item["patient_id"],
                item["patient_name"],
                item["patient_contact"]
            )

            practitioner = Practitioner(
                item["practitioner_id"],
                item["practitioner_name"],
                item["practitioner_speciality"]
            )

            appointment = Appointment(
                item["appointment_id"],
                patient,
                practitioner,
                item["appointment_time"],
                item["status"]
            )

            appointments.append(appointment)

        return appointments


# REPOSITORY LAYER

class AppointmentRepository:
    def __init__(self, storage):
        self.storage = storage

    def save(self, appointments):
        self.storage.save(appointments)

    def load(self):
        return self.storage.load()


# SERVICE LAYER

class AppointmentService:
    def __init__(self, repository):
        self.repository = repository
        self.appointments = repository.load()

    def book_appointment(self, appointment):
        # Prevent duplicate practitioner bookings
        for existing in self.appointments:
            if (
                existing.practitioner.practitioner_id
                == appointment.practitioner.practitioner_id
                and existing.appointment_time
                == appointment.appointment_time
                and existing.status != "Cancelled"
            ):
                raise ValueError(
                    "Practitioner is already booked at this time."
                )

        self.appointments.append(appointment)
        self.repository.save(self.appointments)

    def cancel_appointment(self, appointment_id):
        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                appointment.cancel()
                self.repository.save(self.appointments)
                return

        raise ValueError("Appointment not found.")

    def update_appointment_status(self, appointment_id, status):
        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                appointment.update_status(status)
                self.repository.save(self.appointments)
                return

        raise ValueError("Appointment not found.")

    def get_appointments(self):
        return self.appointments



# PRESENTATION LAYER


class ClinicApp:
    def __init__(self, appointment_service):
        self.appointment_service = appointment_service

    def display_appointments(self):
        appointments = self.appointment_service.get_appointments()

        if not appointments:
            print("No appointments found.")
            return

        for appointment in appointments:
            print(appointment.get_details())



# MAIN PROGRAM


print("Welcome to SmartCare: Community Clinic Appointment Booking System!")


# Create persistence and repository
storage = JsonStorage("appointments.json")
repository = AppointmentRepository(storage)

# Create service
appointment_service = AppointmentService(repository)

# Create presentation application
app = ClinicApp(appointment_service)


# Create patient
patient1 = Patient(
    "P001",
    "Alice Smith",
    "0400 123 456"
)

patient2 = Patient(
    "P002",
    "Bob Johnson",
    "0400 987 654"
)


# Create practitioners
practitioner1 = Practitioner(
    "D001",
    "Dr. John Doe",
    "General Practice"
)

practitioner2 = Practitioner(
    "D002",
    "Dr. Jane Roe",
    "General Practice"
)


# Create appointments
appointment1 = Appointment(
    "A001",
    patient1,
    practitioner1,
    "2024-07-20 10:00 AM"
)

appointment2 = Appointment(
    "A002",
    patient2,
    practitioner2,
    "2024-07-20 11:30 AM"
)


# Book appointments
try:
    appointment_service.book_appointment(appointment1)
    appointment_service.book_appointment(appointment2)

    print("\nAppointments successfully booked.")

except ValueError as error:
    print("\nError:", error)


# Display appointments
print("\nCurrent Appointments")
app.display_appointments()


# Test duplicate booking
print("\nTesting Duplicate Booking")

try:
    duplicate = Appointment(
        "A003",
        patient2,
        practitioner1,
        "2024-07-20 10:00 AM"
    )

    appointment_service.book_appointment(duplicate)

except ValueError as error:
    print("Booking rejected:", error)


# Test cancellation
print("\nCancelling Appointment A002")

try:
    appointment_service.cancel_appointment("A002")
    print("Appointment cancelled successfully.")

except ValueError as error:
    print("Error:", error)


# Display final appointments
print("\nFinal Appointment List")
app.display_appointments()