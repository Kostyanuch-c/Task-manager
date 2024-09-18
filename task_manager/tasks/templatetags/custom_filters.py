from django import template


register = template.Library()


@register.filter
def add_class(field, class_name):
    return field.as_widget(
        attrs={
            "class": " ".join((field.css_classes(), class_name)),
        },
    )


@register.filter
def get_attribute(obj, field_name):
    attribute = getattr(obj, field_name, '')
    if callable(attribute):
        return attribute()
    return attribute
