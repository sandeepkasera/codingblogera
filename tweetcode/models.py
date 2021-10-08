from django.db import models


#custom
import random
from django.conf import settings 

User = settings.AUTH_USER_MODEL


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Posts",on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


# Create your models here.
class Posts(models.Model):
    #id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete = models.CASCADE) #many users can many posts
    title = models.TextField(blank=True,null=True)
    content = models.TextField(blank=True,null=True)
    image = models.FileField(upload_to='images/',blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    '''
    def __str__(self): 
        return self.content
    '''
    class Meta:
        ordering = ['-id']
    

    def serialize(self):
        '''
        Feel free to delete 
        '''
        return {
        "id":self.id,
        "content": self.content,
        }


