import os
import base64
import json
import datetime
import traceback
import urllib.parse
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from criminal_rec.views.recognition import match_face_with_db
from criminal_rec.models import CriminalRec

recognition_results = {}
recognition_status = {}

# Render the image surveillance page
def image_surveillance(request):
    return render(request, "image-surveillance.html")

@csrf_exempt
def capture_image(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    try:
        body = json.loads(request.body)
        image_data = body.get('image', '')
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        image_name = f'captured_image_{timestamp}.png'
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        captured_image_url = f'{settings.MEDIA_URL}{image_name}'

        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        with open(image_path, 'wb') as f:
            f.write(image_bytes)

        recognition_status[image_name] = "processing"
        check_face_view_async(image_path, image_name, captured_image_url)

        return JsonResponse({
            'message': 'Image saved and recognition triggered. Waiting for result...',
            'image_name': image_name,
        })
    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=400)
    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({'error': 'Unexpected server error: ' + str(e)}, status=500)

def check_face_view_async(image_path, image_name, captured_image_url):
    try:
        result = match_face_with_db(image_path)
        print("✅ Recognition result (async):", result)

        if result.get("match"):
            try:
                criminal = CriminalRec.objects.get(criminal_id=result["criminal_id"])
                criminal_data = {
                    "criminal_photo_url": criminal.criminal_photo.url if criminal.criminal_photo else '',
                    "criminal_id": criminal.criminal_id,
                    "name": criminal.criminal_name,
                    "description": criminal.description,
                    "scars_or_marks": criminal.scars_or_marks,
                    "parole_status": criminal.parole_status,
                    "parent_institution": criminal.parent_institution,
                    "captured_image_url": captured_image_url,
                    "confidence": result.get("confidence")  
                }

                recognition_results[image_name] = {
                    "match": True,
                    "confidence": result.get("confidence"),
                    "redirect_url": f"{reverse('match-found')}?{urllib.parse.urlencode(criminal_data)}"
                }
                recognition_status[image_name] = "completed"
            except CriminalRec.DoesNotExist:
                recognition_results[image_name] = {
                    "match": False,
                    "error": "Criminal data not found",
                    "confidence": result.get("confidence")
                }
                recognition_status[image_name] = "error"
                os.remove(image_path)
                print("⚠️ Criminal not found in database (async):", result.get("criminal_id"))
        else:
            recognition_results[image_name] = {
                "match": False,
                "confidence": result.get("confidence", None),
                "message": result.get("message", "No match found above the threshold.")
            }
            recognition_status[image_name] = "completed"
            os.remove(image_path)
    except Exception as e:
        print("❌ Error during recognition (async):", str(e))
        recognition_results[image_name] = {
            "match": False,
            "error": str(e),
            "confidence": None
        }
        recognition_status[image_name] = "error"
        traceback.print_exc()

@csrf_exempt
def check_result(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    image_name = request.GET.get('image_name')
    if not image_name or image_name not in recognition_status:
        return JsonResponse({'status': 'no result'})

    status = recognition_status[image_name]
    result = recognition_results.get(image_name)

    if status == "completed":
        if result and result.get("match"):
            return JsonResponse({
                'status': 'match',
                'redirect_url': result['redirect_url'],
                'confidence': result.get("confidence")
            })
        else:
            return JsonResponse({
                'status': 'no match',
                'result': result,
                'confidence': result.get("confidence")
            })
    elif status == "processing":
        return JsonResponse({'status': 'processing'})
    elif status == "error":
        return JsonResponse({
            'status': 'error',
            'error': result.get("error", "Unknown error"),
            'confidence': result.get("confidence")
        })
    else:
        return JsonResponse({'status': 'no result'})

def match_found(request):
    criminal_photo_url = request.GET.get('criminal_photo_url', '')
    criminal_id = request.GET.get('criminal_id', '')
    name = request.GET.get('name', '')
    description = request.GET.get('description', '')
    scars_or_marks = request.GET.get('scars_or_marks', '')
    parole_status = request.GET.get('parole_status', '')
    parent_institution = request.GET.get('parent_institution', '')
    captured_image_url = request.GET.get('captured_image_url', '')
    confidence = request.GET.get('confidence', '')

    return render(request, 'match_found.html', {
        'image_url': criminal_photo_url,
        'criminal_id': criminal_id,
        'name': name,
        'description': description,
        'scars_or_marks': scars_or_marks,
        'parole_status': parole_status,
        'parent_institution': parent_institution,
        'captured_image_url': captured_image_url,
        'confidence': confidence,
    })
