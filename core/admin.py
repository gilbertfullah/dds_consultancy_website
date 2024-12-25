from django.contrib import admin
from .models import Service, TeamMember, Project, BlogPost, Contact

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'email', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'position', 'bio')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'date_completed', 'featured')
    list_editable = ('featured',)
    list_filter = ('featured', 'date_completed')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description', 'client')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published', 'featured')
    list_editable = ('published', 'featured')
    list_filter = ('published', 'featured', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'responded')
    list_editable = ('responded',)
    list_filter = ('responded', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)