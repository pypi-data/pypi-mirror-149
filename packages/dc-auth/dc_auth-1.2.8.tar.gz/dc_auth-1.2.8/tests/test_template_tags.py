import pytest

from hypothesis import given
from hypothesis.strategies import text

import django.forms as forms
from django.template import Context, Template

from dc_auth.templatetags.dc_form_helpers import (
    is_textarea, is_checkbox, can_use_bulma_input,
)

TEST_TEMPLATE = Template("""
{% load dc_form_helpers %}
{{ field|add_class:css_class }}
""")


@given(text())
def test_add_class(css_class):
    rendered_str = TEST_TEMPLATE.render(Context({
        "field": "<div></div>",
        "css_class": css_class,
    }))
    expected_str = 'class="{}"'.format(css_class)
    assert expected_str in rendered_str


@pytest.mark.parametrize("field,textarea,checkbox,bulma_input",[
    [forms.BooleanField, False, True, False],
    [forms.CharField, False, False, True],
    [forms.ChoiceField, False, False, False],
    [forms.TypedChoiceField, False, False, False],
    [forms.DateField, False, False, True],
    [forms.DateTimeField, False, False, True],
    [forms.DecimalField, False, False, True],
    [forms.DurationField, False, False, True],
    [forms.EmailField, False, False, True],
    [forms.FileField, False, False, False],
    [forms.FloatField, False, False, True],
    [forms.ImageField, False, False, False],
    [forms.IntegerField, False, False, True],
    [forms.JSONField, True, False, False],
    [forms.GenericIPAddressField, False, False, True],
    [forms.MultipleChoiceField, False, False, False],
    [forms.TypedMultipleChoiceField, False, False, False],
    [forms.NullBooleanField, False, False, False],
    [forms.SlugField, False, False, True],
    [forms.TimeField, False, False, True],
    [forms.URLField, False, False, True],
    [forms.UUIDField, False, False, True],
])
def test_widget_checkers(field, textarea, checkbox, bulma_input):
    class TestForm(forms.Form):
        field_instance = field()
    form = TestForm()
    for f in form:
        assert is_textarea(f) is textarea, "is_textarea"
        assert is_checkbox(f) is checkbox, "is_checkbox"
        assert can_use_bulma_input(f) is bulma_input, "can_use_bulma_input"
