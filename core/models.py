from django.db import models
from django.utils.text import slugify

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.ImageField(upload_to='services/', blank=True)
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
    bio = models.TextField()
    image = models.ImageField(upload_to='team/')
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    client = models.CharField(max_length=100)
    date_completed = models.DateField()
    location = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/')
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
    abstract = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    publication_date = models.DateField()
    pdf_file = models.FileField(upload_to='publications/')
    cover_image = models.ImageField(upload_to='publication_covers/', blank=True, null=True)
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

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"