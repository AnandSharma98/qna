from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from taggit.managers import TaggableManager
from django_resized import ResizedImageField
from cloudinary.models import CloudinaryField
# Create your models here.


class Question(models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    body = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = CloudinaryField('image')
    
    url = models.URLField(blank=True)
    likes = models.ManyToManyField(User, related_name='questions')
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()

    # auto_now_add will set time when an instance is created whereas auto_now will set time when someone modified his instance.
    # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()   

    def get_responses(self):
        return self.responses.filter(parent=None) # see link of gfg , jo related_name=responses dia h na , usi ki vjh se self.responses likh ke b Response ke objects ko access kr paa re h


        # it overrides the saving behaviour, basically resizing the image going to be saved



class Response(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
 # https://www.geeksforgeeks.org/related_name-django-built-in-field-validation/#:~:text=The%20related_name%20attribute%20specifies%20the,model%20back%20to%20your%20model.
 # about this related_name   
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE, related_name='responses')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)  # parent of response, self islie kuki ek response ka parent response he ho skta h , ya agr vo question ka reply h toh null b chlega
    body = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='responses')

    def __str__(self):
        return self.body

    def total_likes(self):
        return self.likes.count()

    def get_responses(self):
        return Response.objects.filter(parent=self)

        


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = CloudinaryField('image')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # # it overrides the saving behaviour, basically resizing the image going to be saved
    # def save(self, *args, **kwargs):
    #     super().save()

    #     img = CloudinaryField('image')

    #     if img.height > 100 or img.width > 100:
    #         new_img = (100, 100)
    #         img.thumbnail(new_img)
    #         img.save(self.avatar.path)    

# https://dev.to/earthcomfy/django-user-profile-3hik        