from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from .models import Profile, Skill, Project, Experience, Service
from .forms import RegisterForm, UserPreferenceForm
from django.contrib import messages
import io



def index(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    # Group skills by category for display
    skills_by_category = {}
    for s in skills:
        skills_by_category.setdefault(s.get_category_display(), []).append(s)

    if request.user.is_authenticated:
        projects = Project.objects.prefetch_related("skills").all()
        experiences = Experience.objects.all()
    else:
        projects = Project.objects.none()
        experiences = Experience.objects.none()
    services_management = Service.objects.filter(category="management")
    services_normal = Service.objects.filter(category="normal")

    context = {
        "profile": profile,
        "skills_by_category": skills_by_category,
        "projects": projects,
        "experiences": experiences,
        "services_management": services_management,
        "services_normal": services_normal,
    }
    return render(request, "siteapp/index.html", context)


@login_required
def preferences(request):
    if request.user.is_anonymous:
        return redirect("login")
    from .models import UserPreference
    prefs, _ = UserPreference.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserPreferenceForm(request.POST, instance=prefs)
        if form.is_valid():
            form.save()
            messages.success(request, "Preferences saved")
            return redirect("preferences")
    else:
        form = UserPreferenceForm(instance=prefs)
    return render(request, "siteapp/preferences.html", {"form": form})


def profile_page(request):
    profile = Profile.objects.first()
    if not profile:
        raise Http404("Profile not found")
    return render(request, "siteapp/profile.html", {"profile": profile})


def download_profile(request):
    profile = Profile.objects.first()
    if not profile:
        return JsonResponse({"error": "No profile"}, status=404)
    data = {
        "full_name": profile.full_name,
        "title": profile.title,
        "bio": profile.bio,
        "location": profile.location,
        "email": profile.email,
        "phone": profile.phone,
        "website_url": profile.website_url,
        "github_url": profile.github_url,
        "linkedin_url": profile.linkedin_url,
        "photo_url": profile.photo_url,
        "resume_url": profile.resume_url,
    }
    response = JsonResponse(data)
    response["Content-Disposition"] = 'attachment; filename="profile.json"'
    return response


def download_vcard(request):
    profile = Profile.objects.first()
    if not profile:
        raise Http404("Profile not found")

    def esc(text: str) -> str:
        return text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")

    full_name = profile.full_name or ""
    parts = full_name.split()
    first = parts[0] if parts else ""
    last = parts[-1] if len(parts) > 1 else ""

    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{esc(last)};{esc(first)};;;",
        f"FN:{esc(full_name)}",
    ]
    if profile.title:
        lines.append(f"TITLE:{esc(profile.title)}")
    if profile.location:
        lines.append(f"ADR;TYPE=HOME:;;{esc(profile.location)};;;")
    if profile.email:
        lines.append(f"EMAIL;TYPE=INTERNET,WORK:{esc(profile.email)}")
    if profile.phone:
        lines.append(f"TEL;TYPE=CELL:{esc(profile.phone)}")
    if profile.website_url:
        lines.append(f"URL;TYPE=WORK:{esc(profile.website_url)}")
    if profile.github_url:
        lines.append(f"X-SOCIALPROFILE;TYPE=github:{esc(profile.github_url)}")
    if profile.linkedin_url:
        lines.append(f"X-SOCIALPROFILE;TYPE=linkedin:{esc(profile.linkedin_url)}")
    if profile.photo_url:
        lines.append(f"PHOTO;VALUE=URI:{esc(profile.photo_url)}")
    if profile.bio:
        lines.append(f"NOTE:{esc(profile.bio)}")

    lines.append("END:VCARD")
    content = "\r\n".join(lines) + "\r\n"

    resp = HttpResponse(content, content_type="text/vcard; charset=utf-8")
    resp["Content-Disposition"] = 'attachment; filename="contact.vcf"'
    return resp


def download_profile_pdf(request):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch

    profile = Profile.objects.first()
    if not profile:
        raise Http404("Profile not found")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - inch
    left = inch

    # Header
    p.setTitle(f"{profile.full_name} – Profile")
    p.setFont("Helvetica-Bold", 18)
    p.drawString(left, y, profile.full_name)
    y -= 22
    if profile.title:
        p.setFont("Helvetica", 12)
        p.drawString(left, y, profile.title)
        y -= 18

    # Contact info
    p.setFont("Helvetica", 10)
    def put(line: str):
        nonlocal y
        if y < inch:
            p.showPage()
            y = height - inch
            p.setFont("Helvetica", 10)
        p.drawString(left, y, line)
        y -= 14

    if profile.email:
        put(f"Email: {profile.email}")
    if profile.phone:
        put(f"Phone: {profile.phone}")
    if profile.website_url:
        put(f"Website: {profile.website_url}")
    if profile.github_url:
        put(f"GitHub: {profile.github_url}")
    if profile.linkedin_url:
        put(f"LinkedIn: {profile.linkedin_url}")
    if profile.location:
        put(f"Location: {profile.location}")

    y -= 6

    # Summary
    if profile.bio:
        p.setFont("Helvetica-Bold", 12)
        put("Summary")
        p.setFont("Helvetica", 10)
        for line in profile.bio.splitlines() or [profile.bio]:
            put(line)
        y -= 6

    # Experience
    experiences = Experience.objects.all()[:6]
    if experiences:
        p.setFont("Helvetica-Bold", 12)
        put("Experience")
        p.setFont("Helvetica", 10)
        for exp in experiences:
            dates = f"{exp.start_date.strftime('%b %Y')} – {(exp.end_date.strftime('%b %Y') if exp.end_date else 'Present')}"
            put(f"{exp.role} · {exp.company} ({dates})")
            if exp.location:
                put(f"  {exp.location}")
            if exp.description:
                for line in exp.description.splitlines():
                    put(f"  {line}")
            y -= 4

    # Skills
    skills = Skill.objects.all()[:24]
    if skills:
        p.setFont("Helvetica-Bold", 12)
        put("Skills")
        p.setFont("Helvetica", 10)
        names = " • ".join(s.name for s in skills)
        # wrap roughly at page width
        max_chars = 90
        for i in range(0, len(names), max_chars):
            put(names[i:i+max_chars])
        y -= 4

    # Projects
    projects = Project.objects.all()[:5]
    if projects:
        p.setFont("Helvetica-Bold", 12)
        put("Projects")
        p.setFont("Helvetica", 10)
        for pr in projects:
            put(f"{pr.title}")
            if pr.description:
                for line in pr.description.splitlines():
                    put(f"  {line}")
            if pr.project_url:
                put(f"  Live: {pr.project_url}")
            if pr.repo_url:
                put(f"  Repo: {pr.repo_url}")
            y -= 4

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = 'attachment; filename="profile.pdf"'
    return resp


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data.get("email") or "",
                password=form.cleaned_data["password1"],
            )
            auth_login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "siteapp/register.html", {"form": form})


# Create your views here.
