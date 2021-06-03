from django import forms
from models import Port, PortProtocol

class PortWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        protocols = [proto.name for proto in PortProtocol]
        widgets = [
            forms.TextInput(attrs=attrs),
            forms.RadioSelect(attrs=attrs, choices=protocols)
        ]

        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, Port):
            return [value.number, value.protocol.name]
        elif isinstance(value, str):
            port, protocol = value.split('/')
            return [port, protocol.upper()]

        return [None, None]

class PortField(forms.MultiValueField):
    def __init__(self, **kwargs):
        kwargs['widget'] = PortWidget
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
                choices=[(x.name, x.name) for x in PortProtocol]
            )
        )

        super().__init__(fields=fields, **kwargs)

    def compress(data_list):
        number, proto = data_list
        protocol = PortProtocol[proto]
        return Port(number, protocol)
