from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from website.models import Family, Picture, Species

def my_render(template_path, request_obj, context={}):
    menu_entries = [
        {'label': 'Search', 'url_name': 'website-index'},
        {'label': 'Contact', 'url_name':'website-contact'},
        {'label': 'About', 'url_name':'website-about'},
        ]
    
    context.update({'menu_entries': menu_entries})
    
    return render_to_response(template_path, context, context_instance=RequestContext(request_obj))

def search(request):
    # Save query parameters
    family_id = request.GET.get('family_id')
    
    page = request.GET.get('page')
    
    # Filtering based on query parameters
    pictures_list = Picture.objects.all()
    
    filters = []
    if family_id:
        pictures_list = pictures_list.filter(family_id__exact = family_id)
        
        filters.append({'name': 'Family', 'value': Family.objects.get(pk=family_id).name})
        
    # Paginate
    paginator = Paginator(pictures_list, 6) # TODO: move to settings
    
    try:
        pictures = paginator.page(page)
    except PageNotAnInteger: 
        pictures = paginator.page(1) # If page is not an integer, deliver first page.
    except EmptyPage: # If page is out of range (e.g. 9999), deliver last page of results.
        pictures = paginator.page(paginator.num_pages)
    
    return my_render('results.html', request, {'pictures': pictures, 'filters': filters})

def index(request):
    families = Family.objects.all()
    
    metrics = {
        'pictures': Picture.objects.count(),
        'families': Family.objects.count(),
        'species': Species.objects.count()}
    
    families_for_tag_cloud = [ {'label': f.name, 'count': f.count_pictures(), 'url': 'http://www.google.com'} for f in families]
    
    return my_render('index.html', request, {
        'families': families,
        'metrics': metrics,
        'families_for_tag_cloud': families_for_tag_cloud
        })
        
def contact(request):
    return my_render('contact.html', request)
    
def about(request):
    return my_render('about.html', request)            
    
    
    