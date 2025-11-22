from datetime import timedelta
from typing import Dict

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CustomLoginForm, CustomRegistrationForm, UploadForm
from .models import CustomUser, Project, UserLoginLog


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = CustomRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome to MET! Start checking misinformation.")
        return redirect("dashboard")
    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = CustomLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        selected_role = form.cleaned_data.get("role")
        user = form.get_user()
        if user.role != selected_role:
            messages.error(request, "Role mismatch. Please choose the correct role.")
        else:
            login(request, user)
            # Log the login
            ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            UserLoginLog.objects.create(user=user, ip_address=ip, user_agent=user_agent)
            return redirect("dashboard")
    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect("login")
    return render(request, "auth/logout_confirm.html")


def _predict_confidence(payload: Dict[str, str]) -> float:
    """
    Lightweight heuristic to mimic a prediction engine. It combines characters
    from the idea, description, and file_type into a deterministic score so
    admins can reason about reported values even without a model.
    """

    text = "".join(payload.values())
    if not text:
        return 50.0
    base = sum(ord(c) for c in text)
    confidence = 35 + (base % 66)  # keep between 35 and 100
    return round(min(confidence, 99.9), 2)


def _collect_dashboard_data(user: CustomUser, search_query=None):
    is_admin = user.is_staff or user.role == "admin"
    queryset = Project.objects.all() if is_admin else user.projects.all()
    
    if search_query:
        queryset = queryset.filter(
            Q(idea__icontains=search_query) |
            Q(public_id__icontains=search_query) |
            Q(file_name__icontains=search_query)
        )
    avg_confidence = queryset.aggregate(avg=Avg("prediction_confidence"))["avg"]
    idea_stats = (
        list(
            Project.objects.values("idea").annotate(
                avg_conf=Avg("prediction_confidence"),
                total=Count("id"),
            )
            .order_by("-avg_conf")
        )
        if is_admin
        else None
    )

    now = timezone.now()
    monthly_report = (
        Project.objects.filter(
            created_at__year=now.year,
            created_at__month=now.month,
        )
        if is_admin
        else user.projects.filter(
            created_at__year=now.year,
            created_at__month=now.month,
        )
    )

    total_uploads = queryset.count()
    recent_uploads = queryset.filter(created_at__gte=now - timedelta(days=7)).count()
    stat_total = len(idea_stats) if idea_stats else 0
    id_confidence = list(
        queryset.values("id", "public_id", "user__username")
        .annotate(avg_conf=Avg("prediction_confidence"))
        .order_by("-avg_conf")
    )

    return {
        "is_admin": is_admin,
        "history": queryset,
        "avg_confidence": round(avg_confidence, 2) if avg_confidence else None,
        "idea_stats": idea_stats,
        "monthly_report": monthly_report,
        "profile": user,
        "id_confidence": id_confidence,
        "summary": {
            "uploads": total_uploads,
            "recent": recent_uploads,
            "statistics": stat_total,
        },
    }


@login_required(login_url="login")
def dashboard_view(request):
    user: CustomUser = request.user
    search_query = request.GET.get('search', '')
    form = UploadForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if user.is_staff or user.role == "admin":
            messages.error(request, "Administrators can only monitor submissions.")
            return redirect("dashboard")
        if form.is_valid():
            pending_upload = form.save(commit=False)
            pending_upload.user = user
            payload = {
                "idea": pending_upload.idea,
                "description": pending_upload.description or "",
                "file_type": pending_upload.file_type,
            }
            confidence = _predict_confidence(payload)
            pending_upload.prediction_confidence = confidence
            pending_upload.verdict = "Likely True" if confidence >= 60 else "Needs Review"
            pending_upload.save()
            messages.success(
                request,
                "Upload received. Confidence score prepared for your review.",
            )
            return redirect("dashboard")
        messages.error(
            request,
            "We could not save the upload. Please check the form for details.",
        )

    context = _collect_dashboard_data(user, search_query)
    context["form"] = form
    context["search_query"] = search_query
    return render(request, "dashboard.html", context)


@login_required(login_url="login")
def project_view(request):
    context = _collect_dashboard_data(request.user)
    return render(request, "project.html", context)


@login_required(login_url="login")
def statistics_view(request):
    context = _collect_dashboard_data(request.user)
    return render(request, "statistics.html", context)


@login_required(login_url="login")
def reports_view(request):
    context = _collect_dashboard_data(request.user)
    if not context["is_admin"]:
        return redirect("dashboard")
    
    now = timezone.now()
    selected_month = int(request.GET.get('month', now.month))
    selected_year = int(request.GET.get('year', now.year))
    
    context['monthly_report'] = Project.objects.filter(
        created_at__year=selected_year,
        created_at__month=selected_month,
    )
    context['selected_month'] = selected_month
    context['selected_year'] = selected_year
    context['year_range'] = range(2024, 2029)
    
    # Add all registered users and their login logs
    context['all_users'] = CustomUser.objects.all().order_by('-date_joined')
    context['recent_logins'] = UserLoginLog.objects.all()[:50]
    
    return render(request, "reports.html", context)


@login_required(login_url="login")
def upload_delete_view(request, pk):
    upload = get_object_or_404(Project, pk=pk)
    if not (request.user.is_staff or request.user.role == "admin"):
        messages.error(request, "Only administrators can delete uploads.")
        return redirect("dashboard")
    if request.method == "POST":
        public_id = upload.public_id
        upload.delete()
        messages.success(request, f"{public_id} removed.")
        return redirect("project")
    return render(
        request,
        "admin/upload_confirm_delete.html",
        {"upload": upload},
    )


@login_required(login_url="login")
def profile_view(request):
    context = _collect_dashboard_data(request.user)
    return render(request, "profile.html", context)


@login_required(login_url="login")
def logo_view(request):
    return render(request, "logo.html")


@login_required(login_url="login")
def poster_view(request):
    return render(request, "poster.html")


@login_required(login_url="login")
def advertisement_view(request):
    return render(request, "advertisement.html")


def welcome_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "welcome.html")
