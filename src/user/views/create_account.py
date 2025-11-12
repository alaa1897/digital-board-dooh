from django.shortcuts import render,redirect
from user.models import User 
from django.contrib.auth import login



def create_account(request):
    if request.method == 'POST':
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            role_choice =request.POST.get('role')
            if role_choice == 'client':
                role = 'client'
            elif role_choice == 'admin':
                role = 'admin'
            else:
                 print('you should choose an option')
        
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                role=role
            )
            user.save()
            
            login(request,user)
            if role == 'client':
                return redirect('client_dashboard')
            else:
                return redirect('admin_dashboard')
    else:    
        return render(request, 'general/create_account.html')
    
   
