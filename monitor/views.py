from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .models import Userakun
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Data status yang di-update secara real-time
status_data = {
    "mqtt_status": "Not Connected",
    "gas": "stop",
    "direction": "neutral",
    "steer": "netral",
    "distance": 0.0,
}

# Halaman utama
def index(request):
    return render(request, 'index.html', {"status": status_data})

# API untuk memberikan data real-time
def get_status(request):
    return JsonResponse(status_data)

@csrf_exempt
def update_status(request):
    global status_data
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            status_data.update(data)
            return JsonResponse({"success": True, "message": "Status updated"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request"})

# Fungsi dashboard yang hanya bisa diakses jika login
def dashboard(request):
    # Cek status login (apakah variabel login_status bernilai 1)
    if request.session.get('login_status') == 1:
        return render(request, 'dashboard.html')
    else:
        return redirect('login')  # Arahkan ke halaman login jika belum login

# Fungsi login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = Userakun.objects.get(username=username)
            print(f"Found User: {user.username}")
            if user.password == password:
                print(f"Authenticated User: {user.username}")
                request.session['user_id'] = user.id
                request.session['login_status'] = 1  # Set login_status menjadi 1
                return redirect('dashboard')
            else:
                print("Authentication failed: Incorrect password")
                messages.error(request, 'Username or password is incorrect.')
        except Userakun.DoesNotExist:
            print("Authentication failed: User does not exist")
            messages.error(request, 'Username or password is incorrect.')
    
    return render(request, 'login.html')

# Fungsi logout
def logout_view(request):
    logout(request)  # This will log out the user
    request.session['login_status'] = 0  # Set login_status menjadi 0
    return redirect('login')  # Redirect to the login page after logout
