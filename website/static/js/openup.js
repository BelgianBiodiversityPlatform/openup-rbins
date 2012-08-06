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
    var getTaxonomicFilterFromLists = function(taxonomy_levels){
        // We start by the most specific (=last) one
        var reversed = taxonomy_levels.slice(0).reverse()
        var found_model, found_id;
        
        $.each(reversed, function(i, level){
            //console.log
            var val = $('#' + level.html_id).val();
            
            if(val !== 'ALL') {
               found_model = level.server_model;
               found_id = val;
               return
           } 
        });
        
        console.log(found_model + ':' + found_id)
    };
    
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
        },
        initSearchFormSubmission: function(){
            var conf = OpenUp.config;
            
            conf.dom.search_button.click(function() {
                var url, sn, taxonomic_filter;
                var filters = {};
                
                // Add scientific name if necessary
                sn = conf.dom.sn_text_field.val();
                if(sn !== "") {
                    filters.sn_contains = sn;
                }
                
                taxonomic_filter = getTaxonomicFilterFromLists(conf.search_taxonomy_levels);
                if(taxonomic_filter) {
                    filters.taxonomic_filter = taxonomic_filter;
                }   

                url = conf.urls.search + "?" + $.param(filters);

                //window.location.href = url;    
                return false;
            });
            
        }
    };
    }();



