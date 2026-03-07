from django.shortcuts import render
from django.http import JsonResponse
from com.mnx.MessageNX import MessageNX

from decouple import config
from django.views.decorators.csrf import csrf_exempt

import base64

mnx = MessageNX()


@csrf_exempt
def produce(req):
    if req.method == "POST":
        user = req.POST.get("user")
        job_id = req.POST.get("id")
        timestamp = req.POST.get("timestamp")
        date = req.POST.get("date")
        time = req.POST.get("time")
        image_file = req.FILES.get("image")
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        payload = {
            "user": user,
            "id": job_id,
            "timestamp": timestamp,
            "date": date,
            "time": time,
            "image_base64": image_base64,
        }
        mnx.produce(payload, config("APP_CHANNEL"))
        return JsonResponse({"message": "pushed"})
    return JsonResponse({"message": "try later!"})
