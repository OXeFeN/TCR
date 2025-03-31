import datetime
import calendar
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone
from .models import Reservation

def calendar_view(request):
    """
    Zobrazení kalendáře pro aktuální měsíc.
    """
    today = datetime.date.today()
    year = today.year
    month = today.month

    cal = calendar.Calendar(firstweekday=0)  # 0 = Pondělí
    month_days = cal.monthdatescalendar(year, month)
    calendar_weeks = []

    for week in month_days:
        week_list = []
        for day in week:
            reservations = Reservation.objects.filter(date=day)
            reservation_list = [
                {"start_hour": res.start_hour, "end_hour": res.end_hour}
                for res in reservations
            ]
            week_list.append({
                "day": day.day,
                "date": day.isoformat(),
                "is_current_month": (day.month == month),
                "reservations": reservation_list,
                "is_past": (day < today)  # Dny v minulosti
            })
        calendar_weeks.append(week_list)

    context = {
        "calendar_weeks": calendar_weeks,
        "max_reservations": 5  # nastavit maximální počet rezervací za den
    }
    return render(request, "calendar.html", context)

def my_reservations_view(request):
    if not request.user.is_authenticated:
        # Pokud uživatel není přihlášen, nemusíme nic načítat
        return render(request, "my_reservation.html")
    
    now = timezone.now().date()
    # Předpokládáme, že Reservation má pole "date"
    future_reservations = Reservation.objects.filter(user=request.user, date__gte=now).order_by("date")
    past_reservations = Reservation.objects.filter(user=request.user, date__lt=now).order_by("-date")
    
    context = {
        "future_reservations": future_reservations,
        "past_reservations": past_reservations,
    }
    return render(request, "my_reservation.html", context)

@require_GET
def available_intervals(request):
    """
    Vrací JSON s dostupnými 1-hodinovými bloky pro dané datum.
    Povolené intervaly jsou mezi 6:00 a 22:00.
    Pro dnešní den se vyloučí bloky, jejichž počátek je dříve nebo rovno aktuální hodině.
    """
    date_str = request.GET.get("date")
    if not date_str:
        return JsonResponse({"error": "Datum není specifikováno."}, status=400)
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "Neplatný formát data. Použijte YYYY-MM-DD."}, status=400)
    
    now = datetime.datetime.now()
    today = datetime.date.today()
    if date_obj == today:
        current_hour = now.hour
    # Rezervace pro dnešní den začínají až po aktuální hodině, ale minimálně od 6:00
        start_hour = max(6, current_hour + 1)
        allowed_intervals = [{"start": h, "end": h + 1} for h in range(start_hour, 22)]
    else:
        allowed_intervals = [{"start": h, "end": h + 1} for h in range(6, 22)]
    
    reservations = Reservation.objects.filter(date=date_obj)
    reserved_intervals = [(r.start_hour, r.end_hour) for r in reservations]
    
    available = []
    for interval in allowed_intervals:
        conflict = False
        for res_start, res_end in reserved_intervals:
            if interval["start"] < res_end and interval["end"] > res_start:
                conflict = True
                break
        if not conflict:
            available.append(interval)
    
    return JsonResponse(available, safe=False)


@login_required
@require_POST
def create_reservation(request):
    """
    Zpracování AJAX požadavku pro vytvoření nové rezervace.
    """
    try:
        data = json.loads(request.body)
        date_str = data.get("date")
        start_hour = int(data.get("start_hour"))
        end_hour = int(data.get("end_hour"))
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

        if end_hour <= start_hour:
            return JsonResponse({"error": "Koncová hodina musí být větší než začáteční."}, status=400)

        with transaction.atomic():
            overlapping = Reservation.objects.select_for_update().filter(
                date=date_obj,
                start_hour__lt=end_hour,
                end_hour__gt=start_hour,
            )
            if overlapping.exists():
                return JsonResponse({"error": "Časový úsek je již rezervován."}, status=400)

            reservation = Reservation.objects.create(
                user=request.user,
                date=date_obj,
                start_hour=start_hour,
                end_hour=end_hour,
            )
        return JsonResponse({"message": "Rezervace byla úspěšně vytvořena."})
    
    except (ValueError, KeyError):
        return JsonResponse({"error": "Nesprávný vstupní formát."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@staff_member_required
def admin_reservations_view(request):
    """
    Zobrazení všech rezervací pro admina.
    """
    reservations = Reservation.objects.all().order_by('-date', '-start_hour')
    context = {"reservations": reservations}
    return render(request, "admin_reservations.html", context)

@staff_member_required
@require_POST
def delete_reservation(request, reservation_id):
    """
    Umožňuje adminovi smazat rezervaci.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    messages.success(request, "Rezervace byla úspěšně smazána.")
    return redirect("admin_reservations")