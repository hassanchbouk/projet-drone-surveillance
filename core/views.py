from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Site, Mission, Waypoint, FlightSession, MissionLog


DEMO_PREFIX = "Mission démo "


def is_demo_mission(mission):
    return mission.name.startswith(DEMO_PREFIX)


def get_next_demo_mission_name():
    demo_missions = Mission.objects.filter(name__startswith=DEMO_PREFIX)
    max_number = 0

    for mission in demo_missions:
        suffix = mission.name.replace(DEMO_PREFIX, "").strip()
        if suffix.isdigit():
            max_number = max(max_number, int(suffix))

    return f"{DEMO_PREFIX}{max_number + 1}"


def get_mission_status_label(status):
    labels = {
        "draft": "En attente",
        "planned": "En attente",
        "running": "En cours",
        "completed": "Terminée",
    }
    return labels.get(status, status)


def get_session_status_label(status):
    labels = {
        "planned": "Planifiée",
        "running": "En cours",
        "completed": "Terminée",
        "failed": "Échouée",
    }
    return labels.get(status, status)


def get_event_type_label(event_type):
    labels = {
        "mission_started": "Mission lancée",
        "waypoint_reached": "Waypoint atteint",
        "mission_completed": "Mission terminée",
    }
    return labels.get(event_type, event_type.replace("_", " ").capitalize())


def format_mission_for_display(mission):
    mission.display_status = get_mission_status_label(mission.status)
    mission.is_demo = is_demo_mission(mission)
    return mission


def format_session_for_display(session):
    session.display_status = get_session_status_label(session.status)
    return session


def format_log_for_display(log):
    log.display_event_type = get_event_type_label(log.event_type)
    return log


def dashboard(request):
    sites = Site.objects.all().order_by("name")

    real_missions = Mission.objects.exclude(name__startswith=DEMO_PREFIX).order_by("name")
    demo_missions = Mission.objects.filter(name__startswith=DEMO_PREFIX).order_by("name")

    real_missions_draft = [format_mission_for_display(m) for m in real_missions.filter(status__in=["draft", "planned"])]
    real_missions_running = [format_mission_for_display(m) for m in real_missions.filter(status="running")]
    real_missions_completed = [format_mission_for_display(m) for m in real_missions.filter(status="completed")]

    demo_missions_draft = [format_mission_for_display(m) for m in demo_missions.filter(status__in=["draft", "planned"])]
    demo_missions_running = [format_mission_for_display(m) for m in demo_missions.filter(status="running")]
    demo_missions_completed = [format_mission_for_display(m) for m in demo_missions.filter(status="completed")]

    recent_demo_sessions = [
        format_session_for_display(s)
        for s in FlightSession.objects.filter(mission__name__startswith=DEMO_PREFIX).order_by("-start_time")[:10]
    ]
    recent_real_sessions = [
        format_session_for_display(s)
        for s in FlightSession.objects.exclude(mission__name__startswith=DEMO_PREFIX).order_by("-start_time")[:10]
    ]

    recent_demo_logs = [
        format_log_for_display(l)
        for l in MissionLog.objects.filter(flight_session__mission__name__startswith=DEMO_PREFIX).order_by("-timestamp")[:10]
    ]
    recent_real_logs = [
        format_log_for_display(l)
        for l in MissionLog.objects.exclude(flight_session__mission__name__startswith=DEMO_PREFIX).order_by("-timestamp")[:10]
    ]

    return render(request, "core/dashboard.html", {
        "sites": sites,
        "real_missions_draft": real_missions_draft,
        "real_missions_running": real_missions_running,
        "real_missions_completed": real_missions_completed,
        "demo_missions_draft": demo_missions_draft,
        "demo_missions_running": demo_missions_running,
        "demo_missions_completed": demo_missions_completed,
        "recent_demo_sessions": recent_demo_sessions,
        "recent_real_sessions": recent_real_sessions,
        "recent_demo_logs": recent_demo_logs,
        "recent_real_logs": recent_real_logs,
    })


def site_list(request):
    sites = Site.objects.all().order_by("name")

    return render(request, "core/site_list.html", {
        "sites": sites,
    })


def mission_list(request):
    real_missions = Mission.objects.exclude(name__startswith=DEMO_PREFIX).order_by("name")
    demo_missions = Mission.objects.filter(name__startswith=DEMO_PREFIX).order_by("name")

    real_missions = [format_mission_for_display(m) for m in real_missions]
    demo_missions = [format_mission_for_display(m) for m in demo_missions]

    return render(request, "core/mission_list.html", {
        "real_missions": real_missions,
        "demo_missions": demo_missions,
    })


