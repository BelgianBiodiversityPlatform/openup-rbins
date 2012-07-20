from django.shortcuts import render_to_response
from django.template import RequestContext
from website.models import Family, Picture, Species

def my_render(template_path, request_obj, context={}):
    return render_to_response(template_path, context, context_instance=RequestContext(request_obj))

def index(request):
    families = Family.objects.all()
    
    metrics = {
        'pictures': Picture.objects.count(),
        'families': Family.objects.count(),
        'species': Species.objects.count()}
    
    return my_render('index.html', request, {
        'families': families,
        'metrics': metrics
        })
    
    
    