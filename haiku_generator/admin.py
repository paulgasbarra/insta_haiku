from django.contrib import admin
from .models import Haiku

class HaikuAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Haiku, HaikuAdmin)