def mission_detail(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    mission = format_mission_for_display(mission)

    waypoints = Waypoint.objects.filter(mission=mission).order_by("order_index")
    flight_sessions = [
        format_session_for_display(s)
        for s in FlightSession.objects.filter(mission=mission).order_by("-start_time")
    ]
    mission_logs = [
        format_log_for_display(l)
        for l in MissionLog.objects.filter(flight_session__mission=mission).order_by("-timestamp")
    ]

    current_waypoint = None
    if mission.current_waypoint_index > 0:
        current_waypoint = waypoints.filter(order_index=mission.current_waypoint_index).first()

    return render(request, "core/mission_detail.html", {
        "mission": mission,
        "waypoints": waypoints,
        "flight_sessions": flight_sessions,
        "mission_logs": mission_logs,
        "current_waypoint": current_waypoint,
        "is_demo_mission": is_demo_mission(mission),
        "is_real_mission": not is_demo_mission(mission),
        "sites": Site.objects.all().order_by("name"),
    })


def create_demo_mission(request):
    if request.method == "POST":
        site_id = request.POST.get("site")
        mission_name = request.POST.get("name")
        x1 = request.POST.get("x1")
        y1 = request.POST.get("y1")
        z1 = request.POST.get("z1")
        x2 = request.POST.get("x2")
        y2 = request.POST.get("y2")
        z2 = request.POST.get("z2")

        site = get_object_or_404(Site, id=site_id)

        mission = Mission.objects.create(
            site=site,
            name=mission_name if mission_name else get_next_demo_mission_name(),
            status=Mission.MissionStatus.DRAFT,
            trigger_type=Mission.TriggerType.MANUAL,
            current_waypoint_index=0,
        )

        Waypoint.objects.create(
            mission=mission,
            x=float(x1),
            y=float(y1),
            z=float(z1),
            speed=1.0,
            order_index=1,
        )

        Waypoint.objects.create(
            mission=mission,
            x=float(x2),
            y=float(y2),
            z=float(z2),
            speed=1.0,
            order_index=2,
        )

        return redirect("mission_detail", mission_id=mission.id)

    return redirect("dashboard")


def launch_mission(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)

    if request.method == "POST" and mission.status in [
        Mission.MissionStatus.DRAFT,
        Mission.MissionStatus.PLANNED,
    ]:
        mission.status = Mission.MissionStatus.RUNNING
        mission.current_waypoint_index = 1
        mission.save()

        flight_session = FlightSession.objects.create(
            mission=mission,
            start_time=timezone.now(),
            status=FlightSession.FlightSessionStatus.RUNNING,
        )

        MissionLog.objects.create(
            flight_session=flight_session,
            timestamp=timezone.now(),
            event_type="mission_started",
            message=f"La mission « {mission.name} » a été lancée avec succès.",
        )

    return redirect("mission_detail", mission_id=mission.id)


def advance_mission(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)

    if mission.status == Mission.MissionStatus.COMPLETED:
        return redirect("mission_detail", mission_id=mission.id)

    waypoints = Waypoint.objects.filter(mission=mission).order_by("order_index")
    flight_session = FlightSession.objects.filter(mission=mission).order_by("-start_time").first()

    if request.method == "POST" and flight_session and mission.status == Mission.MissionStatus.RUNNING:
        next_index = mission.current_waypoint_index + 1

        if next_index <= waypoints.count():
            mission.current_waypoint_index = next_index
            mission.save()

            MissionLog.objects.create(
                flight_session=flight_session,
                timestamp=timezone.now(),
                event_type="waypoint_reached",
                message=f"La mission « {mission.name} » a atteint le waypoint {mission.current_waypoint_index}.",
            )
        else:
            mission.status = Mission.MissionStatus.COMPLETED
            mission.save()

            flight_session.status = FlightSession.FlightSessionStatus.COMPLETED
            flight_session.end_time = timezone.now()
            flight_session.save()

            MissionLog.objects.create(
                flight_session=flight_session,
                timestamp=timezone.now(),
                event_type="mission_completed",
                message=f"La mission « {mission.name} » est terminée avec succès.",
            )

    return redirect("mission_detail", mission_id=mission.id)