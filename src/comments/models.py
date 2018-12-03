from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from gamereviews.models import Reviews
# Create your models here.

class Comment(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    #gamereview      = models.ForeignKey(Reviews,null=True   )

    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id       = models.PositiveIntegerField(null=True)
    content_object  = GenericForeignKey('content_type', 'object_id')

    comment_content = models.TextField()
    timestamp       = models.DateTimeField(auto_now_add=True)
