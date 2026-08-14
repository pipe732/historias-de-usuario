from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(bound_field, css_class):
    try:
        existing = bound_field.field.widget.attrs.get('class', '')
    except Exception:
        existing = ''
    new_class = (existing + ' ' + css_class).strip()
    attrs = {**bound_field.field.widget.attrs, 'class': new_class}
    return bound_field.as_widget(attrs=attrs)
