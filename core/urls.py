from django.urls import path
from .views import TeamMemberDetailView
from . import views

app_name = 'core'

urlpatterns = [
    # Main pages
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('team/', views.TeamView.as_view(), name='team'),
    path('contact/', views.contact_view, name='contact'),
    
    # Services
    path('services/', views.ServicesView.as_view(), name='services'),
    path('services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    
    # Projects
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    
    # Blog
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    
    # Publication
    path('publications/', views.PublicationListView.as_view(), name='publications'),
    path('publications/<slug:slug>/', views.PublicationDetailView.as_view(), name='publication_detail'),
    
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    # Privacy Policy
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy'),
    
    # Terms of Service
    path('terms-of-service/', views.TermsOfServiceView.as_view(), name='terms'),
    
    # Team
    path('team/<int:pk>/', TeamMemberDetailView.as_view(), name='team_member_detail'),
    
    # Cookie Policy
    path('cookie-policy/', views.CookiePolicyView.as_view(), name='cookie-policy'),
]