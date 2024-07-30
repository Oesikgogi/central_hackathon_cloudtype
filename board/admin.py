# community/board/admin.py

from django.contrib import admin
from .models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)

"""
from .models import Board

class BoardAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(Board, BoardAdmin)
"""
