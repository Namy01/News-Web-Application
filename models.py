from django.db import models
class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)
    Published_at = models.DateTimeField(null=True, blank = True)
    image = models.ImageField(upload_to="static/image", default="")

    def __str__(self):
        return self.title
    
# class User(models.Model):
#     user_name = models.CharField(max_length=50)
#     password = 

