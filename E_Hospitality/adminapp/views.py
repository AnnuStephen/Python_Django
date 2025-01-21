from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Patient.forms import AppointmentForm
from accounts.forms import RegistrationForm
from accounts.models import User
from Doctor.models import Doctor, EPrescription
from Patient.models import Appointment, Billing, HealthResource, MedicalHistory, Patient
from adminapp.forms import EditUserForm, FacilityForm
from adminapp.models import Facility

def admin_dashboard(request):
    
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)
        
        if user.role == 'Admin':  

            doctors = Doctor.objects.all()
            patients = Patient.objects.all()
            appointments = Appointment.objects.all()  
            facilities = Facility.objects.all()            
            
            users = User.objects.all()     

            # users = User.objects.exclude(role='Admin')   
            
            return render(request, 'admin/admin_dashboard.html', {
                'user': user,
                'doctors': doctors,
                'patients': patients,
                'appointments': appointments,
                'facilities': facilities,
                'users': users
            })
        else:
            messages.error(request, "Access denied! You are not authorized to view this page.")
            return redirect('login')
    else:
        messages.error(request, "You are not logged in. Please log in to view your dashboard.")
        return redirect('login')


def create_user(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)        
        
        if user.role == 'Admin':
            if request.method == 'POST':
                form = RegistrationForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "User created successfully!")
                    return redirect('admin_dashboard')  
            else:
                form = RegistrationForm()
            return render(request, 'admin/create_user.html', {'form': form})
        else:
            messages.error(request, "You do not have permission to create users.")
            return redirect('home')  
    else:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')

def edit_user(request, user_id):

    if 'user_id' in request.session:

        admin_id = request.session['user_id']
        admin = get_object_or_404(User, id=admin_id)
        
        if admin.role == 'Admin':  
            user = get_object_or_404(User, id=user_id)
            if request.method == 'POST':
                form = EditUserForm(request.POST, instance=user)
                if form.is_valid():
                    form.save()
                    messages.success(request, "User details updated successfully!")
                    return redirect('admin_dashboard')  
            else:
                form = EditUserForm(instance=user)
            return render(request, 'admin/edit_user.html', {'form': form, 'user': user})
        else:
            messages.error(request, "You do not have permission to edit users.")
            return redirect('login') 
    else:
        messages.error(request, "Please log in first.")
        return redirect('login')


def delete_user(request, user_id):
    
    if 'user_id' in request.session:
        admin_user = get_object_or_404(User, id=request.session['user_id'])
        
        if admin_user.role == 'Admin':
            user_to_delete = get_object_or_404(User, id=user_id)
            user_to_delete.delete()
            messages.success(request, "User deleted successfully.")
        else:
            messages.error(request, "You do not have permission to delete users.")
    else:
        messages.error(request, "You must be logged in to perform this action.")
    
    return redirect('admin_dashboard') 



def create_facility(request):
    if request.session.get('user_id'):
        user = get_object_or_404(User, id=request.session['user_id'])

        if user.role != 'Admin':  # Restrict access to Admin
            messages.error(request, "You do not have permission to perform this action.")
            return redirect('login')

        if request.method == 'POST':
            form = FacilityForm(request.POST)
            if form.is_valid():
                facility = form.save(commit=False)
                facility.created_by = user
                facility.save()
                messages.success(request, "Facility added successfully!")
                return redirect('admin_dashboard')
        else:
            form = FacilityForm()

        return render(request, 'admin/create_facility.html', {'form': form})
    else:
        messages.error(request, "You are not logged in.")
        return redirect('login')
    

def edit_facility(request, pk):
    facility = get_object_or_404(Facility, id=pk)
    if request.session.get('user_id'):
        user = get_object_or_404(User, id=request.session['user_id'])

        if user.role != 'Admin':  # Restrict access to Admin
            messages.error(request, "You do not have permission to perform this action.")
            return redirect('login')

        if request.method == 'POST':
            form = FacilityForm(request.POST, instance=facility)
            if form.is_valid():
                form.save()
                messages.success(request, "Facility updated successfully!")
                return redirect('admin_dashboard')
        else:
            form = FacilityForm(instance=facility)

        return render(request, 'admin/edit_facility.html', {'form': form})
    else:
        messages.error(request, "You are not logged in.")
        return redirect('login')

# Delete Facility
def delete_facility(request, pk):
    facility = get_object_or_404(Facility, id=pk)
    if request.session.get('user_id'):
        user = get_object_or_404(User, id=request.session['user_id'])

        if user.role != 'Admin':  # Restrict access to Admin
            messages.error(request, "You do not have permission to perform this action.")
            return redirect('login')

        facility.delete()
        messages.success(request, "Facility deleted successfully!")
        return redirect('admin_dashboard')
    else:
        messages.error(request, "You are not logged in.")
        return redirect('login')
    
    
