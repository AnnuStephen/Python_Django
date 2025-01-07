from django.shortcuts import render, redirect,get_object_or_404
import stripe

from Doctor.models import EPrescription
from E_Hospitality import settings
from accounts.models import User
from .forms import AppointmentForm, PatientForm
from .models import Patient, Appointment, MedicalHistory, Billing, HealthResource
from django.contrib import messages


 
def patient_dashboard(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)

        if user.role == 'Patient':
            try:
                patient = Patient.objects.get(user=user) 
                appointments = Appointment.objects.filter(patient=patient)
                medical_histories = MedicalHistory.objects.filter(patient=patient)
                billing_info = Billing.objects.filter(patient=patient)
                resources = HealthResource.objects.all()
                
                prescriptions = EPrescription.objects.filter(patient=patient)
                
                
                return render(request, 'patient_dashboard.html', {
                    'user': user,
                    'appointments': appointments,
                    'medical_histories': medical_histories,
                    'billing_info': billing_info,
                    'resources': resources,
                    'prescriptions': prescriptions
                })
            except Patient.DoesNotExist:
                messages.error(request, "Patient details not found! Please complete your profile.")
                return redirect('create_profile') 
        else:
            messages.error(request, "Access denied! You are not authorized to view this page.")
            return redirect('login') 

    else:
        messages.error(request, "You are not logged in. Please log in to view your dashboard.")
        return redirect('login') 
    

def create_profile(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)

        if request.method == 'POST':
            form = PatientForm(request.POST)
            if form.is_valid():
                patient = form.save(commit=False)
                patient.user = user 
                patient.save()
                messages.success(request, "Your details have been successfully added!")
                return redirect('patient_dashboard') 
        else:
            form = PatientForm()

        return render(request, 'create_profile.html', {'form': form}) 

    else:
        messages.error(request, "You are not logged in. Please log in to add your details.")
        return redirect('login')  


def create_appointment(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)

        if request.method == 'POST':
            form = AppointmentForm(request.POST)
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.patient = Patient.objects.get(user=user)  
                appointment.status = 'Scheduled'
                appointment.save()
                messages.success(request, "Appointment scheduled successfully!")
                return redirect('patient_dashboard')  
            else:
                print(form.errors) 
        else:
            form = AppointmentForm()
        
        return render(request, 'create_appointment.html', {'form': form})

    else:
        messages.error(request, "You are not logged in. Please log in to add your details.")
        return redirect('login') 



# # Set your secret key
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def pay_bill(request, bill_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)
        
        if user.role == 'Patient':
            try:
                bill = get_object_or_404(Billing, id=bill_id, patient__user=user)

                if bill.payment_status == 'Paid':
                    messages.info(request, "The bill has already been paid.")
                    return redirect('patient_dashboard')
                
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',  
                            'product_data': {
                                'name': f"Bill for {bill.patient.first_name} {bill.patient.last_name}",
                            },
                            'unit_amount': int(bill.amount * 100), 
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri('/patient/payment-success/') + f'?bill_id={bill.id}',
                    cancel_url=request.build_absolute_uri('/patient/payment-cancelled/'),
                )

               
                return redirect(checkout_session.url, code=303)

            except Billing.DoesNotExist:
                messages.error(request, "Bill not found!")
                return redirect('patient_dashboard')

        else:
            messages.error(request, "Access denied! You are not authorized to pay this bill.")
            return redirect('login') 

    else:
        messages.error(request, "You are not logged in. Please log in to pay the bill.")
        return redirect('login')  
    



def payment_success(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)

        if user.role == 'Patient':
            bill_id = request.GET.get('bill_id')
            if not bill_id:
                messages.error(request, "Invalid payment details!")
                return redirect('patient_dashboard')

            try:
                bill = get_object_or_404(Billing, id=bill_id, patient__user=user)

                if bill.payment_status == 'Paid':
                    messages.info(request, "This bill has already been paid.")
                    return redirect('patient_dashboard')

                bill.payment_status = 'Paid'
                bill.save()


                appointments = Appointment.objects.filter(patient=bill.patient, status='Scheduled')
                appointments.update(status='Completed')


                messages.success(request, "Payment successful and appointments marked as completed!")
                return redirect('patient_dashboard')

            except Billing.DoesNotExist:
                messages.error(request, "Bill not found!")
                return redirect('patient_dashboard')

        else:
            messages.error(request, "You are not authorized to view this page.")
            return redirect('login')

    else:
        messages.error(request, "You are not logged in. Please log in to continue.")
        return redirect('login')


def payment_cancelled(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = get_object_or_404(User, id=user_id)

        if user.role == 'Patient':
            messages.error(request, "Payment was cancelled. Please try again.")
            return render(request, 'patient_dashboard.html', {'payment_status': 'cancelled'})
        else:
            messages.error(request, "You are not authorized to view this page.")
            return render(request, 'patient_dashboard.html', {'payment_status': 'error'})

    else:
        messages.error(request, "You are not logged in. Please log in to continue.")
        return render(request, 'patient_dashboard.html', {'payment_status': 'error'})


