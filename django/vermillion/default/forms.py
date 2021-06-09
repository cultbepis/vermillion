import docker
from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models

# Form Components (Fields, Widgets, etc.)
class TraefikPortWidget(forms.MultiWidget):
    def __init__(self, attrs=None, visible=True):
        protocols = [proto.name for proto in models.PortProtocol]
        widgets = [
            forms.TextInput(attrs=attrs),
            forms.RadioSelect(attrs=attrs, choices=protocols)
        ]

        super().__init__(widgets, attrs)
        self.visible = visible

    def decompress(self, value):
        if isinstance(value, models.Port):
            return [value.number, value.protocol.name]
        elif isinstance(value, str):
            port, protocol = value.split('/')
            return [port, protocol.upper()]

        return [None, None]

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['visible'] = self.visible
        return context

    def render(self, name, value, attrs=None, renderer=None):
        if self.visible:
            return super().render(name, value, attrs, renderer)
        else:
            return ''

class TraefikPortField(forms.MultiValueField):
    def __init__(self, **kwargs):
        visible = kwargs.get('visible') if kwargs.get('visible', True) in [True, False] else True
        kwargs['widget'] = TraefikPortWidget(visible=visible)
        fields = (
            IntegerField(
                error_messages={
                    'required': 'This field is required.',
                    'incomplete': 'Enter a port number between 1 and 65535.',
                    'invalid': 'You must provide a port number between 1 and 65535.',
                    'min_value': 'Port number cannot be less than %(limit_value)s.',
                    'max_value': 'Port number cannot be greater than %(limit_value)s.',
                },
                min_value=1,
                max_value=65535
            ),
            ChoiceField(
                error_messages={
                    'required': 'This field is required.',
                    'invalid_choice': "'%(value)s' is not a valid choice."
                },
                choices=[(x.name, x.name) for x in models.PortProtocol]
            )
        )

        super().__init__(fields=fields, **kwargs)

    def compress(data_list):
        number, proto = data_list
        protocol = models.PortProtocol[proto]
        return models.Port(number, protocol)

# Forms
class ContainerTemplateForm(forms.ModelForm):
    ports = None

    class Meta:
        model = models.ContainerTemplate
        fields = ['name', 'image_url']

    def clean(self):
        on_docker_hub = True
        docker_hub_re = re.compile('[a-z0-9]+(?:/[a-z0-9]+')
        external_registry_re = re.compile('(?:http(?:s)?://)?(?:(?:[a-z0-9])+\.)?[a-z0-9]+\.[a-z0-9]+(?::[0-9]+)?(?:[a-z0-9/]+)?')

        if self.cleaned_data['image_url']:
            if docker_hub_re.match(self.cleaned_data['image_url']) || external_registry_re.match(self.cleaned_data['image_url']):
                try:
                    with docker.from_env() as client:
                        delete_image_after = False

                        try:
                            try:
                                img = client.images.get(name=self.cleaned_data['image_url'])
                            except docker.errors.ImageNotFound:
                                delete_image_after = True

                            image = client.images.pull(self.cleaned_data['image_url'])
                        except Exception as e:
                            # TODO: Log the real error, display generic error info.
                            raise ValidationError(_("Docker error: Failed to retrieve image."))

                        has_exposed_ports = image.attrs['Config'].get('ExposedPorts', None)
                        if has_exposed_ports:
                            for port in has_exposed_ports.keys():
                                self.ports.append(dict(zip('number', 'protocol'], port.split('/'))))

                        if delete_image_after:
                            client.images.remove(image=self.cleaned_data['image_url'])
                except Exception as e:
                    # TODO: Log the real error, display generic error info.
                    raise ValidationError(_("Docker error: Failed to spawn Docker client."))

        super().clean()

    def save(self):
        super().save()

        # TODO: Catch and log exceptions.
        # Add true-up process to fix missing ExposedPorts?
        for port_definition in self.ports:
            port = models.Port(port_definition['number'], models.PortProtocol[port_definition['protocol'].upper()])
            exposed_port = ExposedPort(template=self.instance, port=port)
            exposed_port.save()

class VolumeDefinitionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().init(*args, **kwargs)

        if not kwargs.get('instance', None) and not self.template := kwargs.get('template', None):
            raise TypeError(f"{type(self).__name__} requires either an existing instance ('instance' keyword argument) or a ContainerTemplate object ('template' keyword argument).")

    class Meta:
        model = models.VolumeDefinition
        exclude = ['template']

class ServiceDefinitionForm(forms.ModelForm):
    class Meta:
        model = models.ServiceDefinition
        fields = ['name', 'templates']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = models.Service
        exclude = ['state']

    def save():
        # TODO: Actually provision infrastructure here
        self.instance.state = models.Service.STOPPED
        super().save()

class ServicePortForm(forms.Form):
    container = forms.CharField(required=True, widget=forms.HiddenInput)
    container_port = forms.ChoiceField(required=True)
    traefik_port = TraefikPortField()
    activate_port_binding = forms.BooleanField(initial=False)

    def __init__(self, *, service, **kwargs):
        if not isinstance(service, models.Service):
            raise TypeError(f"{type(self).__name__} requires a Service object for the 'service' keyword argument.")
        self.service = service
        super().__init__(**kwargs)
