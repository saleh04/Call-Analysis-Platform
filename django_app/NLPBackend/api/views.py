import requests
from django.shortcuts import render, redirect
from .models import CallAnalysis

FASTAPI_URL = "http://localhost:8000/analyze"

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        # 1. Save locally first
        audio = request.FILES['audio']
        record = CallAnalysis.objects.create(audio_file=audio, status='processing')
        
        # 2. Send to FastAPI
        try:
            files = {'file': (audio.name, audio.read(), audio.content_type)}
            response = requests.post(FASTAPI_URL, files=files, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                # 3. Update model with results
                record.transcript = data.get('transcript')
                record.intent = data.get('intent')
                record.urgency_level = data.get('urgency')
                record.routing_department = data.get('department')
                record.status = 'completed'
            else:
                record.status = 'failed'
        except requests.exceptions.RequestException:
            record.status = 'failed'
            
        record.save()
        return redirect('dashboard')

    return render(request, 'core/upload.html')

def dashboard(request):
    analyses = CallAnalysis.objects.all().order_by('-created_at')
    return render(request, 'core/dashboard.html', {'analyses': analyses})
