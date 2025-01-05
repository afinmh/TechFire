from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Userakun, SensorData, FireImage
import json
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.storage import default_storage
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

def gambar(request):
    return render(request, 'gambar.html')

# --- Bagian Database ---

# -Get data terbaru yang dikirim ke database
def get_status(request):
    return JsonResponse(status_data)

# -Update data ke database
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

# Login
def dashboard(request):
    if request.session.get('login_status') == 1:
        return render(request, 'dashboard.html')
    else:
        return redirect('login') 


# ----- API -----

# -Database Akun
@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')

        if not username or not password:
            if request.content_type == 'application/json':
                return JsonResponse({'error': 'Username and password are required.'}, status=400)
            else:
                return render(request, 'login.html', {'error': 'Username and password are required.'})

        try:
            user = Userakun.objects.get(username=username)
            if user.password == password:
                if request.content_type == 'application/json':
                    return JsonResponse({
                        'success': True,
                        'user_id': user.id,
                        'username': user.username,
                    })
                else:
                    request.session['user_id'] = user.id
                    request.session['login_status'] = 1
                    return redirect('dashboard')
            else:
                if request.content_type == 'application/json':
                    messages.error(request, 'Username atau password salah.')
                    return JsonResponse({'error': 'Invalid credentials.'}, status=401)
                else:
                    messages.error(request, 'Username atau password salah.')
                    return render(request, 'login.html', {'error': 'Invalid credentials.'})
        except Userakun.DoesNotExist:
            if request.content_type == 'application/json':
                messages.error(request, 'User tidak terdaftar')
                return JsonResponse({'error': 'User does not exist.'}, status=404)
            else:
                messages.error(request, 'User tidak terdaftar')
                return render(request, 'login.html', {'error': 'User does not exist.'})

    return render(request, 'login.html')

# -Databse Sensor
def sensor_data_api(request):
    if request.method == 'GET':
        sensor_data = SensorData.objects.all().order_by('-timestamp') #Urut dari Timestamp
        data = []

        for sensor in sensor_data:
            data.append({
                'pompa': sensor.pompa,
                'strobo': sensor.strobo,
                'speaker': sensor.speaker,
                'fire': sensor.fire,
                'batre': sensor.batre,
                'distance': sensor.distance,
                'timestamp': sensor.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        return JsonResponse({'sensor_data': data}, safe=False)
    else:
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)

# -Database Gambar
def fire_image_api(request):
    if request.method == 'GET':
        fire_images = FireImage.objects.all().order_by('-timestamp')  # Urut dari Timestamp
        data = []

        for image in fire_images:
            data.append({
                'timestamp': image.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'fire_image_url': request.build_absolute_uri(image.fire_image.url),  # Buat URL absolut
            })
        return JsonResponse({'fire_images': data}, safe=False)
    else:
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)

# -Upload Gambar Api
@csrf_exempt
def fire_image_upload(request):
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['fire_image']
            saved_path = default_storage.save(f'fire_images/{uploaded_file.name}', uploaded_file)
            fire_image = FireImage(fire_image=saved_path)
            fire_image.save()
            return JsonResponse({
                'message': 'Image uploaded successfully!',
                'fire_image_id': fire_image.id,
                'fire_image_url': request.build_absolute_uri(fire_image.fire_image.url),
            }, status=201)
        except KeyError:
            return JsonResponse({'error': 'fire_image is required in the request'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)



# Logout
def logout_view(request):
    logout(request)
    request.session['login_status'] = 0
    return redirect('login') 
