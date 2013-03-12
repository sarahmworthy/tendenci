$(document).ready(function() {
        $( ".modal-form-wrap" ).dialog({
            autoOpen: false,
            height: 400,
            width: 500,
            modal: true,
            position: "center",
            title: "Confirm Form",
            resizable: false,
        });
        // check if captcha field exists in the form
        if ($(".form-field div.id_captcha").parents("div.embed-form .form-builder-wrap form").length > 0){
            $("div.embed-form .form-builder-wrap form .form-field div.id_captcha").hide();
            $("div.embed-form .form-builder-wrap form").submit(function(){
                data = $(this).parent().attr('data')
                $(".modal-form-wrap").each(function(){
                    if ( $(this).attr('data') == data ){
                        $(this).dialog("open");
                    }
                });
                return false;
            });
        }
        // update dialog fields with fields from the form
        $(".embed-form .form-field").each(function(){
            //$(this).find("input[type='text']").bind("change propertychange keyup input paste", function(){
            $(this).find("input[type='text']").change(function(){
                var id = $(this).attr('id');
                var modalfield = $(".modal-form-wrap .form-field input[id="+id+"]").val($(this).val());
            });
            //$(this).find("textarea").bind("change propertychange keyup input paste", function(){
            $(this).find("textarea").change(function(){
                var id = $(this).attr('id');
                var modalfield = $(".modal-form-wrap .form-field textarea[id="+id+"]").val($(this).val());
            });
            $(this).find("select").change(function(){
                var id = $(this).attr('id');
                var modalfield = $(".modal-form-wrap .form-field select[id="+id+"]").val($(this).val());
            });
            $(this).find("input[type='checkbox']").click(function(){
                var id = $(this).attr('id');
                var checked = $(this).is(':checked')
                var modalfield = $(".modal-form-wrap .form-field input[id="+id+"]").prop('checked', checked);
            });
        });
});
