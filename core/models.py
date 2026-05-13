from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.conf import settings
from cloudinary.models import CloudinaryField

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    icon = CloudinaryField('icon', folder='services', blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = RichTextField()
    
    # --- FIXED ---
    # Changed from ImageField to CloudinaryField for direct, reliable integration.
    # The 'folder' attribute specifies the directory in your Cloudinary account.
    image = CloudinaryField('image', folder='team_members', overwrite=True, resource_type='image')
    
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    
    professional_experience = RichTextField(blank=True, null=True)
    skills = RichTextField(blank=True, null=True)
    certifications = RichTextField(blank=True, null=True)
    education = RichTextField(blank=True, null=True)
    publications = RichTextField(blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Project(models.Model):
    CATEGORY_CHOICES = (
        ('research', 'Research & Analysis'),
        ('evaluation', 'Monitoring & Evaluation'),
        ('data_collection', 'Data Collection'),
        ('strategy', 'Strategic Planning'),
        ('capacity_building', 'Capacity Building'),
        ('digital', 'Digital Solutions'),
        ('endline_evaluation', 'Endline Evaluation'),
        ('technical_consultancy', 'Technical Consultancy'),
        ('fiscal_policy', 'Fiscal Policy'),
        ('governance', 'Governance'),
        ('policy_advisory', 'Policy Advisory'),
        ('education', 'Education'),
        ('socio_economic', 'Socio-Economic Analysis'),
        ('human_rights', 'Human Rights'),
        ('poverty', 'Poverty & Development'),
        ('agriculture', 'Agriculture'),
        ('microfinance', 'Microfinance'),
        ('labour', 'Labour & Informal Economy'),
        ('climate', 'Climate Change'),
        ('health', 'Health'),
        
    )

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='research')
    description = RichTextField()
    image = CloudinaryField('image', folder='projects')
    client = models.CharField(max_length=100)
    date_completed = models.DateField()
    location = models.CharField(max_length=100)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags (e.g. Geospatial, Research)")
    slug = models.SlugField(unique=True, blank=True)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    image = CloudinaryField('image', folder='blog')
    author = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Publication(models.Model):
    CATEGORY_CHOICES = [
        ('research_paper', 'Research Paper'),
        ('policy_brief', 'Policy Brief'),
        ('report', 'Report'),
        ('case_study', 'Case Study'),
        ('working_paper', 'Working Paper'),
    ]

    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    abstract = RichTextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    publication_date = models.DateField()
    pdf_file = CloudinaryField('pdf', folder='publications', resource_type='raw')
    cover_image = CloudinaryField('image', folder='publication_covers', blank=True, null=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    keywords = models.CharField(max_length=255, help_text="Comma-separated keywords")
    doi = models.CharField(max_length=100, blank=True, verbose_name="DOI")
    institution = models.CharField(max_length=255, blank=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    citation_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-publication_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_keywords_list(self):
        return [keyword.strip() for keyword in self.keywords.split(',')]
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.keywords.split(',')] if self.keywords else []

class NewsPost(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    CATEGORY_CHOICES = (
        ('announcement', 'Announcement'),
        ('press_release', 'Press Release'),
        ('update', 'Project Update'),
        ('event', 'Event'),
        ('partnership', 'Partnership'),
    )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='update')
    location = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    image = CloudinaryField('image', folder='news', blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True) 
    date = models.DateField()
    content = RichTextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:news_detail', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []

    def __str__(self):
        return self.title

    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class JobVacancy(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full-time'),
        ('contract', 'Contract'),
        ('short_contract', 'Short Contract'),
        ('internship', 'Internship'),
        ('part_time', 'Part-time'),
    )

    title = models.CharField(max_length=200)
    description = RichTextField()
    application_form = models.URLField(blank=True, null=True, help_text="Link to the Google Form for applications")
    job_description_pdf = CloudinaryField('pdf', folder='job_descriptions', resource_type='raw', blank=True, null=True, help_text="Upload the full job description PDF")
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(max_length=100, default='Freetown, Sierra Leone')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    closing_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Job Vacancies"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:job_detail', kwargs={'slug': self.slug})