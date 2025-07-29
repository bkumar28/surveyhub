from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(value, css_class):
    """
    Add specified CSS class to an HTML form field widget.

    Usage:
    {{ form.field|add_class:"form-control" }}
    """
    if value.startswith("<select"):
        return value.replace("<select", f'<select class="{css_class}"')
    elif value.startswith("<input"):
        if 'type="checkbox"' in value:
            return value.replace("<input", '<input class="form-check-input"')
        elif 'type="radio"' in value:
            return value.replace("<input", '<input class="form-check-input"')
        else:
            return value.replace("<input", f'<input class="{css_class}"')
    elif value.startswith("<textarea"):
        return value.replace("<textarea", f'<textarea class="{css_class}"')
    return value
