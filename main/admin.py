from django.contrib import admin

from .models import Word, ChatID

class WordAdmin(admin.ModelAdmin):
    list_filter = ('word', 'is_meaningful',)
    list_display = ('word', 'is_meaningful',)

# class ChatIDAdmin(admin.ModelAdmin):
#     # list_filter = ('chat_id')
#     list_display = ('chat_id',)


admin.site.register(Word, WordAdmin)
admin.site.register(ChatID)
