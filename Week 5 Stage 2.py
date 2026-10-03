print("Welcome to SmartCare: Community Clinic Appointment Booking System!")


class Patient:
    def __init__(self, patient_id, name, contact_details):
        self.patient_id = patient_id
        self.name = name
        self.contact_details = contact_details

    def update_details(self, name, contact_details):
        self.name = name
        self.contact_details = contact_details

    def get_details(self):
        return f"Patient ID: {self.patient_id} | Name: {self.name} | Contact: {self.contact_details}"


class Practitioner:
    def __init__(self, practitioner_id, name, speciality):
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


# Create patients
patient1 = Patient("P001", "Alice Smith", "0400 123 456")
patient2 = Patient("P002", "Bob Johnson", "0400 987 654")

# Create practitioners
practitioner1 = Practitioner("D001", "Dr. John Doe", "General Practice")
practitioner2 = Practitioner("D002", "Dr. Jane Roe", "General Practice")

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

# Display information
print("\nPatient Information")
print(patient1.get_details())
print(patient2.get_details())

print("\nPractitioner Information")
print(practitioner1.get_details())
print(practitioner2.get_details())

print("\nAppointment Information")
print(appointment1.get_details())
print(appointment2.get_details())

# Test cancellation
appointment2.cancel()

print("\nAfter Cancellation")
print(appointment2.get_details())