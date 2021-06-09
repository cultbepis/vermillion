from enum import Enum, auto

from django.db import models

class PortProtocol(Enum):
    HTTP = auto()
    TCP = auto()
    UDP = auto()

class Port:
    def __init__(self, number: int, protocol: PortProtocol) -> None:
        if number > 0 and number < 65536:
            self.number = number
        else:
            raise ValueError("Port number must be between 1 and 65535.")

        self.protocol = protocol

    def __str__(self):
        return f"{self.number}/{self.protocol.name.lower()}"

class PortField(models.CharField):
    description = "An exposed port to be consumed by Traefik's service discovery"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        name, proto = value.split('/')
        protocol = PortProtocol[proto.upper()]
        return Port(name, protocol)

    def to_python(self, value):
        if isinstance(value, Port) or value is None:
            return value

        name, proto = value.split('/')
        protocol = PortProtocol[proto.upper()]
        return Port(name, protocol)

    def get_prep_value(self, value):
        return '/'.join(value.name, value.protocol.name.lower())

# Models
class ContainerTemplate(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    image_url = models.CharField(max_length=4096, blank=False)

class ExposedPort(models.Model):
    template = models.ForeignKey('ContainerTemplate', on_delete=models.CASCADE, blank=False, related_name='exposed_ports', related_query_name='exposed_ports')
    port = PortField(blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['template', 'port'], name='unique_exposed_port_per_container_template')
        ]

class VolumeDefinition(models.Model):
    container_dir = models.CharField(max_length=4096, blank=False)
    required = models.BooleanField(default=True, blank=False)
    template = models.ForeignKey('ContainerTemplate', on_delete=models.CASCADE, blank=False, related_name='volume_definitions', related_query_name='volume_definitions')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['container_dir', 'template'], name='unique_container_dir_per_template')
        ]

class Volume(models.Model):
    host_dir = models.CharField(max_length=4096, blank=False)
    definition = models.ForeignKey('VolumeDefinition', on_delete=models.PROTECT, blank=False, related_name='volumes', related_query_name='volumes')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, blank=False, related_name='volumes', related_query_name='volumes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['host_dir', 'service'], name='unique_host_dir_per_service'),
            models.UniqueConstraint(fields=['definition', 'service'], name='unique_volume_definition_per_service'),
            models.UniqueConstraint(fields=['host_dir'], condition=models.Q(host_dir__startswith='/'), name='unique_absolute_host_dir')
        ]

class ServiceDefinition(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    templates = models.ManyToManyField('ContainerTemplate', related_name='service_definitions', related_query_name='service_definitions')

class Service(models.Model):
    (RUNNING, STOPPED, DECONSTRUCTED) = range(0, 3)
    STATE_CHOICES = (
        (RUNNING, 'Running'),
        (STOPPED, 'Stopped'),
        (DECONSTRUCTED, 'Deconstructed'),
    )

    name = models.CharField(max_length=30, unique=True, blank=False)
    definition = models.ForeignKey('ServiceDefinition', on_delete=models.PROTECT, blank=False, related_name='services', related_query_name='services')
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, default=DECONSTRUCTED, blank=False)

    def get_state(self):
        return STATE_CHOICES[self.state][1]

class ServicePortMapping(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, blank=False, related_name='port_mappings', related_query_name='port_mappings')
    container_port = models.ForeignKey('ExposedPort', on_delete=models.PROTECT, blank=False, related_name='service_mappings', related_query_name='service_mappings')
    traefik_port = PortField(blank=False, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['service', 'container_port'], name='unique_container_port_per_service'),
        ]
