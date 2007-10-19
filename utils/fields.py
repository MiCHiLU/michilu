from django import newforms as forms
from django.newforms.util import ValidationError
from django.utils.translation import ugettext
from utils import has_surrogate_pair


class CharField(forms.CharField):
    def __init__(self, surrogate_pair=True, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)
        self.surrogate_pair = surrogate_pair

    def clean(self, value):
        value = super(CharField, self).clean(value)
        if not self.surrogate_pair and has_surrogate_pair(value):
            raise ValidationError(ugettext(u'Ensure this value has not surrogate pair characters.'))
        return value

