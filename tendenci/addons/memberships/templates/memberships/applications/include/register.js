$(document).ready(function(){
    $('#discount_check').click(function(){
        code = $('#id_discount_code').val();
        
        $.post(
            '{% url discount.discounted_prices %}',
            {
                'code':code,
                'app':'memberships'
            },
            function(data, textStatus, jqXHR){
                json = $.parseJSON(data);
                $('#discount-message').html(json["message"]);
            }
        );
    });
});

