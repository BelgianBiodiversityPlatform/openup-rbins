from django import template

register = template.Library()

# TODO: Extract in a specific app
# TODO: Write tests
# TODO: Pass results instead of generating display (like "for")
# TODO: Implement different algorithms
# TODO: PEP-8

@register.tag(name="simple_tag_cloud")
def do_simple_tag_cloud(parser, token):
    bits = token.split_contents()
    
    if len(bits) != 4:
        raise template.TemplateSyntaxError("%r tag requires 3 arguments: data, min_size and max_size" % token.contents.split()[0])
            
    tag_name, data, min_size, max_size = bits 
    
    return TagCloudNode(data, min_size, max_size)
    
class TagCloudNode(template.Node):
    def __init__(self, data, min_size, max_size):
        self.data = template.Variable(data)
        self.min_size = int(min_size)
        self.max_size = int(max_size)
    
    
    def render(self, context):
        data = self.data.resolve(context)
        
        smallest_count, largest_count = find_min_max(data)
           
        r = ''
        for tag in data:
            current_count = tag['count']
            size = calculate_size(current_count, smallest_count, largest_count, self.max_size, self.min_size)
            r += '<a href="%s" style="font-size: %dpx;">%s</a> ' % (tag['url'], size, tag['label'])
            
        return r    

# Utility functions
def calculate_size(current_count, smallest_count, largest_count, max_size, min_size):
    return ( ((current_count-smallest_count) * (max_size-min_size)) / (largest_count-smallest_count) ) + min_size


def find_min_max(data):
    # Expects each element of data has a 'count' attributes
    smallest_count = data[0]['count']
    largest_count = data[0]['count']
    
    for tag in data:
        current_count = tag['count']
        if current_count < smallest_count:
            smallest_count = current_count
        if current_count > largest_count:
            largest_count = current_count
            
    return (smallest_count, largest_count)                       
        
                