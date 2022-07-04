from django import template
from django.contrib.auth.models import User
from main.models import Question, Response

register = template.Library()

@register.filter(name="che")
def che(user, response_id):
    response = Response.objects.get(id=response_id)
    return response.likes.filter(id=user.id).exists()  