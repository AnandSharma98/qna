from django import template
from main.models import  Response

register = template.Library() # module-level variable named register that is a template.Library instance, in which all the tags and filters are registered.

@register.filter(name="che")  #  registering to make it available to Django’s template language:
def che(user, response_id):
    response = Response.objects.get(id=response_id)
    return response.likes.filter(id=user.id).exists()  