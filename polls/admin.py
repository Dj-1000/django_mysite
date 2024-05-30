from django.contrib import admin
from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display =('id','question_text')
    
admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)
