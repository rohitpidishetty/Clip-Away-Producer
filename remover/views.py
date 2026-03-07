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

        user = req.POST.get("user")
        job_id = req.POST.get("id")
        timestamp = req.POST.get("timestamp")
        date = req.POST.get("date")
        time = req.POST.get("time")
        image_file = req.FILES.get("image")

        if not image_file:
            return JsonResponse({"message": "No image provided"}, status=400)

        MAX_SIZE = 5 * 1024 * 1024
        if image_file.size > MAX_SIZE:
            return JsonResponse({"message": "File too large"}, status=400)

        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
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
            return JsonResponse({"message": "APP_CHANNEL not set"}, status=500)

        mnx.produce(payload, app_channel)

        return JsonResponse({"message": "pushed"})

    except Exception as e:
        # Log the exception to console (Azure logs)
        print("Error in /remove/:", str(e))
        return JsonResponse({"message": "Internal server error", "error": str(e)}, status=500)
