function deleteApplicant(ele, prefix) {
    var applicant_form = $(ele).parents('.applicant-form');
    var attr_id = $(applicant_form).attr("id");
    // remove the applicant form
    $(applicant_form).remove();
    
    // update the TOTAL_FORMS
    var forms = $(".applicant-form");
    var prefixes = ['user', 'profile', 'demographics', 'membership']
    for (var i=0, l=prefixes.length; i < l; i++) {
        $("#id_" + prefixes[i] + "-TOTAL_FORMS").val(forms.length);
    }
    
    // update form index
    var this_form;
    for (var i=0, formCount=forms.length; i<formCount; i++){
        this_form = forms.get(i);
        $(this_form).find(".form-field").find('[id^="id_user"]').each(function() {
            if (this){
                updateIndex(this, 'user', i);
            }
        });
        $(this_form).find(".form-field").find('[id^="id_profile"]').each(function() {
            if (this){
                updateIndex(this, 'profile', i);
            }
        });
        $(this_form).find(".form-field").find('[id^="id_demographics"]').each(function() {
            if (this){
                updateIndex(this, 'demographics', i);
            }
        });
        $(this_form).find(".form-field").find('[id^="id_membership"]').each(function() {
            if (this){
                updateIndex(this, 'membership', i);
            }
        });

        // update form header
        if (i > 0){
            updateFormHeader(this_form, i);
        }
    }
    
    return false;
}

function updateIndex(e, prefix, idx){
    var id_regex = new RegExp('('+prefix+'-\\d+)');
    var replacement = prefix + '-' + idx
    if ($(e).attr("for")) 
        {$(e).attr("for", $(e).attr("for").replace(id_regex, replacement));}
    if (e.id) {e.id = e.id.replace(id_regex, replacement);}
    if (e.name){ e.name = e.name.replace(id_regex, replacement);}
}

function updateFormHeader(this_form, idx){
    idx = idx + 1;

    // change the serial number on the form
    var id_regex = new RegExp('(form_\\d+)');
    var replacement = 'form_' + idx
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

function addApplicant(ele) {
    var formCount = parseInt($('#id_user-TOTAL_FORMS').val());
    var row = $('.applicant-form:first').clone(true).get(0);
    
    $('.applicant-form:first').find('.applicant-header').removeClass('hidden');
    //$(row).insertAfter($('.registrant-form:last')).find('.hidden').removeClass('hidden');
    // remove the error
    $(row).find('div.error').remove();

    // update id attr
    var id_regex = new RegExp('(form_\\d+)');
    var replacement = 'form_' + formCount;
    if(row.id){
        row.id = row.id.replace(id_regex, replacement);
    }

    var prefixes = ['user', 'profile', 'demographics', 'membership']
    for (var i=0, l=prefixes.length; i < l; i++) {
        $(row).find(".form-field").find('[id^="id_'+prefixes[i]+'"]').each(function() {
            updateIndex(this, prefixes[i], formCount);
            var $this = $(this);
            if ($this.attr('type') == 'text'){
                $this.val('');
            }          
        });
        $(row).find(".form-field").find('label[for^="id_'+prefixes[i]+'"]').each(function() {
            updateIndex(this, prefixes[i], formCount);
        });
        $('#id_' + prefixes[i] + '-TOTAL_FORMS').val(formCount + 1);
    }
    
    $(row).insertAfter($('.applicant-form:last')).find('.hidden').removeClass('hidden');
    updateFormHeader(row, formCount);
    
    return false;
}

$(document).ready(function(){
    // delete confirmation
    $('button.delete-button').live('click', function(e){
         var delete_confirm = confirm('Are you sure you want to delete this applicant?');   // confirm
         if(delete_confirm) {
            deleteApplicant(this);
         }
        return false;   // cancel
    });

    $('button.add-another-btn').live('click', function(e){
        e.preventDefault();
        addApplicant(this);
        return false;
    });
});
