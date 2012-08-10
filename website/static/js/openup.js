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
        var reversed = taxonomy_levels.slice(0).reverse();
        var found_model, found_id;
        
        $.each(reversed, function(i, level){
            //console.log('P: ' + level.html_id);
            var val = $('#' + level.html_id).val();
            
            if(val !== 'ALL') {
               found_model = level.server_model;
               found_id = val;
               found_label = level.label;
               return false; // Breaks $.each
           } 
        });
        
        if (found_model) {
            return {
                'model': found_model,
                'id': found_id,
                'label': found_label
            };
        } else { // Nothing is selected
            return false;
        }
    };
    
    var taxonomySelectChanged = function(event){
        var changed_elem_id = event.target.id;
        var selected_id = '{sel} option:selected'.supplant({sel: changed_elem_id});
        var changed_elem_value = $('#' + selected_id).val();
        var conf = OpenUp.config; // Shortcut 
        var found_current = false;
        var nextone;
        
        // Get the level object for thge changed element
        var changed_level;
        $.each(conf.search_taxonomy_levels, function(i, level){
            if (level.html_id === changed_elem_id) {
                changed_level = level;
            }
        });
        
        
        if(changed_elem_value === 'ALL') {
            // We have to update only the "child" levels
            $.each(conf.search_taxonomy_levels, function(i, level){
                if(level === changed_level) {
                    found_current = true;
                    
                }
                
                if(found_current && level !== changed_level) { // Lower levels
                    populate_list(level, {changed_model_name: changed_level.server_model, changed_id: changed_elem_value});
                    
                    // Hide all the levels lower than current (if required by config)
                    if(level.hide_until_parent_set) {
                        $('#' + getContainerId(level)).hide();
                    }
                }
                
            });
            
        } else {
            // We have to update all the other levels
            $.each(conf.search_taxonomy_levels, function(i, level){
                // We don't touch the elment that changed
                if(level !== changed_level) {
                    populate_list(level, {changed_model_name: changed_level.server_model, changed_id: changed_elem_value});
                } else {
                    // We're on the element that changed... show the child, if necessary
                    nextone = conf.search_taxonomy_levels[i+1];               
                    if (nextone.hide_until_parent_set) {
                        // Maybe it's already displayed ? unnecessary op. in that case...
                        $('#' + getContainerId(nextone)).show();
                    }
                    
                }
            });
        }

    };
    
    var populate_list = function(level_to_populate, additional_params) {
        var params = {target_model: level_to_populate.server_model};
        if (additional_params !== null) {
            $.extend(params, additional_params);
        }
        
        $('#spinner_' + level_to_populate.html_id).show();
        
        $.getJSON(OpenUp.config.urls.populate_taxonomic_lists, params, function(data){
            var select_id = level_to_populate.html_id;
            var $select = $('#' + select_id);
            $select.empty();
            
            $select.append('<option value="ALL">--- ALL ---</option>');
            
            $.each(data.entries, function(i, entry){
                $select.append('<option value="{id}">{name}</option>'.supplant({id: entry.pk, name: entry.name}));
            });
            
            // Select entry
            $('#{select_id} option[value="{val}"]'.supplant({select_id: select_id, val: data.selected_value})).prop('selected', true);
            
            $('#spinner_' + level_to_populate.html_id).hide();
        });
    };
    
    var getContainerId = function(level) {
      return 'container_' + level.html_id;
    };
    
    var generateFormEntryForTaxonomicLevel = function(level){
        var add_style;
        
        if (level.hide_until_parent_set){
            add_style="display: none;";
        }
        
        var str = '<div id="{level_container_id}" style="{add_style}" class="control-group">\
            <label class="control-label" for="{html_id}">{label}</label>\
            <div class="controls">\
                <select id="{html_id}"></select>\
                <img id="spinner_{html_id}" src="{spinner_path}" />\
            </div>\
        </div>'.supplant({
            add_style: add_style, 
            label: level.label, 
            html_id: level.html_id, 
            spinner_path: OpenUp.config.spinner_path,
            level_container_id: getContainerId(level)
            });
        
        // Initially populate them (all values)
       populate_list(level);
        
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
        
        // When a (taxonomic) select changes, the others follow
        initSearchFormAjax: function(){
            // Install handlers for all elements defined in the config
            $.each(OpenUp.config.search_taxonomy_levels, function(i, level){
                $('#' + level.html_id).change(taxonomySelectChanged);
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
                    filters.taxonomic_filter_model = taxonomic_filter.model;
                    filters.taxonomic_filter_id = taxonomic_filter.id;
                    filters.taxonomic_filter_label = taxonomic_filter.label;
                }   

                url = conf.urls.search + "?" + $.param(filters);

                window.location.href = url;    
                return false;
            });
            
        }
    };
    }();



