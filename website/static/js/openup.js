// Helpers, language fixes and improvements
if (!String.prototype.supplant) {
    String.prototype.supplant = function (o) {
        return this.replace(/{([^{}]*)}/g,
        function (a, b) {
            var r = o[b];
            return typeof r === 'string' || typeof r === 'number' ? r : a;
        });
    };
}


// We use the "module pattern"
OpenUp = function(){
    // private variables and methods
    var generateFormEntryForTaxonomicLevel = function(level){
        var str = '<div class="control-group">\
            <label class="control-label" for="{html_id}">{label}</label>\
            <div class="controls">\
                <select id="{html_id}"></select>\
            </div>\
        </div>'.supplant({label: level.label, html_id: level.html_id});
        
        // Initially populate them (all values)
        $.getJSON(OpenUp.config.urls.populate_taxonomic_lists, {target_model: level.server_model}, function(data){
            var $select = $('#{html_id}'.supplant({html_id: level.html_id}));
            $select.append('<option value="ALL">--- ALL ---</option>');
            
            $.each(data, function(i, entry){
                $select.append('<option value="{id}">{name}</option>'.supplant({id: entry.pk, name: entry.name}));
            });
        });
        
        return str;
    };

    return {
        config: {}, // Will be populated by HTML page
        addTaxonomySelectsToSearchForm: function(){
            var conf = OpenUp.config; // Shortcut 

            $.each(conf.search_taxonomy_levels, function(i, level){
                conf.dom.taxonomic_select_container.append(generateFormEntryForTaxonomicLevel(level));
            });
        }
    };
    }();



