try:
    from ..codebase.html_base_code import *
except ImportError:
    from codebase.html_base_code import *
from termcolor import colored
from colorama import init
init()


django_unicorn_help_text = f"""\n
\n\n============ DJANGO UNICORN USAGE ===========
{django_unicorn_base_html}
Docs URL:\t{colored("https://www.django-unicorn.com/docs","green")}
\n\n=======================================\n\n
"""

django_tailwind_help_text = f"""\n
\n\n============ DJANGO TAILWIND USAGE ===========
{django_tailwind_base_html}
Docs URL:\t{colored("https://django-tailwind.readthedocs.io/en/latest/installation.html", "green")}
\n\n=======================================\n\n
"""

django_htmx_help_text = f"""\n
\n============ DJANGO HTMX USAGE ===========
{django_htmx_base_html}
Docs URL:\t{colored("https://django-htmx.readthedocs.io/en/latest/installation.html", "green")}
\n\n=======================================\n\n
"""

django_tailwind_crispy_help_text = """\n
\n============ DJANGO TAILWIND CRISPY USAGE ===========")
Current functionality allows the |crispy filter to be used to style your form. In your template:

    Load the filter: {% load tailwind_filters %}
    Apply the crispy filter: {{ form|crispy }}
Docs URL:\thttps://github.com/django-crispy-forms/crispy-tailwind
\n\n=======================================\n\n
"""


ckeditor_help_text = f"""\n
\n\n=======================================\n\n
Usage
Field

The quickest way to add rich text editing capabilities to your models is to use the included RichTextField model field type. A CKEditor widget is rendered as the form field but in all other regards the field behaves like the standard Django TextField. For example:

from django.db import models
from ckeditor.fields import RichTextField

class Post(models.Model):
    content = RichTextField()

For file upload support use RichTextUploadingField from ckeditor_uploader.fields.
Widget

Alternatively, you can use the included CKEditorWidget as the widget for a formfield. For example:

from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from post.models import Post

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

admin.site.register(Post, PostAdmin)

For file upload support use CKEditorUploadingWidget from ckeditor_uploader.widgets.

Docs URL:\t{colored("https://github.com/django-ckeditor/django-ckeditor", "green")}
\n\n=======================================\n\n
"""