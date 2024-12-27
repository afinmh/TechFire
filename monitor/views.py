from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .models import Userakun, SensorData
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

status_data = {
    "pompa": "OFF",
    "strobo": "OFF",
    "speaker": "OFF",
    "fire" : "Aman",
    "batre": 0,
    "distance": 0
}

def index(request):
    return render(request, 'index.html', {"status": status_data})

def get_status(request):
    return JsonResponse(status_data)

@csrf_exempt
def update_status(request):
    global status_data
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            status_data.update(data)

            SensorData.objects.create(
                pompa=data.get("pompa", "OFF"),
                strobo=data.get("strobo", "OFF"),
                speaker=data.get("speaker", "OFF"),
                fire=data.get("fire", "Aman"),
                batre=data.get("batre", 0),
                distance=data.get("distance", 0.0),
            )

            return JsonResponse({"success": True, "message": "Status updated and saved to database"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request"})

def dashboard(request):
    if request.session.get('login_status') == 1:
        return render(request, 'dashboard.html')
    else:
        return redirect('login') 

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
                request.session['login_status'] = 1
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
    logout(request)
    request.session['login_status'] = 0
    return redirect('login') 
