from urlparse import parse_qs

import pprint

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.utils import simplejson

from website.models import Family, Genus, Species, Picture

def my_render(template_path, request_obj, context={}):
    menu_entries = [
        {'label': 'Search', 'url_name': 'website-index', 'icon_name': 'icon-search'},
        {'label': 'Contact', 'url_name':'website-contact', 'icon_name': 'icon-comment'},
        {'label': 'About', 'url_name':'website-about', 'icon_name': 'icon-asterisk'},
        ]
    
    context.update({'menu_entries': menu_entries})
    
    return render_to_response(template_path, context, context_instance=RequestContext(request_obj))

def search(request):
    # Save query parameters
    family_id = request.GET.get('family_id')
    sn_contains = request.GET.get('sn_contains')
    
    taxonomic_filter_model = request.GET.get('taxonomic_filter_model')
    taxonomic_filter_id = request.GET.get('taxonomic_filter_id')
    taxonomic_filter_label = request.GET.get('taxonomic_filter_label')
    
    page = request.GET.get('page')
    
    # Filtering based on query parameters
    pictures_list = Picture.objects.all()
    
    filters = []
    
    if family_id:
        pictures_list = pictures_list.filter(family_id__exact = family_id)
        filters.append({'name': 'Family', 'value': Family.objects.get(pk=family_id).name})
        
    if sn_contains:
        pictures_list = pictures_list.filter(scientificname__icontains = sn_contains)
        filters.append({'name': 'Scientific name contains', 'value': sn_contains })
        
    if taxonomic_filter_model:
        selected_instance = globals()[taxonomic_filter_model].objects.get(pk=taxonomic_filter_id)
        
        filters.append({'name': taxonomic_filter_label, 'value': selected_instance.name})        
        
        pictures_list = pictures_list.filter(**{Picture.model_fk_mapping[taxonomic_filter_label]: selected_instance.pk}) 
        
        
    # Paginate
    paginator = Paginator(pictures_list, 6) # TODO: move to settings
    
    try:
        pictures = paginator.page(page)
    except PageNotAnInteger: 
        pictures = paginator.page(1) # If page is not an integer, deliver first page.
    except EmptyPage: # If page is out of range (e.g. 9999), deliver last page of results.
        pictures = paginator.page(paginator.num_pages)
    
    return my_render('results.html', request, {'pictures': pictures, 'filters': filters, 'force_menu_entry': 'Search'})

def index(request):
    families = Family.objects.all()
    
    metrics = {
        'pictures': Picture.objects.count(),
        'families': Family.objects.count(),
        'species': Species.objects.count()}
    
    return my_render('index.html', request, {
        'families': families,
        'metrics': metrics,
        })
        
def contact(request):
    return my_render('contact.html', request)
    
def about(request):
    return my_render('about.html', request)
    
# AJAX/JSON views
def ajax_populate_list(request):
    target_model_name = request.GET['target_model']
    
    entries = globals()[target_model_name].objects.all()
    json = simplejson.dumps([ {'pk': e.pk, 'name': e.name } for e in entries])
    
    return returns_json(json)
    
# Helpers	 
def returns_json(json):
    return HttpResponse(json, mimetype='application/javascript')    
        
    
    