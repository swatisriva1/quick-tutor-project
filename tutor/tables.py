import django_tables2 as tables
import django_tables2 as TemplateColumn
from .models import Job

class tutorJobs(tables.Table):
    class Meta:
        model = Job
        template_name = "django_tables2/bootstrap4.html"
        fields = ("customer_profile", "subject", "course", "location", "notes")

    session = tables.TemplateColumn(template_name='tutor/beginSession.html')