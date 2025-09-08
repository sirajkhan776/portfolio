from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    full_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    website_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    photo_url = models.URLField(blank=True)
    resume_url = models.URLField(blank=True)

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    CATEGORY_CHOICES = (
        ("language", "Language"),
        ("framework", "Framework"),
        ("tool", "Tool"),
        ("cloud", "Cloud"),
        ("other", "Other"),
    )

    name = models.CharField(max_length=100, unique=True)
    level = models.CharField(max_length=50, blank=True, help_text="e.g. Beginner/Intermediate/Advanced")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="other")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name="projects")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date", "title"]

    def __str__(self):
        return self.title


class Experience(models.Model):
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.role} @ {self.company}"

    @property
    def is_current(self):
        return self.end_date is None


class Service(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    icon = models.CharField(max_length=32, blank=True, help_text="Emoji or short label, e.g. 🛠️")
    price = models.CharField(max_length=100, blank=True, help_text="e.g. $50/hr or Fixed")
    CATEGORY_CHOICES = (
        ("management", "Management"),
        ("normal", "Digital"),
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="normal")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class UserPreference(models.Model):
    THEME_CHOICES = (
        ("system", "System"),
        ("light", "Light"),
        ("dark", "Dark"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default="system")
    reduce_motion = models.BooleanField(default=False)
    ACCENT_CHOICES = (
        ("blue", "Blue"),
        ("green", "Green"),
        ("purple", "Purple"),
        ("orange", "Orange"),
        ("pink", "Pink"),
    )
    accent = models.CharField(max_length=10, choices=ACCENT_CHOICES, default="blue")
    DENSITY_CHOICES = (
        ("comfortable", "Comfortable"),
        ("compact", "Compact"),
    )
    density = models.CharField(max_length=12, choices=DENSITY_CHOICES, default="comfortable")
    SECTION_CHOICES = (
        ("home", "Home"),
        ("about", "About"),
        ("services", "Services"),
        ("projects", "Projects"),
        ("experience", "Experience"),
        ("skills", "Skills"),
    )
    default_section = models.CharField(max_length=16, choices=SECTION_CHOICES, default="home")
    show_email = models.BooleanField(default=True)
    show_phone = models.BooleanField(default=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"


# Create your models here.
