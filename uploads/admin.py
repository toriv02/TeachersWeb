from django.contrib import admin
from teachers.models import *
from django.contrib.auth.admin import UserAdmin



@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CustmoUser)
class CustmoUserAdmin(UserAdmin):
    list_display = ('username','fio', 'school', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'fio', 'email', 'school__name') 
    list_filter = ('school','is_staff', 'is_active') 

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('fio', 'email', 'first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('School', {'fields': ('school',)}),
    )

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('headline', 'author',  'time', 'is_published')
    list_filter = ( 'is_published','subject')
    search_fields = ('headline', 'comment', 'author__username','author__first_name','author__last_name')
    date_hierarchy = 'time'
    
    fieldsets = (
        (None, {
            'fields': ('headline','comment', 'author','subject','is_published')
        }),
    )

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('records_FK', 'file')
    search_fields = ('records_FK__headline',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('records_FK', 'moderator', 'time')
    list_filter = ('moderator', )
    search_fields = ('content', 'records_FK__headline', 'moderator__username', 'moderator__first_name', 'moderator__last_name')
    date_hierarchy = 'time'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('records_FK', 'author', 'time')
    list_filter = ('author', )
    search_fields = ('content', 'records_FK__headline', 'author__username','author__first_name', 'author__last_name')
    date_hierarchy = 'time'

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('headline', 'description', 'ref')  
    search_fields = ('headline', 'description', 'ref') 
    readonly_fields = ('ref',)