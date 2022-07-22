from django import template
from main.models import  Response

register = template.Library()

@register.filter(name="che")
def che(user, response_id):
    response = Response.objects.get(id=response_id)
    return response.likes.filter(id=user.id).exists()  