from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from website.models import Family, Picture, Species

def my_render(template_path, request_obj, context={}):
    return render_to_response(template_path, context, context_instance=RequestContext(request_obj))

def search(request):
    # Save query parameters
    family_id = request.GET.get('family_id')
    
    page = request.GET.get('page')
    
    # Filtering based on query parameters
    pictures_list = Picture.objects.all()
    if family_id:
        pictures_list = pictures_list.filter(family_id__exact = family_id)
        
    # Paginate
    paginator = Paginator(pictures_list, 6) # TODO: move to settings
    
    try:
        pictures = paginator.page(page)
    except PageNotAnInteger: 
        pictures = paginator.page(1) # If page is not an integer, deliver first page.
    except EmptyPage: # If page is out of range (e.g. 9999), deliver last page of results.
        pictures = paginator.page(paginator.num_pages)
    
    return my_render('results.html', request, {'pictures' : pictures})

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
    
    
    