# doctor details view
def doctor_details(request, user_id):
    if 'user_id' in request.session:
        user = get_object_or_404(User, id=request.session['user_id'])
        
        if user.role == 'Admin':  
            try:
               
                doctor = Doctor.objects.get(user__id=user_id)
                appointments = Appointment.objects.filter(doctor=doctor, status__in=['Scheduled', 'Rescheduled'])  # Filter appointments for this doctor
            except Doctor.DoesNotExist:
                # If no doctor is found, render the page with a message
                doctor = None
                appointments = []
                messages.info(request, "No doctor data available.")
            
            return render(request, 'admin/manage_doctors.html', {
                'doctor': doctor,
                'appointments': appointments
            })
        else:
            messages.error(request, "Access denied! You are not authorized to view this page.")
            return redirect('login')
    else:
        messages.error(request, "You are not logged in. Please log in to view this page.")
        return redirect('login')
    

# patient details view
def patient_details(request, user_id):
    # Check if user is logged in and is an admin
    if 'user_id' in request.session:
        user = get_object_or_404(User, id=request.session['user_id'])
        
        if user.role == 'Admin':  # Admin role check
            try:
                
                patient = Patient.objects.get(user__id=user_id)
                appointments = Appointment.objects.filter(patient__user=user_id) 
                billing_info = Billing.objects.filter(patient__user=user_id)  
                medical_histories = MedicalHistory.objects.filter(patient__user=user_id)
                prescriptions = EPrescription.objects.filter(patient__user=user_id)
                resources = HealthResource.objects.filter(patient__user=user_id)
            
                
            except Patient.DoesNotExist:
               
                patient = None
                appointments = []
                billing_info = []
                medical_histories=[]
                prescriptions=[]
                resources=[]

                messages.info(request, "No patient data available.")
            
            return render(request, 'admin/manage_patients.html', {
                'patient': patient,
                'appointments': appointments,
                'billing_info': billing_info,
                'medical_histories':medical_histories,
                'prescriptions':prescriptions,
                'resources':resources
            })
        else:
            messages.error(request, "Access denied! You are not authorized to view this page.")
            return redirect('login')
    else:
        messages.error(request, "You are not logged in. Please log in to view this page.")
        return redirect('login')



def admin_create_appointment(request, patient_id):
    if 'user_id' in request.session:
        admin_user = get_object_or_404(User, id=request.session['user_id'])
        if admin_user.role != 'Admin':
            messages.error(request, "Access denied! Only admins can create appointments.")
            return redirect('admin_dashboard')
        
        
        patient = get_object_or_404(Patient, user__id=patient_id)

        if request.method == 'POST':
            form = AppointmentForm(request.POST)
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.patient = patient  
                appointment.status = 'Scheduled'
                appointment.save()
                messages.success(request, "Appointment created successfully for the patient!")
                return redirect('patient_details', user_id=patient_id)  
            else:
                print(form.errors)  
        else:
            form = AppointmentForm()

        return render(request, 'admin/create_appointment.html', {
            'form': form,
            'patient': patient
        })
    else:
        messages.error(request, "You are not logged in. Please log in as an admin to create an appointment.")
        return redirect('login')


def edit_appointment(request, appointment_id):
    if 'user_id' in request.session:
        user = get_object_or_404(User, id=request.session['user_id'])

        if user.role == 'Admin':
            appointment = get_object_or_404(Appointment, id=appointment_id)

            if request.method == 'POST':
                new_date = request.POST.get('date')
                new_time = request.POST.get('time')

                # Perform basic validation (optional)
                if not new_date or not new_time:
                    messages.error(request, "Please provide a valid date and time.")
                    return render(request, 'admin/edit_appointment.html', {'appointment': appointment})

                appointment.date = new_date
                appointment.time = new_time
                appointment.status = 'Rescheduled'  
                appointment.save()

                messages.success(request, "Appointment rescheduled successfully!")
                return redirect('patient_details', user_id=appointment.patient.user.id)
            
            return render(request, 'admin/edit_appointment.html', {'appointment': appointment})

        else:
            messages.error(request, "Access denied! You are not authorized to view this page.")
            return redirect('login')

    else:
        messages.error(request, "You are not logged in. Please log in to edit this appointment.")
        return redirect('login')

def cancel_appointment(request, appointment_id):
    if 'user_id' in request.session:
        user = get_object_or_404(User, id=request.session['user_id'])

        if user.role == 'Admin':  
            appointment = get_object_or_404(Appointment, id=appointment_id)

            # Check if already canceled
            if appointment.status == 'Cancelled':
                messages.info(request, "This appointment is already canceled.")
                return redirect('patient_details', user_id=appointment.patient.user.id)

            # Update the status to 'Cancelled'
            appointment.status = 'Cancelled'
            appointment.save()

            messages.success(request, "Appointment has been successfully cancelled.")
            return redirect('patient_details', user_id=appointment.patient.user.id)  

        else:
            messages.error(request, "Access denied! You do not have permission to cancel appointments.")
            return redirect('login')

    else:
        messages.error(request, "You are not logged in. Please log in to cancel appointments.")
        return redirect('login')



