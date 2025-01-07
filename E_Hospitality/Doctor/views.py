from django.shortcuts import get_object_or_404, render, redirect


from Patient.forms import MedicalHistoryForm
from Patient.models import Appointment, Billing, Patient
from accounts.models import User
from .forms import DoctorProfileForm, EPrescriptionForm
from .models import Doctor,EPrescription
from django.contrib import messages


def doctor_dashboard(request):

    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)

        if user.role == 'Doctor':
            try:
                doctor = Doctor.objects.get(user=user)
                prescriptions = EPrescription.objects.filter(doctor=doctor)
                appointments = Appointment.objects.filter(doctor=doctor ,status='Scheduled')  # Filter appointments for this doctor

                return render(request, 'doctor_dashboard.html', {
                    'user': user,
                    'doctor':doctor,
                    'prescriptions': prescriptions,
                    'appointments': appointments
                })
            except Doctor.DoesNotExist:
                messages.error(request, "Doctor not found!")
                return redirect('create_doctor')
        else:
            messages.error(request, "Access denied! You are not authorized to view this page.")
            return redirect('login') 

    else:
        messages.error(request, "You are not logged in. Please log in to view your dashboard.")
        return redirect('login') 
    


def create_doctor(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)

        if request.method == 'POST':
            form = DoctorProfileForm(request.POST)
            if form.is_valid():
                doctor = form.save(commit=False)
                doctor.user = user  
                doctor.save()
                messages.success(request, "Your details have been successfully added!")
                return redirect('doctor_dashboard')  
        else:
            form = DoctorProfileForm()

        return render(request, 'create_doctor.html', {'form': form})  

    else:
        messages.error(request, "You are not logged in. Please log in to add your details.")
        return redirect('login')







def add_medical_history(request, appointment_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)

       
        if user.role == 'Doctor':
            try:
               
                appointment = get_object_or_404(Appointment, id=appointment_id, doctor__user=user)
                
                if request.method == 'POST':
                    form_medical_history = MedicalHistoryForm(request.POST)
                    form_prescription = EPrescriptionForm(request.POST)
                    
                    if form_medical_history.is_valid() and form_prescription.is_valid():
                        
                        medical_history = form_medical_history.save(commit=False)
                        medical_history.patient = appointment.patient  
                        medical_history.save()

                        # Save prescription
                        prescription = form_prescription.save(commit=False)
                        prescription.patient = appointment.patient 
                        prescription.doctor = appointment.doctor  
                        prescription.save()

                        
                        appointment.medical_history_added = True
                        appointment.prescription_added = True
                        appointment.save()

                        messages.success(request, "Medical history and prescription added successfully!")
                        return redirect('doctor_dashboard')  
                else:
                    form_medical_history = MedicalHistoryForm()
                    form_prescription = EPrescriptionForm()

                
                return render(request, 'medical_history.html', {
                    'form_medical_history': form_medical_history,
                    'form_prescription': form_prescription,
                    'appointment': appointment
                })

            except Appointment.DoesNotExist:
                messages.error(request, "Appointment not found or you're not authorized to edit this appointment.")
                return redirect('doctor_dashboard')

        else:
            messages.error(request, "Access denied! You are not authorized to view this page.")
            return redirect('login')  

    else:
        messages.error(request, "You are not logged in. Please log in to add medical history and prescription.")
        return redirect('login')  




def create_bill(request, appointment_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)

       
        if user.role == 'Doctor':
            try:
                
                appointment = get_object_or_404(Appointment, id=appointment_id, doctor__user=user)

               
                if request.method == 'POST':
                    amount = request.POST.get('amount') 
                    if amount:
                        billing = Billing(patient=appointment.patient, amount=amount, appointment=appointment, payment_status='Pending')
                        billing.save()
                        messages.success(request, "Bill created successfully!")
                        return redirect('doctor_dashboard')  
                else:
                    return render(request, 'create_bill.html', {'appointment': appointment})

            except Appointment.DoesNotExist:
                messages.error(request, "Appointment not found!")
                return redirect('doctor_dashboard')
        else:
            messages.error(request, "Access denied! You are not authorized to create a bill.")
            return redirect('login')

    else:
        messages.error(request, "You are not logged in. Please log in to create a bill.")
        return redirect('login')
    
    