import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from django.conf import settings
from django.core.cache import cache

# Genus used implicitally to populate Ajax lists!
from website.models import Family, Genus, Species, Picture, first_rank_higher
from website.utils import ga_metrics


def my_render(template_path, request_obj, context={}):
    menu_entries = [
        {'label': 'Search', 'url_name': 'website-index', 'icon_name': 'icon-search'},
        {'label': 'Contact', 'url_name': 'website-contact', 'icon_name': 'icon-comment'},
        {'label': 'About', 'url_name': 'website-about', 'icon_name': 'icon-asterisk'},
    ]
    
    context.update({'menu_entries': menu_entries,
                    'GA_ACCOUNT': settings.GOOGLE_ANALYTICS_APP_NAME})
    
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
        pictures_list = pictures_list.filter(family_id__exact=family_id)
        filters.append({'name': 'Family', 'value': Family.objects.get(pk=family_id).name})
        
    if sn_contains:
        pictures_list = pictures_list.filter(scientificname__icontains=sn_contains)
        filters.append({'name': 'Scientific name contains', 'value': sn_contains})
        
    if taxonomic_filter_model:
        selected_instance = globals()[taxonomic_filter_model].objects.get(pk=taxonomic_filter_id)
        
        filters.append({'name': taxonomic_filter_label, 'value': selected_instance.name})
        
        pictures_list = pictures_list.filter(**{Picture.model_fk_mapping[taxonomic_filter_label]: selected_instance.pk})
        
    # Paginate
    paginator = Paginator(pictures_list, 6)
    
    try:
        pictures = paginator.page(page)
    except PageNotAnInteger:
        pictures = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:  # If page is out of range (e.g. 9999), deliver last page of results.
        pictures = paginator.page(paginator.num_pages)
    
    return my_render('results.html', request, {'pictures': pictures,
                                               'filters': filters,
                                               'force_menu_entry': 'Search'})


def index(request):
    families = Family.objects.all()

    ga_data = get_cached_analytics()

    metrics = {
        'pictures': Picture.objects.count(),
        'families': Family.objects.count(),
        'species': Species.objects.count(),

        'visitors': ga_data['visitors'],
        'visits': ga_data['visits']
    }

    return my_render('index.html', request, {
        'families': families,
        'metrics': metrics}
    )
        

def contact(request):
    return my_render('contact.html', request)
    

def about(request):
    return my_render('about.html', request)
    

# AJAX/JSON views

# Can be called:
# 1) In reaction to a list  change (details in changed_rank and changed_id)
# 2) At page load for initial populate (need all values)
def ajax_populate_list(request):
    target_model_name = request.GET['target_model']
    
    changed_model_name = request.GET.get('changed_model_name', False)
    changed_id = request.GET.get('changed_id', False)
    
    all_entries = globals()[target_model_name].objects.all().order_by('name')
    
    # Page init, we want to lad all values
    if not changed_model_name:
        entries = all_entries
        selected_value = 'ALL'
    # We loadvalues in reaction to a change in another list, so we have to filter
    else:
        # Is the changed level higher than the level to populate ?
        if first_rank_higher(changed_model_name, target_model_name):
            # We returns only children of the changed level, 'ALL' is selected
            if changed_id == 'ALL':
                entries = all_entries
            else:
                entries = all_entries.filter(**{Picture.model_fk_mapping[changed_model_name]: changed_id})
            
            selected_value = 'ALL'
        else:
            # We return every entries, but select the parent of the changed level
            entries = all_entries
            selected_value = getattr(globals()[changed_model_name].objects.get(pk=changed_id), Picture.model_fk_mapping[target_model_name])
    
    prepared_entries = [{'pk': e.pk, 'name': e.name} for e in entries]
    json_data = json.dumps({'entries': prepared_entries, 'selected_value': selected_value})
    
    return returns_json(json_data)

    
# Helpers
def returns_json(json):
    return HttpResponse(json, content_type='application/javascript')


def get_cached_analytics():
    # Google analytics API query is slow, so we cache results
    GA_TIMEOUT = 15 * 60  # 15 minutes
    cached_data = cache.get("googla_analytics_results")
    if cached_data is None:
        ga_data = ga_metrics(settings.GOOGLE_ANALYTICS_APP_NAME,
                             settings.GOOGLE_ANALYTICS_USER_EMAIL,
                             settings.GOOGLE_ANALYTICS_USER_PASS,
                             settings.GOOGLE_ANALYTICS_TABLE_ID)

        cache.set("googla_analytics_results", ga_data, GA_TIMEOUT)
        metrics = ga_data
    else:
        metrics = cached_data

    return metrics

        
    
    