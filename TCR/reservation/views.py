import datetime
import calendar
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
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
            })
        calendar_weeks.append(week_list)

    context = {"calendar_weeks": calendar_weeks}
    return render(request, "calendar.html", context)

def year_calendar_view(request, year=None):
    """
    Zobrazení kalendáře pro celý rok.
    Pokud není rok specifikován, použije se aktuální rok.
    """
    if year is None:
        year = datetime.date.today().year
    else:
        year = int(year)

    months_data = []
    cal = calendar.Calendar(firstweekday=0)

    # Pro každý měsíc roku (1 až 12)
    for month in range(1, 13):
        month_dates = cal.monthdatescalendar(year, month)
        month_info = {
            "month": month,
            "month_name": calendar.month_name[month],
            "weeks": []
        }
        for week in month_dates:
            week_days = []
            for day in week:
                reservations = Reservation.objects.filter(date=day)
                week_days.append({
                    "date": day,
                    "day": day.day,
                    "is_current_month": (day.month == month),
                    "reservations": reservations,
                })
            month_info["weeks"].append(week_days)
        months_data.append(month_info)

    context = {"year": year, "months": months_data}
    return render(request, "calendar_year.html", context)

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