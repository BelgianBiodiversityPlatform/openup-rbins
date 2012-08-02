from django.conf.urls import patterns, include, url

urlpatterns = patterns('website.views',
    url(r'^$', 'index', name="website-index"), # Main (search) view
    
    url(r'^search$', 'search', name="website-search-view"), # Search results
    url(r'^contact$', 'contact', name="website-contact"),
    url(r'^about$', 'about', name="website-about"),
    
    # Ajax requests:
    url(r'^ajax-populate-list', 'ajax_populate_list', name="ajax-populate-list"),
)