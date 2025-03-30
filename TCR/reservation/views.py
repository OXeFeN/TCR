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
    today = datetime.date.today()
    year = today.year
    month = today.month

    cal = calendar.Calendar(firstweekday=0)  # Lze nastavit dle požadavku (0 = pondělí)
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
                "is_current_month": day.month == month,
                "reservations": reservation_list,
            })
        calendar_weeks.append(week_list)

    context = {"calendar_weeks": calendar_weeks}
    return render(request, "reservations/calendar.html", context)


@require_POST
def create_reservation(request):
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
    Zobrazí stránku se všemi rezervacemi, kterou mohou spravovat pouze admini.
    """
    reservations = Reservation.objects.all().order_by('-date', '-start_hour')
    context = {"reservations": reservations}
    return render(request, "reservations/admin_reservations.html", context)


@staff_member_required
@require_POST
def delete_reservation(request, reservation_id):
    """
    Umožní adminovi smazat rezervaci.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    messages.success(request, "Rezervace byla úspěšně smazána.")
    return redirect("admin_reservations")