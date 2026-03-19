from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from com.mnx.MessageNX import MessageNX
from decouple import config
import base64

mnx = MessageNX()

@csrf_exempt
def produce(req):
    try:
        if req.method != "POST":
            return JsonResponse({"message": "Only POST allowed"}, status=405)

        print("Request received")

        user = req.POST.get("user")
        job_id = req.POST.get("id")
        timestamp = req.POST.get("timestamp")
        date = req.POST.get("date")
        time = req.POST.get("time")
        image_file = req.FILES.get("image")

        if not image_file:
            print("No image found in request")
            return JsonResponse({"message": "No image provided"}, status=400)

        print(f"Image size: {image_file.size}")

                
        img = Image.open(image_file)
        img = img.resize((512, 512))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=60)  # compressing

        # Encode image
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        payload = {
            "user": user,
            "id": job_id,
            "timestamp": timestamp,
            "date": date,
            "time": time,
            "image_base64": image_base64,
        }

        app_channel = config("APP_CHANNEL", default=None)
        if not app_channel:
            print("APP_CHANNEL not set")
            return JsonResponse({"message": "APP_CHANNEL not set"}, status=500)

        print("Producing payload to MessageNX...")
        mnx.produce(payload, app_channel)
        print("Payload produced successfully")

        return JsonResponse({"message": "pushed"})

    except Exception as e:
        # Log the exception
        print("Internal error:", str(e))
        return JsonResponse({"message": "Internal server error", "error": str(e)}, status=500)


@csrf_exempt
def test(req):
    return JsonResponse({"a": 1})

