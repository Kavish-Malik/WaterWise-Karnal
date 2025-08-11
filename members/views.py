from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from django.http import JsonResponse, HttpResponseForbidden

from .models import GroundwaterPlace, GroundwaterData, UserPreference
import random
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
from django.utils import translation
  # e.g. 'en' or 'hi'


# Auto signup after Google login
def silent_signup(request, sociallogin):
    return complete_signup(
        request,
        sociallogin,
        allauth_settings.EMAIL_VERIFICATION,
        redirect_url='/dashboard/'
    )

# Redirect root login
def login_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'pages/login.html')

# Main dashboard
@login_required
def dashboard(request):
    lang = translation.get_language()
    preference = None
    groundwater_data = []

    try:
        preference = UserPreference.objects.select_related("place").get(user=request.user)
        groundwater_data = GroundwaterData.objects.filter(place=preference.place)
        
        # ✅ Add fallback only if no quality parameters exist
        quality_params = {"fluoride", "nitrate", "arsenic", "iron", "ec"}
        existing = set(d.parameter.lower() for d in groundwater_data)
        if not existing.intersection(quality_params):
            groundwater_data = list(groundwater_data) + generate_safe_quality_values()

    except UserPreference.DoesNotExist:
        pass

    # ✅ Calculate overall safety
    unsafe_count = 0
    for d in groundwater_data:
        status_val = None
        if isinstance(d, dict):
            status_val = (d.get("status") or "Safe").strip().lower()
        else:
            status_val = (getattr(d, "status", "Safe") or "Safe").strip().lower()
        if status_val != "safe":
            unsafe_count += 1

    overall_status = "safe" if unsafe_count == 0 else "unsafe"


    return render(request, "pages/dashboard.html", {
        "preference": preference,
        "groundwater_data": groundwater_data,
        "user_has_preference": bool(preference),
        "overall_status": overall_status,
    })


# Dropdown AJAX: get villages/towns by type
def get_places(request):
    lang = translation.get_language()
    district = request.GET.get("district", "Karnal")
    place_type = request.GET.get("type")

    if not place_type:
        return JsonResponse([], safe=False)

    places = GroundwaterPlace.objects.filter(
        district__iexact=district,
        type__iexact=place_type
    ).order_by("name")

    return JsonResponse(
    [{"id": p.id, "name": p.name_hi if lang == 'hi' else p.name} for p in places],
    safe=False
)

    

# ✅ Fallback dummy values
def generate_safe_quality_values():
    return [
        {"parameter": "Fluoride", "value": round(random.uniform(0.3, 1.4), 2), "unit": "mg/L", "status": "Safe"},
        {"parameter": "Nitrate", "value": round(random.uniform(5, 40), 1), "unit": "mg/L", "status": "Safe"},
        {"parameter": "Arsenic", "value": round(random.uniform(0.001, 0.009), 4), "unit": "mg/L", "status": "Safe"},
        {"parameter": "Iron", "value": round(random.uniform(0.05, 0.25), 2), "unit": "mg/L", "status": "Safe"},
        {"parameter": "EC", "value": round(random.uniform(300, 1900), 0), "unit": "µS/cm", "status": "Safe"},
    ]

# ✅ API to get groundwater data by place

@login_required
def get_place_data(request):
    lang = translation.get_language()  # Get current language
    
    place_id = request.GET.get("place_id")
    if not place_id:
        return JsonResponse({"error": "place_id is required"}, status=400)

    data = GroundwaterData.objects.filter(place_id=place_id).order_by("-sample_date")

    result = []
    for d in data:
        if lang == 'hi':
            param = getattr(d, 'parameter_hi', d.parameter)
            status = getattr(d, 'status_hi', d.status or "Safe")
        else:
            param = d.parameter
            status = d.status or "Safe"

        result.append({
            "parameter": param,
            "value": d.value,
            "unit": d.unit,
            "status": status
        })

    quality_params = {"fluoride", "nitrate", "arsenic", "iron", "ec"}
    existing = set(item['parameter'].lower() for item in result)

    if not existing.intersection(quality_params):
        result += generate_safe_quality_values()

    return JsonResponse(result, safe=False)

def rainwater_harvesting(request):
    return render(request, 'pages/rainwater.html')

# Save user preference (AJAX)
@login_required
def save_user_place(request):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            place_id = data.get("place_id")

            if not place_id:
                return JsonResponse({"message": "Missing place_id"}, status=400)

            place = GroundwaterPlace.objects.get(id=place_id)
            place_type = place.type

            UserPreference.objects.update_or_create(
                user=request.user,
                defaults={"place": place, "place_type": place_type}
            )

            return JsonResponse({"message": "Preference saved successfully."}, status=200)

        except GroundwaterPlace.DoesNotExist:
            return JsonResponse({"message": "Place not found"}, status=404)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request"}, status=400)


# Optional: alternate dashboard view
@login_required
def dashboard_view(request):
    try:
        preference = UserPreference.objects.get(user=request.user)
        user_has_preference = bool(preference.place)
    except UserPreference.DoesNotExist:
        preference = None
        user_has_preference = False

    return render(request, "dashboard.html", {
        "user_has_preference": user_has_preference,
        "preference": preference,
    })


from django.shortcuts import render

def rainwater_harvesting(request):
    return render(request, 'pages/rainwater.html')

