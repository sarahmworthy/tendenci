from django.http import Http404

def blog_disabled(request):
    raise Http404