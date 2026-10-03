print("Welcome to SmartCare: Community Clinic Appointment Booking System!")


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
    def __init__(self, appointment_id, patient, practitioner, appointment_time):
        if not appointment_time:
            raise ValueError("Appointment time is required.")

        self.appointment_id = appointment_id
        self.patient = patient
        self.practitioner = practitioner
        self.appointment_time = appointment_time
        self.status = "Booked"

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


class AppointmentService:
    def __init__(self):
        self.appointments = []

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

    def cancel_appointment(self, appointment_id):
        for appointment in self.appointments:
            if appointment.appointment_id == appointment_id:
                appointment.cancel()
                return

        raise ValueError("Appointment not found.")

    def display_appointments(self):
        if not self.appointments:
            print("No appointments found.")
            return

        for appointment in self.appointments:
            print(appointment.get_details())


# Create objects
patient1 = Patient("P001", "Alice Smith", "0400 123 456")
patient2 = Patient("P002", "Bob Johnson", "0400 987 654")

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

# Create service
appointment_service = AppointmentService()

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
appointment_service.book_appointment(appointment1)
appointment_service.book_appointment(appointment2)

print("\nCurrent Appointments")
appointment_service.display_appointments()

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

appointment_service.cancel_appointment("A002")

appointment_service.display_appointments()