from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone


class BaseReprModel(models.Model):

    class Meta:
        abstract = True

    def __repr__(self):
        field_names = [f.name for f in self._meta.fields]
        field_values = {f: getattr(self, f, None) for f in field_names}
        return f'<{self.__class__.__name__}: {field_values}>'


class Post(BaseReprModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.title

class Comment(BaseReprModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )

    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)

    post = models.ForeignKey(
        'Post', 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    
    def __str__(self):
        return self.text[:40]