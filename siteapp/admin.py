from django.contrib import admin
from .models import Profile, Skill, Project, Experience, Service, UserPreference


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "title", "location", "email")
    search_fields = ("full_name", "title", "location", "email")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "level", "order")
    list_editable = ("order",)
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "project_url", "repo_url", "order")
    list_editable = ("order",)
    search_fields = ("title", "description")
    filter_horizontal = ("skills",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "start_date", "end_date", "order")
    list_editable = ("order",)
    search_fields = ("role", "company", "description")
    list_filter = ("company",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "icon", "price", "order")
    list_editable = ("order",)
    list_filter = ("category",)
    search_fields = ("title", "summary")


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "theme", "reduce_motion")
    list_filter = ("theme", "reduce_motion")


# Register your models here.
