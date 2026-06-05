from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from .models import Service, TeamMember, Project, BlogPost, Contact, NewsPost, JobVacancy
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
        
        # --- Existing context data ---
        context['services'] = Service.objects.all()
        context['featured_projects'] = Project.objects.filter(featured=True).order_by('-date_completed')[:6]
        context['all_projects_count'] = Project.objects.count()
        context['latest_posts'] = BlogPost.objects.filter(published=True).order_by('-created_at')[:3]
        
        # --- CORRECTED LINE FOR NEWS TICKER ---
        # The news ticker template looks for the 'latest_news' variable.
        # This line fetches the 5 latest published news posts and adds them to the context.
        context['latest_news'] = NewsPost.objects.filter(status='published').order_by('-date')[:5]

        # Add the services list for the template
        context['services_list'] = [
            "Research & Analysis",
            "Policy Advisory", 
            "Strategic Planning",
            "M&E Services",
            "Capacity Building",
            "Project Design"
        ]

        # --- Your existing logic for carousel images ---
        # This logic remains unchanged.
        carousel_images = []
        for i in range(1, 6):  # Assuming you have 5 images named Picture1.jpg to Picture5.jpg
            image_path = f'carousel/Picture{i}.jpg'  # Use forward slashes for compatibility
            
            # This check is good for development where STATIC_ROOT might not be set
            full_path = None
            for static_dir in settings.STATICFILES_DIRS:
                potential_path = os.path.join(static_dir, 'images', image_path)
                if os.path.exists(potential_path):
                    full_path = potential_path
                    break
            
            static_url = f'images/{image_path}'
            carousel_images.append({
                'url': static_url,
                'alt': f'Slide {i}',
                'exists': full_path is not None
            })
        
        context['carousel_images'] = carousel_images
        return context
    
class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.all().order_by('order')[:3]

        # approach steps used by the spinning-ring section
        context['approach_steps'] = [
            {'title': 'Client-Centred',   'desc': 'Deep dive into your goals & constraints'},
            {'title': 'Collaborative',    'desc': 'Co-create solutions with stakeholders'},
            {'title': 'Research-Driven',  'desc': 'Evidence-based insights & analytics'},
            {'title': 'Results-Focused',  'desc': 'Implementation, M&E, and capacity-building'},
        ]

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

        # Apply category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

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

        # Get categories from model choices
        context['categories'] = Project.CATEGORY_CHOICES

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
    
class NewsListView(ListView):
    """
    Displays a list of all published news posts with pagination.
    """
    model = NewsPost
    template_name = 'pages/news_list.html' 
    context_object_name = 'news_posts'    
    paginate_by = 9

    def get_queryset(self):
        return NewsPost.objects.filter(status='published').order_by('-id')
    
class NewsDetailView(DetailView):
    """
    Displays a single news post.
    """
    model = NewsPost
    template_name = 'pages/news_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        """
        Ensure that only published posts can be viewed on the live site.
        """
        return NewsPost.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related news posts based on category, excluding the current post
        context['related_posts'] = NewsPost.objects.filter(
            status='published',
            category=self.object.category
        ).exclude(id=self.object.id)[:2]
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

                Thank you for contacting Development Decision Support (DDS). We have received your message and will get back to you shortly.

                Best regards,
                The DDS Team
                """

                send_mail(
                    subject='Thank you for contacting DDS',
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

class CareersView(TemplateView):
    template_name = 'pages/careers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies'] = JobVacancy.objects.filter(is_active=True).order_by('-closing_date')
        return context

class JobDetailView(DetailView):
    model = JobVacancy
    template_name = 'pages/job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Build the full URL for sharing
        context['full_url'] = self.request.build_absolute_uri()
        return context

class GlobalSearchView(ListView):
    template_name = 'pages/search_results.html'
    context_object_name = 'results'
    paginate_by = 12

    def get_queryset(self):
        from django.db.models import Value, CharField, Q
        from itertools import chain
        query = self.request.GET.get('q', '').strip()
        if not query:
            return []
        
        # Search News
        news = NewsPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published'
        ).annotate(type=Value('news', output_field=CharField()))
        
        # Search Projects
        projects = Project.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(client__icontains=query)
        ).annotate(type=Value('project', output_field=CharField()))
        
        # Search Publications
        publications = Publication.objects.filter(
            Q(title__icontains=query) | Q(abstract__icontains=query) | Q(authors__icontains=query)
        ).annotate(type=Value('publication', output_field=CharField()))
        
        # Combine results
        results = list(chain(news, projects, publications))
        
        # Sort by date (descending)
        def get_date(obj):
            return getattr(obj, 'date', getattr(obj, 'date_completed', getattr(obj, 'publication_date', None)))
        
        return sorted(results, key=lambda x: str(get_date(x) or ""), reverse=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
from django.http import JsonResponse
from django.urls import reverse

def search_suggestions(request):
    from django.db.models import Q
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})

    # Search News
    news = list(NewsPost.objects.filter(
        Q(title__icontains=query),
        status='published'
    ).values('title', 'slug')[:3])
    for item in news: item['type'] = 'news'

    # Search Projects
    projects = list(Project.objects.filter(
        Q(title__icontains=query)
    ).values('title', 'slug')[:3])
    for item in projects: item['type'] = 'project'

    # Search Publications
    publications = list(Publication.objects.filter(
        Q(title__icontains=query)
    ).values('title', 'slug')[:3])
    for item in publications: item['type'] = 'publication'

    from itertools import chain
    results = list(chain(news, projects, publications))
    
    # Simple mapping for URLs
    for item in results:
        if item['type'] == 'news':
            item['url'] = reverse('core:news_detail', kwargs={'slug': item['slug']})
        elif item['type'] == 'project':
            item['url'] = reverse('core:project_detail', kwargs={'slug': item['slug']})
        else:
            item['url'] = reverse('core:publication_detail', kwargs={'slug': item['slug']})

    return JsonResponse({'results': results})
