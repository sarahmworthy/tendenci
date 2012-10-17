function updateIndex(e, prefix, idx){
    var id_regex = new RegExp('(form-\\d+)');
    var replacement = prefix + '-' + idx
    if ($(e).attr("for")) 
        {$(e).attr("for", $(e).attr("for").replace(id_regex, replacement));}
    if (e.id) {e.id = e.id.replace(id_regex, replacement);}
    if (e.name){ e.name = e.name.replace(id_regex, replacement);}
}

// update the serial number on the form. ex: Registrant #3, Reg #3
function updateFormHeader(this_form, prefix, idx){
    idx = idx + 1;

    // change the serial number on the form
    var id_regex = new RegExp('(form_\\d+)');
    var replacement = prefix + '_' + idx
    if (this_form.id) {this_form.id = this_form.id.replace(id_regex, replacement);}

    var reg_header = $(this_form).find('.applicant-header');
    if (reg_header) {
        $(reg_header).parent().children('div:last').show();
        $(reg_header).children('span.showhide').text('- ');
        var ic = $(reg_header).find('.item-counter');
        if (ic) {
            $(ic).html(idx);}
    };
    
};

function addApplicant(ele, prefix, price) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var row = $('.applicant-form:first').clone(true).get(0);
    
    $('.applicant-form:first').find('.applicant-header').removeClass('hidden');
    //$(row).insertAfter($('.registrant-form:last')).find('.hidden').removeClass('hidden');
    // remove the error
    $(row).find('div.error').remove();

    // update id attr
    var id_regex = new RegExp('(form_\\d+)');
    var replacement = prefix + '_' + formCount;
    if(row.id){
        row.id = row.id.replace(id_regex, replacement);
    }
    console.log(id_regex)
    //$(row).find(".form-field").children().children().each(function() {
    $(row).find(".form-field").find('[id^="id_form"]').each(function() {
        updateIndex(this, prefix, formCount);
        var $this = $(this);
        if ($this.attr('type') == 'text'){
         $this.val('');
        }
        
        // uncheck the checkbox
        if ($this.attr('type') == 'checkbox'){
         $this.attr('checked', false);
         
         {% if request.user.is_superuser %}
        if ($this.attr('name').search('override') != -1)
        {
        	var price_box = $this.closest('.admin-override').next();
        	toggle_admin_override($this, price_box);
        }
         {% endif %}
         
        }
      
    });
    
    $(row).find(".form-field").find('label[for^="id_form"]').each(function() {
        updateIndex(this, prefix, formCount);
    });
    
    $(row).insertAfter($('.applicant-form:last')).find('.hidden').removeClass('hidden');
    
    
    $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
    updateFormHeader(row, prefix, formCount);
    
    return false;
}

function add_applicants(e, prefix) {
    extra_count = 1;
    if (extra_count > 0) {
        for(var i=0; i<extra_count; i++){
            addApplicant(e, prefix);
        }
    }
    return false;
}
