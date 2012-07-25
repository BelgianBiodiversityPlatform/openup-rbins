from math import log10
from django import template

register = template.Library()

# TODO: Extract in a specific app
# TODO: Write tests
# TODO: Implement different algorithms
# TODO: PEP-8
# TODO: update doc (incorrect now)
# TODO Improve tag so it works with both QuerySets (ok now) and list of dict (not ok now)

@register.tag(name="simple_tag_cloud")
def do_simple_tag_cloud(parser, token):
    bits = token.split_contents()
    
    if len(bits) != 6:
        raise template.TemplateSyntaxError("%r tag requires 5 arguments: data, count_property, min_size, max_size and mode." % token.contents.split()[0])
            
    tag_name, data, count_property, min_size, max_size, mode = bits 
    
    return TagCloudNode(data, count_property, min_size, max_size, mode)
    
class TagCloudNode(template.Node):
    """
    Simple helper to allow generation of tag clouds.
    
    Usage:
    
    {% simple_tag_cloud queryset count_attribute min_size max_size mode %}
    
    For each element (model instance) in queryset, this tag will add a 'tag_size' attribute.
    The value of tag_size will be in the min_size...max_size range and will reflect the value of the 'count_attribute' attribute of the instance.
    
    Mode should be set to "lin" or "log".
    
    Example:
    
    {% simple_tag_cloud families count_pictures 15 80 log %}
    
    => each element in families (a QuerySet) will gain a tag_size attribute. This tag size will be proportional to a_family.count_pictures and will be >= 15 and <= 80.
    
    The typical usage will then be:
    
    {% for family in families %}
        <a style="font-size: {{ family.tag_size }}px;" href="{% url family.get_full_path %}">{{ family.name }}</a> 
    {% endfor %}
    
    NOTE: This currently only works with querysets.
    NOTE: the count_attribute parameter should be the name of a property (NOT a method!) of the instance. This can be, for example, created with the @property decorator.
    Example (in models.py:)
    
    @property
    def count_pictures(self):
        return len(self.picture_set.all())
    
    """
    
    def __init__(self, data, count_property, min_size, max_size, mode):
        self.data = template.Variable(data)
        self.count_property = count_property
        self.min_size = int(min_size)
        self.max_size = int(max_size)
        
        if mode == 'log':
            self.calculate = calculate_log
        elif mode == "lin":
            self.calculate = calculate_lin    
    
    
    def render(self, context):
        data = self.data.resolve(context)
        
        smallest_count, largest_count = find_min_max(data, self.count_property)
           
        results = []
        for tag in data:
            current_count = getattr(tag, self.count_property)
            size = self.calculate(current_count, smallest_count, largest_count, self.max_size, self.min_size)
            tag.tag_size = size
            
        return ''    
        

# Utility functions
def calculate_lin(current_count, smallest_count, largest_count, max_size, min_size):
    return ( ((current_count-smallest_count) * (max_size-min_size)) / (largest_count-smallest_count) ) + min_size

def calculate_log(current_count, smallest_count, largest_count, max_size, min_size):
    return (log10(current_count) / log10(largest_count)) * (max_size - min_size) + min_size

def find_min_max(data, count_property):
    # Expects each element of data has a 'count' attributes
    smallest_count = getattr(data[0], count_property)
    largest_count = getattr(data[0], count_property)
    
    for tag in data:
        current_count = getattr(tag, count_property)
        if current_count < smallest_count:
            smallest_count = current_count
        if current_count > largest_count:
            largest_count = current_count
            
    return (smallest_count, largest_count)                       
        
                