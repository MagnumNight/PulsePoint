from django import template

# Variable: register - The template library
register = template.Library()

# Function: class_name - Returns the class name of a given object
@register.filter
def class_name(value):
    return value.__class__.__name__
