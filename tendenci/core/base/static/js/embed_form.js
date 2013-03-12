var jq = jQuery.noConflict(true);
jq(document).ready(function() {
        jq( ".modal-form-wrap" ).dialog({
            autoOpen: false,
            height: 400,
            width: 500,
            modal: true,
            position: "center",
            title: "Confirm Form",
            resizable: false,
        });
        // check if captcha field exists in the form
        if (jq(".form-field div.id_captcha").parents("div.embed-form .form-builder-wrap form").length > 0){
            jq("div.embed-form .form-builder-wrap form .form-field div.id_captcha").hide();
            jq("div.embed-form .form-builder-wrap form").submit(function(){
                data = jq(this).parent().attr('data')
                jq(".modal-form-wrap").each(function(){
                    if ( jq(this).attr('data') == data ){
                        jq(this).dialog("open");
                    }
                });
                return false;
            });
        }
        // update dialog fields with fields from the form
        jq(".embed-form .form-field").each(function(){
            //jq(this).find("input[type='text']").bind("change propertychange keyup input paste", function(){
            jq(this).find("input[type='text']").change(function(){
                var id = jq(this).attr('id');
                var modalfield = jq(".modal-form-wrap .form-field input[id="+id+"]").val(jq(this).val());
            });
            //jq(this).find("textarea").bind("change propertychange keyup input paste", function(){
            jq(this).find("textarea").change(function(){
                var id = jq(this).attr('id');
                var modalfield = jq(".modal-form-wrap .form-field textarea[id="+id+"]").val(jq(this).val());
            });
            jq(this).find("select").change(function(){
                var id = jq(this).attr('id');
                var modalfield = jq(".modal-form-wrap .form-field select[id="+id+"]").val(jq(this).val());
            });
            jq(this).find("input[type='checkbox']").click(function(){
                var id = jq(this).attr('id');
                var checked = jq(this).is(':checked')
                var modalfield = jq(".modal-form-wrap .form-field input[id="+id+"]").prop('checked', checked);
            });
        });
});
