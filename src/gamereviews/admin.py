from django.contrib import admin

# Register your models here.
from .models import News
from .models import Reviews
from .models import Topgames, Slideshow

admin.site.register(News)
admin.site.register(Reviews)
admin.site.register(Topgames)
admin.site.register(Slideshow)