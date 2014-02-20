import json
import urllib

from gdata.client import BadAuthentication

import logging
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from django.conf import settings
from django.core.cache import cache

# Genus/Subfamily used implicitally to populate Ajax lists!
from website.models import Family, Subfamily, Genus, Species, Picture, Planche, first_rank_higher
from website.utils import ga_metrics

logger = logging.getLogger(__name__)


def my_render(template_path, request_obj, context={}):
    menu_entries = [
        {'label': 'Search', 'url_name': 'website-index', 'icon_name': 'icon-search'},
        {'label': 'Browse all pictures', 'url_name': 'website-search-view', 'icon_name': 'icon-eye-open'},
        {'label': 'Browse all plates', 'url_name': 'website-browse-plates', 'icon_name': 'icon-book'},
        {'label': 'Contact', 'url_name': 'website-contact', 'icon_name': 'icon-comment'},
        {'label': 'About', 'url_name': 'website-about', 'icon_name': 'icon-asterisk'},
    ]
    
    context.update({'menu_entries': menu_entries,
                    'GA_ACCOUNT': settings.GOOGLE_ANALYTICS_APP_NAME,
                    'BLOG_URL': settings.NOELMAL_BLOG_URL})
    
    return render_to_response(template_path, context, context_instance=RequestContext(request_obj))


def search(request):
    return my_render('results.html', request, {'force_menu_entry': 'Search'})


def ajax_search_results(request):
    params = extract_request_params(request)

    # 1. Filtering
    pictures_list = Picture.objects.all()
    filters = []

    if params['family_id']:
        pictures_list = pictures_list.filter(family_id__exact=params['family_id'])
        filters.append({'name': 'Family', 'value': Family.objects.get(pk=params['family_id']).name})

    if params['sn_contains']:
        pictures_list = pictures_list.filter(scientificname__icontains=params['sn_contains'])
        filters.append({'name': 'Scientific name contains', 'value': params['sn_contains']})

    if params['taxonomic_filter_model']:
        selected_instance = globals()[params['taxonomic_filter_model']].objects.get(pk=params['taxonomic_filter_id'])
        pictures_list = pictures_list.filter(**{Picture.model_fk_mapping[params['taxonomic_filter_label']]: selected_instance.pk})
        filters.append({'name': params['taxonomic_filter_label'], 'value': selected_instance.name})

    # 2. In specific vases, provide "search refinement" links
    refine_links = []
    # 2a) if searching by Family: provide subfamily refinement
    #import pdb; pdb.set_trace()
    if params['family_id']:
        subfamilies = Subfamily.objects.filter(family_id__exact=params['family_id'])
        if len(subfamilies) > 0:
            proposals = []
            for subfamily in subfamilies:
                new_params = {'taxonomic_filter_model': 'Subfamily', 'taxonomic_filter_id': subfamily.pk, 'taxonomic_filter_label': 'Subfamily'}
                url_str = reverse('website-search-view') + "?" + urllib.urlencode(new_params)
                proposals.append({'text': subfamily.name, 'url': url_str})

            refine = {'label': 'Refine by subfamily: ', 'proposals': proposals}
            refine_links.append(refine)

    # 3. Pagination

    # Number of images returned in each batch.
    # They will be shown on screen in rows of 6 images
    # The number of rows should be bigger than height of screen on initial load, or the scroll
    # events will never fire, and the rest will not be loaded
    paginator = Paginator(pictures_list, 4 * 6)
    
    pictures = paginator.page(params['page'])
    
    pictures_data = [{
        'fileuri': picture.fileuri,
        'picture_id': picture.picture_id,

        'scientificname': picture.scientificname,
        'fileuri_picture_only': picture.fileuri_picture_only,
        'family_name': picture.family_name_formatted,
        'subfamily_name': picture.subfamily_name_formatted,
        'genus_name': picture.genus_name_formatted,
        'species_name': picture.species_name_formatted,
        'subspecies_name': picture.subspecies_name_formatted,

        'eventdate_verbatim': picture.eventdate_verbatim or '/',
        'country_name': picture.country_name_formatted,
        'province_name': picture.province_name_formatted,
        'station_name': picture.station_name_formatted,

        'origpathname': picture.origpathname,
        'view_name': picture.view_name_formatted,

        'plates': picture.related_planches  # List of plates ref. the same specimen
            
    } for picture in pictures]

    # 4. Serialize and return all that
    meta_to_serialize = {'has_next': pictures.has_next(),
                         'total_count': paginator.count,
                         'current_filters': filters,
                         'refine_links': refine_links}
    
    pics_to_serialize = pictures_data

    all_to_serialize = {'pictures': pics_to_serialize, 'meta': meta_to_serialize}
    return returns_json(json.dumps(all_to_serialize))


def index(request):
    families = Family.objects.all()

    try:
        ga_data = get_cached_analytics()
    except BadAuthentication:
        logger.error('Google Analytics API authentication error. Please check the credentials.')
        ga_data = {'visitors': None, 'visits': None}  # ...avoiding IndexError later

    metrics = {
        'pictures': Picture.objects.count(),
        'families': Family.objects.count(),
        'species': Species.objects.count(),

        'plates': Planche.objects.count(),

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


def plates(request):
    plates = Planche.objects.all()

    return my_render('all_plates.html', request, {'plates': plates})


def show_plate(request, pk):
    plate = get_object_or_404(Planche, pk=pk)
    return my_render('plate.html', request, {'plate': plate})


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


def extract_request_params(request):
    return {
        'family_id': request.GET.get('family_id'),
        'sn_contains': request.GET.get('sn_contains'),

        'taxonomic_filter_model': request.GET.get('taxonomic_filter_model'),
        'taxonomic_filter_id': request.GET.get('taxonomic_filter_id'),
        'taxonomic_filter_label': request.GET.get('taxonomic_filter_label'),

        'page': request.GET.get('page')
    }

        
    
    