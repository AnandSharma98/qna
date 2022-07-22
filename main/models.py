from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
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
    likes = models.ManyToManyField(User, related_name='question_likes')  # it's like M:N relationship: where one row can refer to many row of another table and vice versa (a user can  like many questions, a question can have many likes)
    tags = TaggableManager()

    # auto_now_add will set time when an instance is created whereas auto_now will set time when someone modified his instance.
    # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()   

    def get_responses(self):
        return self.responses.filter(parent=None) # see link of gfg , jo related_name=responses dia h na , usi ki vjh se self.responses likh ke b Response ke objects ko access kr paa re h



class Response(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)  # one row of table referring to many row of another table (bole toh multiple response ka same user ho skte h )
 # https://www.geeksforgeeks.org/related_name-django-built-in-field-validation/#:~:text=The%20related_name%20attribute%20specifies%20the,model%20back%20to%20your%20model.
 # about this related_name   
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE, related_name='responses')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)  # parent of response, self islie kuki ek response ka parent response he ho skta h , ya agr vo question ka reply h toh null b chlega
    body = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="response_likes")

    def __str__(self):
        return self.body

    def total_likes(self):
        return self.likes.count()

    def get_responses(self):
        return Response.objects.filter(parent=self)

        


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # one row of table referring to only single row of another table
    avatar = CloudinaryField('image')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

# https://dev.to/earthcomfy/django-user-profile-3hik        