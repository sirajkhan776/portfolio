from .models import Profile, Service, UserPreference


def profile(request):
    return {"profile": Profile.objects.first()}


def services_menu(request):
    try:
        management = list(Service.objects.filter(category="management").order_by("order", "title")[:6])
        normal = list(Service.objects.filter(category="normal").order_by("order", "title")[:6])
    except Exception:
        management, normal = [], []
    return {"services_menu": {"management": management, "normal": normal}}


def user_prefs(request):
    prefs = None
    if request.user.is_authenticated:
        try:
            prefs, _ = UserPreference.objects.get_or_create(user=request.user)
        except Exception:
            prefs = None
    return {"user_prefs": prefs}
