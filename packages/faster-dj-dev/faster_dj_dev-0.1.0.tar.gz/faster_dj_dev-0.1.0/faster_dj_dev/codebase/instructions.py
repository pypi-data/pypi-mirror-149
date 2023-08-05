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