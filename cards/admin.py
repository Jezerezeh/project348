from django.contrib import admin
from .models import Card, Supertyperel, Subtyperel, CardTyperel

# Register your models here.
admin.site.register(Card)
admin.site.register(Subtyperel)
admin.site.register(Supertyperel)
admin.site.register(CardTyperel)