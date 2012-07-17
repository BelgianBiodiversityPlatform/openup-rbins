from django.shortcuts import render_to_response
from django.template import RequestContext

def my_render(template_path, request_obj, context={}):
    return render_to_response(template_path, context, context_instance=RequestContext(request_obj))

def index(request):
    return my_render('index.html', request)
    
    
    