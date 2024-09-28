from django.shortcuts import render
from django.http import JsonResponse
from .models import Doctor, Appointment
from .symptom_mapping import SYMPTOM_SPECIALTY_MAP

# Chatbot view to handle symptom input and doctor shortlisting
def chatbot(request):
    if request.method == 'POST':
        # Collect patient symptoms from chatbot input
        patient_symptoms = request.POST.get('symptoms')
        patient_name = request.POST.get('name')  # You can store patient name in session or ask

        # Map symptoms to specialty
        specialty = SYMPTOM_SPECIALTY_MAP.get(patient_symptoms.lower(), None)
        if not specialty:
            return JsonResponse({"message": "We couldn't identify a specialty for your symptoms. Please consult a general physician."})

        # Find doctors for that specialty
        doctors = Doctor.objects.filter(specialty=specialty)
        if not doctors.exists():
            return JsonResponse({"message": f"Sorry, we couldn't find any doctors for the specialty: {specialty}"})

        # Show available doctors
        doctor_list = [{"name": doc.name, "specialty": doc.specialty, "availability": doc.availability} for doc in doctors]
        
        # Returning doctors as JSON for chatbot to render
        return JsonResponse({
            "message": f"We found {len(doctor_list)} doctor(s) for your symptoms.",
            "doctors": doctor_list
        })

    # Return chatbot default response
    return JsonResponse({"message": "Welcome to Gemini Healthcare chatbot! How can I assist you today?"})

# Function to handle appointment creation
def make_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        appointment_time = request.POST.get('appointment_time')
        patient_name = request.POST.get('patient_name')
        symptoms = request.POST.get('symptoms')

        # Validate input and create an appointment
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            appointment = Appointment.objects.create(
                patient_name=patient_name,
                doctor=doctor,
                appointment_time=appointment_time,
                symptoms=symptoms
            )
            return JsonResponse({"message": f"Appointment successfully scheduled with Dr. {doctor.name} on {appointment_time}."})
        except Doctor.DoesNotExist:
            return JsonResponse({"message": "Doctor not found!"})

    return JsonResponse({"message": "Failed to schedule appointment."})
# In appointment/views.py
def chatbot_interface(request):
    return render(request, 'chatbot.html')

