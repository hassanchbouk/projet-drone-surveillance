from django.contrib import admin

# Register your models here.
from .models import Site, Zone, Mission, Waypoint, FlightSession, MissionLog


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "site")
    list_filter = ("type", "site")
    search_fields = ("name", "site__name")


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "site", "status", "trigger_type")
    list_filter = ("status", "trigger_type", "site")
    search_fields = ("name", "site__name")


@admin.register(Waypoint)
class WaypointAdmin(admin.ModelAdmin):
    list_display = ("id", "mission", "order_index", "x", "y", "z", "speed")
    list_filter = ("mission",)
    search_fields = ("mission__name",)
    ordering = ("mission", "order_index")


@admin.register(FlightSession)
class FlightSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "mission", "status", "start_time", "end_time")
    list_filter = ("status", "mission")
    search_fields = ("mission__name",)
    ordering = ("-start_time",)


@admin.register(MissionLog)
class MissionLogAdmin(admin.ModelAdmin):
    list_display = ("id", "flight_session", "event_type", "timestamp")
    list_filter = ("event_type",)
    search_fields = ("event_type", "message", "flight_session__mission__name")
    ordering = ("-timestamp",)