from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, time, timedelta
from .models import Appointment
from django.views.decorators.csrf import csrf_exempt


# Function to generate available slots
def get_available_slots(date_obj):
    start_time = time(10, 0)  # 10:00 AM
    end_time = time(17, 0)    # 5:00 PM
    break_start = time(13, 0) # 1:00 PM
    break_end = time(14, 0)   # 2:00 PM

    slots = []
    current_time = datetime.combine(date_obj, start_time)

    while current_time.time() < end_time:
        if not (break_start <= current_time.time() < break_end):  # Skip break time
            slots.append(current_time.strftime("%I:%M %p"))  # Format time in AM/PM

        current_time += timedelta(minutes=30)

    # Remove booked slots
    booked_slots = Appointment.objects.filter(date=date_obj).values_list('time_slot', flat=True)
    return [slot for slot in slots if slot not in booked_slots]


# API to fetch available slots
def available_slots(request, date):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        slots = get_available_slots(date_obj)

        return JsonResponse({"available_slots": slots})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# View to render the booking page and handle booking
@csrf_exempt
def book_appointment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        date = request.POST.get("date")
        time_slot = request.POST.get("time_slot")  # Example: "03:30 PM"

        # Convert "03:30 PM" -> "15:30"
        try:
            time_slot_24hr = datetime.strptime(time_slot, "%I:%M %p").time()
        except ValueError:
            return JsonResponse({"status": "error", "message": "Invalid time format"}, status=400)

        # Check if the slot is already booked
        if Appointment.objects.filter(date=date, time_slot=time_slot_24hr).exists():
            return JsonResponse({"status": "error", "message": "Slot already booked"}, status=400)

        # Save appointment
        Appointment.objects.create(name=name, phone=phone, date=date, time_slot=time_slot_24hr)
        return JsonResponse({"status": "success", "message": "Appointment booked successfully"})

    return render(request, "appointments/book.html")