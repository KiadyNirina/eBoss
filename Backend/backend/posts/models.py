from django.db import models

# Create your models here.
class Post(models.Model) :
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_created=True)
    picture = models.ImageField(upload_to='images/post', null=True, blank=True)

    def __str__(self) -> str:
        return self.content
    
