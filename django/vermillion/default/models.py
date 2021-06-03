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

# Models start here

class ContainerTemplate(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    image_url = models.URLField(blank=False)
    exposed_port = PortField(blank=False)

class VolumeDefinition(models.Model):
    container_dir = models.CharField(max_length=4096, blank=False)
    required = models.BooleanField(default=True, blank=False)
    template = models.ForeignKey('ContainerTemplate', on_delete=models.CASCADE, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['container_dir', 'template'], name='unique_container_dir_per_template')
        ]

class Volume(models.Model):
    host_dir = models.CharField(max_length=4096, blank=False, unique=True)
    definition = models.ForeignKey('VolumeDefinition', on_delete=models.PROTECT, blank=False)
    service = models.ForeignKey('Service', on_delete=models.CASCADE, blank=False)

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
    name = models.CharField(max_length=30, unique=True, blank=False)
    definition = models.ForeignKey('ServiceDefinition', on_delete=models.PROTECT, blank=False)
