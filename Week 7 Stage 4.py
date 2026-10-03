import json
import os


class Patient:
    def __init__(self, patient_id, name, contact_details):
        if not name:
            raise ValueError("Patient name cannot be empty.")

        self.patient_id = patient_id
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
        self.appointment_id = appointment_id
        self.patient = patient
        self.practitioner = practitioner
        self.appointment_time = appointment_time
        self.status = status

    def cancel(self):
        self.status = "Cancelled"

    def get_details(self):
        return (
            f"Appointment ID: {self.appointment_id} | "
            f"Patient: {self.patient.name} | "
            f"Practitioner: {self.practitioner.name} | "
            f"Time: {self.appointment_time} | "
            f"Status: {self.status}"
        )


class AppointmentRepository:
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


class AppointmentService:
    def __init__(self, repository):
        self.repository = repository
        self.appointments = repository.load()

    def book_appointment(self, appointment):
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

    def display_appointments(self):
        if not self.appointments:
            print("No appointments found.")
            return

        for appointment in self.appointments:
            print(appointment.get_details())


# Create repository
repository = AppointmentRepository()

# Create service
service = AppointmentService(repository)

# Create patient and practitioner
patient = Patient(
    "P001",
    "Alice Smith",
    "0400 123 456"
)

practitioner = Practitioner(
    "D001",
    "Dr. John Doe",
    "General Practice"
)

# Create appointment
appointment = Appointment(
    "A001",
    patient,
    practitioner,
    "2024-07-20 10:00 AM"
)

# Book appointment
try:
    service.book_appointment(appointment)
    print("Appointment successfully booked.")

except ValueError as error:
    print("Error:", error)

# Display appointments
print("\nAppointments")
service.display_appointments()