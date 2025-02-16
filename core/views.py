from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from .models import Service, TeamMember, Project, BlogPost, Contact
from django.db.models.functions import ExtractYear
from django.conf import settings
from .forms import ContactForm
from django.db.models import Q
from .models import Publication
from django.views.generic import DetailView
import os

class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()[:3]
        context['featured_projects'] = Project.objects.filter(featured=True)[:3]
        context['latest_posts'] = BlogPost.objects.filter(published=True).order_by('-created_at')[:3]

        # Define image paths and verify they exist
        carousel_images = []
        for i in range(1, 6):  # Assuming you have 5 images named Picture1.jpg to Picture5.jpg
            image_path = f'carousel/Picture{i}.jpg'  # Use forward slashes for compatibility
            
            if settings.STATIC_ROOT:
                full_path = os.path.join(settings.STATIC_ROOT, 'images', image_path)
            else:
                # Check in STATICFILES_DIRS if STATIC_ROOT is not set
                full_path = os.path.join(settings.STATICFILES_DIRS[0], 'images', image_path)
            
            static_url = f'images/{image_path}'
            carousel_images.append({
                'url': static_url,
                'alt': f'Slide {i}',
                'exists': os.path.exists(full_path)
            })
        
        context['carousel_images'] = carousel_images
        return context

class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.all()
        return context

class TeamView(ListView):
    model = TeamMember
    template_name = 'pages/team.html'
    context_object_name = 'team_members'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group team members by their roles
        context['leadership_team'] = TeamMember.objects.filter(position__icontains='Director').order_by('order')
        context['research_team'] = TeamMember.objects.filter(position__icontains='Researcher').order_by('order')
        context['data_team'] = TeamMember.objects.filter(position__icontains='Data').order_by('order')
        context['operations_team'] = TeamMember.objects.filter(
            position__icontains='Operations').order_by('order')
        return context

class TeamMemberDetailView(DetailView):
    model = TeamMember
    template_name = 'team_member_detail.html'
    context_object_name = 'member'

class ServicesView(ListView):
    template_name = 'pages/services.html'
    model = Service
    context_object_name = 'services'

class ServiceDetailView(DetailView):
    template_name = 'pages/service_detail.html'
    model = Service
    context_object_name = 'service'

class ProjectListView(ListView):
    template_name = 'pages/projects.html'
    model = Project
    context_object_name = 'projects'
    paginate_by = 9
    
    def apply_filters(self, queryset):
        # Apply search filter
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                title__icontains=search_query) | queryset.filter(
                description__icontains=search_query)

        # Apply location filter
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location=location)

        # Apply year filter
        year = self.request.GET.get('year')
        if year:
            queryset = queryset.filter(date_completed__year=year)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get unique locations
        context['locations'] = Project.objects.values_list(
            'location', flat=True).distinct().order_by('location')

        # Get unique years from date_completed
        context['years'] = Project.objects.annotate(
            year=ExtractYear('date_completed')
        ).values_list('year', flat=True).distinct().order_by('-year')

        # Get featured projects with the same filters applied
        featured_queryset = Project.objects.filter(featured=True)
        featured_queryset = self.apply_filters(featured_queryset)
        context['featured_projects'] = featured_queryset.order_by('-date_completed')[:2]

        return context

    def get_queryset(self):
        # Get all projects and apply filters
        queryset = Project.objects.all().order_by('-date_completed')
        return self.apply_filters(queryset)

class ProjectDetailView(DetailView):
    template_name = 'pages/project_detail.html'
    model = Project
    context_object_name = 'project'

class BlogListView(ListView):
    template_name = 'pages/blog.html'
    model = BlogPost
    context_object_name = 'posts'
    paginate_by = 6
    queryset = BlogPost.objects.filter(published=True)

class BlogDetailView(DetailView):
    template_name = 'pages/blog_detail.html'
    model = BlogPost
    context_object_name = 'post'

    def get_queryset(self):
        return BlogPost.objects.filter(published=True)

class PublicationListView(ListView):
    model = Publication
    template_name = 'pages/publications.html'
    context_object_name = 'publications'
    paginate_by = 9

    def get_queryset(self):
        queryset = Publication.objects.all()
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        year = self.request.GET.get('year')

        if category:
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(abstract__icontains=search) |
                Q(authors__icontains=search) |
                Q(keywords__icontains=search)
            )
        if year:
            queryset = queryset.filter(publication_date__year=year)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Publication.CATEGORY_CHOICES
        context['years'] = Publication.objects.dates('publication_date', 'year', order='DESC')
        context['featured_publications'] = Publication.objects.filter(featured=True)[:3]
        return context

class PublicationDetailView(DetailView):
    model = Publication
    template_name = 'pages/publication_detail.html'
    context_object_name = 'publication'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related publications based on category
        related = Publication.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        context['related_publications'] = related
        return context

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email notification
            try:
                # Email to admin
                admin_message = f"""
                New contact form submission:
                
                Name: {contact.name}
                Email: {contact.email}
                Subject: {contact.subject}
                Message: {contact.message}
                """
                
                send_mail(
                    subject=f'New Contact Form Submission: {contact.subject}',
                    message=admin_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )

                # Auto-reply to user
                user_message = f"""
                Dear {contact.name},

                Thank you for contacting Laterite. We have received your message and will get back to you shortly.

                Best regards,
                The Laterite Team
                """
                
                send_mail(
                    subject='Thank you for contacting Laterite',
                    message=user_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[contact.email],
                    fail_silently=False,
                )

            except Exception as e:
                # Log the error but don't show it to the user
                print(f"Error sending email: {e}")

            messages.success(request, 'Your message has been sent successfully! We will contact you soon.')
            return redirect('core:contact')
    else:
        form = ContactForm()
    
    return render(request, 'pages/contact.html', {'form': form})

# class TeamView(ListView):
#     template_name = 'pages/team.html'
#     model = TeamMember
#     context_object_name = 'team_members'

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

class PrivacyPolicyView(TemplateView):
    template_name = 'pages/privacy_policy.html'

class TermsOfServiceView(TemplateView):
    template_name = 'pages/terms_of_service.html'

class CookiePolicyView(TemplateView):
    template_name = 'pages/cookie_policy.html'