from decimal import Decimal
import urllib.parse
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from app.models import User, Payment
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import logout



def loginpage(request):

    if request.method == 'POST':

        email=request.POST.get('email')
        password=request.POST.get('password')

        user = User.objects.filter(email=email).first()

        if user is not None and user.check_password(password):
            request.session['email'] = request.POST.get('email')
            request.session.save()
            return redirect('dashboard')
        else:
            return redirect('signuppage')


    return render(request, 'login.html')


def money_transfer(request):
    email = request.session.get('email')

    if email:

        if request.method == 'POST':
            rname = request.POST.get('rname')
            remail = request.POST.get('remail')
            amount = request.POST.get('amount')

            try:  # If recipient is a registered user.
                ruser = get_object_or_404(User, email=remail, name=rname)
                ruser.account_balance += Decimal(amount)
                ruser.save()
                sender = get_object_or_404(User, email=email)
                sender.account_balance -= Decimal(amount)
                sender.save()

                Payment.objects.create_payment(
                    sender=sender,
                    recipient_email=remail,
                    recipient_name=rname,
                    amount=Decimal(amount),
                    status='Completed'
                )

                dashboard_link = f"http://127.0.0.1:8000/dashboard?email={ruser.email}&amount={amount}&type={'registered'}"
                message = f"Fund successfully transmitted! Accept it through the dashboard: {dashboard_link}"

                send_mail(
                    "Welcome to the Payment Platform",
                    message,
                    'edupurposes24x7@example.com',
                    [ruser.email],
                    fail_silently=False
                )

                return redirect('dashboard')  # Redirect to the dashboard after successful transfer

            except Exception:  # If recipient is unregistered.
                sender = get_object_or_404(User, email=email)
                sender.account_balance -= Decimal(amount)
                sender.save()

                Payment.objects.create_payment(
                    sender=sender,
                    recipient_email=remail,
                    recipient_name=rname,
                    amount=Decimal(amount),
                    status='pending'
                )

                registration_link = f"http://127.0.0.1:8000/?email={remail}&amount={amount}&type={'unregistered'}"
                message = f"Fund transmission is pending! Accept it through the registration: {registration_link}"

                send_mail(
                    "Welcome to the Payment Platform",
                    message,
                    'edupurposes24x7@example.com',
                    [remail],
                    fail_silently=False
                )

                return redirect('dashboard')  # Redirect to the dashboard after successful transfer

        else:
            return redirect('loginpage')
    else:
        return redirect('loginpage')



def dashboard(request):
    email = request.session.get('email')
    
    if email:
        user = get_object_or_404(User, email=email)
        pending_amount=Decimal(0.0)
        return render(request, 'dashboard.html', {'email': email,'user': user,'amount':pending_amount})
    
    elif  request.GET.get('email') and request.GET.get('amount') is not None:
        email =request.GET.get('email')
        request.session['email'] = email
        request.session.save()
        pending_amount=Decimal(request.GET.get('amount'))
        user = get_object_or_404(User, email=email)
        Payment.objects.filter(amount=pending_amount, recipient_email=email).update(status='completed & accepted')
        return render(request, 'dashboard.html', {'email': email,'user': user,'amount':pending_amount})
    else:
        return redirect('loginpage')


def logout_view(request):
    logout(request)
    request.session.flush()  # Clear all session data
    return redirect('loginpage')

# def signuppage(request):

#     if request.GET.get('email') and request.GET.get('type') and request.GET.get('amount') is not None:
#         initial_amount = Decimal(request.GET.get('amount'))
#     else:
#         initial_amount = Decimal(10000)

#     if request.method == 'POST':

#         email=request.POST.get('email')
#         name=request.POST.get('name')
#         password=request.POST.get('password')

#         user = User(
#             email=email,
#             name=name,
#             account_balance=initial_amount
#         )
#         user.set_password(password)
#         user.save()
#         request.session['email'] = email
#         request.session.save()

#         message = "Congratulation!. Yoy are Succussfully registerd"
#         send_mail(
#             "Welcome to the Payment Platform",
#             message,
#             'edupurposes24x7@example.com',
#             [email],
#             fail_silently=False
#         )
#         return redirect('dashboard')
#     else:
#         return render(request, 'registration.html')


# def signuppage(request):
#     if request.GET.get('email') and request.GET.get('type') and request.GET.get('amount') is not None:
#         return HttpResponse('yes')
#     else:
#         return HttpResponse('bad')

#     return render(request, 'registration.html')


def signuppage(request):
    # if request.GET.get('email') and request.GET.get('type') and request.GET.get('amount') is not None:
    email = request.GET.get('email')
    amount = request.GET.get('amount')
    user_type = request.GET.get('type')

    if (email is not None) and (amount is not None) and (user_type is not None):
        initial_amount = Decimal(request.GET.get('amount'))
    else:
        initial_amount = Decimal(10000)

    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')

        # URL decode the email parameter
        email = urllib.parse.unquote(email)

        user = User(
            email=email,
            name=name,
            account_balance=initial_amount
        )
        user.set_password(password)
        user.save()
        request.session['email'] = email
        request.session.save()

        message = "Congratulations! You are successfully registered"
        send_mail(
            "Welcome to the Payment Platform",
            message,
            'edupurposes24x7@example.com',
            [email],
            fail_silently=False
        )
        return redirect('dashboard')
    else:
        return render(request, 'registration.html')
