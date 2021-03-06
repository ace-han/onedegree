from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return TemplateResponse(request, 'index.html')


def admin_index(request):
    return TemplateResponse(request, 'admin_index.html')