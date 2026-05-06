from django.contrib import admin
from django.utils.html import format_html
from .models import Service, TeamMember, Project, BlogPost, Contact, NewsPost, Publication
from unfold.admin import ModelAdmin

# ── Site-level branding ────────────────────────────────────────────────────
admin.site.site_header  = "DDS Research & Consultancy"
admin.site.site_title   = "DDS Admin"
admin.site.index_title  = "Content Management Dashboard"


# ── Helpers ────────────────────────────────────────────────────────────────

def _status_badge(label, color):
    """Return a coloured pill badge for use in list_display."""
    colors = {
        "green":  ("#d1fae5", "#065f46", "#10b981"),
        "red":    ("#fee2e2", "#991b1b", "#dc2626"),
        "blue":   ("#dbeafe", "#1e40af", "#3b82f6"),
        "amber":  ("#fef3c7", "#92400e", "#f59e0b"),
        "slate":  ("#f1f5f9", "#475569", "#94a3b8"),
    }
    bg, text, border = colors.get(color, colors["slate"])
    return format_html(
        '<span style="'
        "display:inline-flex;align-items:center;gap:5px;"
        "padding:3px 10px;border-radius:99px;"
        "font-size:.72rem;font-weight:600;letter-spacing:.04em;"
        "background:{};color:{};border:1px solid {};"
        '">'
        '<span style="width:6px;height:6px;border-radius:50%;background:{};"></span>'
        "{}"
        "</span>",
        bg, text, border, border, label,
    )


# ── Service ────────────────────────────────────────────────────────────────
@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display  = ("title", "created_at", "updated_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("title",)

    fieldsets = (
        (None, {
            "fields": ("title", "slug", "description", "icon"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


# ── TeamMember ─────────────────────────────────────────────────────────────
@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display  = ("name", "position", "email", "order", "member_photo")
    list_editable = ("order",)
    search_fields = ("name", "position", "bio", "email")
    ordering      = ("order", "name")

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "position", "image", "email", "linkedin", "order"),
        }),
        ("Biography", {
            "fields": ("bio",),
        }),
        ("Professional Details", {
            "fields": ("professional_experience", "education", "skills", "certifications", "publications"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Photo")
    def member_photo(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:36px;height:36px;border-radius:50%;object-fit:cover;border:2px solid #e2e8f0;" />',
                obj.image.url,
            )
        return format_html('<span style="color:#94a3b8;font-size:.75rem;">No photo</span>')


# ── Project ────────────────────────────────────────────────────────────────
@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display   = ("title", "category", "client", "location", "date_completed", "featured", "featured_badge")
    list_editable  = ("featured",)  # keep the field available for inline edit
    list_filter    = ("category", "featured", "date_completed", "location")
    search_fields  = ("title", "description", "client", "location")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "date_completed"
    ordering       = ("-date_completed",)

    fieldsets = (
        ("Project Overview", {
            "fields": ("title", "slug", "category", "client", "location", "date_completed", "tags", "featured"),
        }),
        ("Content", {
            "fields": ("description", "image"),
        }),
    )

    @admin.display(description="Featured", ordering="featured")
    def featured_badge(self, obj):
        if obj.featured:
            return _status_badge("Featured", "green")
        return _status_badge("Standard", "slate")


# ── BlogPost ───────────────────────────────────────────────────────────────
@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):
    list_display   = ("title", "author", "created_at", "published", "publish_badge", "featured", "featured_badge")
    list_editable  = ("published", "featured")
    list_filter    = ("published", "featured", "created_at")
    search_fields  = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields  = ("author",)
    date_hierarchy = "created_at"
    ordering       = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Post Details", {
            "fields": ("title", "slug", "author", "image"),
        }),
        ("Content", {
            "fields": ("content",),
        }),
        ("Publishing", {
            "fields": ("published", "featured"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Status", ordering="published")
    def publish_badge(self, obj):
        if obj.published:
            return _status_badge("Published", "green")
        return _status_badge("Draft", "amber")

    @admin.display(description="Featured", ordering="featured")
    def featured_badge(self, obj):
        if obj.featured:
            return _status_badge("Featured", "blue")
        return format_html("—")


# ── NewsPost ───────────────────────────────────────────────────────────────
@admin.register(NewsPost)
class NewsPostAdmin(ModelAdmin):
    list_display  = ("title", "category_badge", "location", "date", "status", "status_badge")
    list_editable = ("status",)
    list_filter   = ("status", "category", "date", "location")
    search_fields = ("title", "content", "tags", "location")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "date"
    ordering      = ("-date",)

    fieldsets = (
        ("News Post Details", {
            "fields": ("title", "slug", "category", "location", "date", "status", "tags"),
        }),
        ("Media", {
            "fields": ("image",),
        }),
        ("Content", {
            "fields": ("content",),
        }),
    )

    CATEGORY_COLORS = {
        "announcement": "blue",
        "press_release": "green",
        "update": "slate",
        "event": "amber",
        "partnership": "blue",
    }

    @admin.display(description="Category", ordering="category")
    def category_badge(self, obj):
        label = dict(NewsPost.CATEGORY_CHOICES).get(obj.category, obj.category)
        color = self.CATEGORY_COLORS.get(obj.category, "slate")
        return _status_badge(label, color)

    @admin.display(description="Status", ordering="status")
    def status_badge(self, obj):
        if obj.status == "published":
            return _status_badge("Published", "green")
        return _status_badge("Draft", "amber")


# ── Publication ────────────────────────────────────────────────────────────
@admin.register(Publication)
class PublicationAdmin(ModelAdmin):
    list_display   = ("title", "authors", "category_badge", "publication_date", "featured_badge", "citation_count")
    list_filter    = ("category", "featured", "publication_date")
    search_fields  = ("title", "abstract", "authors", "keywords")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publication_date"
    ordering       = ("-publication_date",)

    fieldsets = (
        ("Publication Details", {
            "fields": ("title", "slug", "authors", "category", "publication_date", "institution", "doi"),
        }),
        ("Files & Media", {
            "fields": ("pdf_file", "cover_image"),
        }),
        ("Content", {
            "fields": ("abstract", "keywords"),
        }),
        ("Metrics & Visibility", {
            "fields": ("featured", "page_count", "citation_count"),
        }),
    )

    CATEGORY_COLORS = {
        "research_paper": "blue",
        "policy_brief":   "green",
        "report":         "amber",
        "case_study":     "slate",
        "working_paper":  "slate",
    }

    @admin.display(description="Category", ordering="category")
    def category_badge(self, obj):
        label = dict(Publication.CATEGORY_CHOICES).get(obj.category, obj.category)
        color = self.CATEGORY_COLORS.get(obj.category, "slate")
        return _status_badge(label, color)

    @admin.display(description="Featured", ordering="featured")
    def featured_badge(self, obj):
        if obj.featured:
            return _status_badge("Featured", "green")
        return format_html("—")


# ── Contact ────────────────────────────────────────────────────────────────
@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display   = ("name", "email", "subject", "created_at", "responded", "responded_badge")
    list_editable  = ("responded",)
    list_filter    = ("responded", "created_at")
    search_fields  = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)
    ordering       = ("-created_at",)

    fieldsets = (
        ("Contact Details", {
            "fields": ("name", "email", "subject"),
        }),
        ("Message", {
            "fields": ("message",),
        }),
        ("Status", {
            "fields": ("responded", "created_at"),
        }),
    )

    @admin.display(description="Status", ordering="responded")
    def responded_badge(self, obj):
        if obj.responded:
            return _status_badge("Responded", "green")
        return _status_badge("Pending", "amber")
