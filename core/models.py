from django.db import models

# Create your models here.

class Site(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Zone(models.Model):
    class ZoneType(models.TextChoices):
        FORBIDDEN = "forbidden", "Forbidden"
        OBSTACLE = "obstacle", "Obstacle"

    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="zones",
    )
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=20,
        choices=ZoneType.choices,
    )
    geometry = models.TextField()

    class Meta:
        ordering = ["site__name", "name"]

    def __str__(self):
        return f"{self.name} ({self.type})"


class Mission(models.Model):
    class MissionStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        PLANNED = "planned", "Planned"
        RUNNING = "running", "Running"
        COMPLETED = "completed", "Completed"

    class TriggerType(models.TextChoices):
        MANUAL = "manual", "Manual"
        EVENT = "event", "Event"

    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name="missions",
    )
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=MissionStatus.choices,
        default=MissionStatus.DRAFT,
    )
    trigger_type = models.CharField(
        max_length=20,
        choices=TriggerType.choices,
        default=TriggerType.MANUAL,
    )
    current_waypoint_index = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["site__name", "name"]

    def __str__(self):
        return self.name


class Waypoint(models.Model):
    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name="waypoints",
    )
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    speed = models.FloatField()
    order_index = models.PositiveIntegerField()

    class Meta:
        ordering = ["mission", "order_index"]
        constraints = [
            models.UniqueConstraint(
                fields=["mission", "order_index"],
                name="unique_waypoint_order_per_mission",
            )
        ]

    def __str__(self):
        return f"{self.mission.name} - Waypoint {self.order_index}"


class FlightSession(models.Model):
    class FlightSessionStatus(models.TextChoices):
        PLANNED = "planned", "Planned"
        RUNNING = "running", "Running"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name="flight_sessions",
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=FlightSessionStatus.choices,
    )

    class Meta:
        ordering = ["-start_time"]

    def __str__(self):
        return f"Session {self.id} - {self.mission.name}"


class MissionLog(models.Model):
    flight_session = models.ForeignKey(
        FlightSession,
        on_delete=models.CASCADE,
        related_name="logs",
    )
    timestamp = models.DateTimeField()
    event_type = models.CharField(max_length=100)
    message = models.TextField()

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Log {self.id} - {self.event_type}"