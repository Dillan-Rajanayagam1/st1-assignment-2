# SmartCare AI-Generated Appointment System

appointments = []

def book_appointment(patient, practitioner, time):

    if not patient:
        print("Error: Patient name is required.")
        return

    appointment = {
        "patient": patient,
        "practitioner": practitioner,
        "time": time
    }

    appointments.append(appointment)
    print("Appointment successfully booked!")


def display_appointments():

    if len(appointments) == 0:
        print("No appointments found.")
        return

    for appointment in appointments:
        print("----------------------")
        print("Patient:", appointment["patient"])
        print("Practitioner:", appointment["practitioner"])
        print("Time:", appointment["time"])


# Example appointments
book_appointment("Alice Smith", "Dr. John Doe", "2024-07-20 10:00 AM")
book_appointment("Bob Johnson", "Dr. Jane Roe", "2024-07-20 11:30 AM")

display_appointments()