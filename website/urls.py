from django.conf.urls import patterns, include, url

urlpatterns = patterns('website.views',
    url(r'^$', 'index', name="website-index"), # Main (search) view
    
    url(r'^search$', 'search', name="website-search-view"), # Search results
    url(r'^contact$', 'contact', name="website-contact"),
    url(r'^about$', 'about', name="website-about"),
    
    url(r'^plates$', 'plates', name="website-browse-plates"),
    url(r'^plates/(?P<pk>\d+)$', 'show_plate', name="website-show-plate"),
    
    # Ajax requests:
    url(r'^ajax-populate-list', 'ajax_populate_list', name="ajax-populate-list"),
    url(r'^ajax-search-results', 'ajax_search_results', name="ou-ajax-search-results")
)