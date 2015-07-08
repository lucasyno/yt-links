# -*- coding: utf-8 -*-
import string
from django import forms
from django.core.urlresolvers import reverse

from .models import Owner, Link
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, ButtonHolder
from crispy_forms.bootstrap import StrictButton


class LinkEditForm(forms.ModelForm):
    class Meta:
	model = Link
	fields = ['link', ]

    def __init__(self, *args, **kwargs):
        super(LinkEditForm, self).__init__(*args, **kwargs)
	self.fields['link'].required = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'link',
            ButtonHolder(
	        Submit('Add link','Add link', css_class='btn-primary')))

            
class OwnerEditForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['gen_hash',]

    def __init__(self, *args, **kwargs):
        super(OwnerEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tags = True
        self.helper.layout = Layout(
            'gen_hash',
            ButtonHolder(
                Submit('change', 'Change', css_class='btn-primary')))

    def clean(self):
        d = self.cleaned_data
	if len(d['gen_hash'])>25:
	     raise forms.ValidationError('Please, use max 25 characters')
        allowed_letters = ''.join((string.lowercase, string.uppercase))
        for char in d['gen_hash']:
            if char not in allowed_letters:
                raise forms.ValidationError('Please, type only ASCII letters')
        if Owner.objects.filter(gen_hash=d['gen_hash']).exists():
        	raise forms.ValidationError('This name already exists, please type other')
        return d

