odoo.define('sisvac.partner_form', function (require) {
    'use strict';

    require('web.dom_ready');
    
    let $partner_vat = $("#partner_vat");
    if (!$partner_vat.length) {
        return;
    }
    let patient_api = "/sisvac/patient_api/"
    let $name = $("#welcome_name");
    let $form_body = $(".form_body");
    let $vat_error_message = $(".vat_error_message");
    let $already_registered_message = $(".already_registered_message");
    
    let $patient_form = $(".patient_form");
    let $phone_field = $("#phone");
    let $mobile_field = $("#mobile");
    let $submit_button = $(".sisvac_patient_submit");
    let $hidden_vat = $("#vat");

    $partner_vat.on('keyup', function (ev) {
        let partner_vat = $partner_vat.val();
        if (partner_vat.replace(/\D/g,'').length !== 11) {
            return;
        }
        console.count("Partner Vat");
        
        $.ajax({
            url: patient_api + partner_vat,
            dataType: 'json',
            success: function (data) {
                
                $partner_vat.prop("disabled", true);
                $hidden_vat.val($partner_vat.val());
                $name.html(data.patient_name);
                
                hide_error_messages();
                activate_form();
            },
            error: function (xhr, ajaxOptions, thrownError) {
                $vat_error_message.removeClass("d-none");
                console.error("An error has been occurred. " + thrownError);
            }
        });
    });

    $('.patient_form').on("keydown", function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            return false;
        }
    });

    function hide_error_messages() {
        $already_registered_message.addClass("d-none");
        $vat_error_message.addClass("d-none");
    }

    function activate_form() {
        $form_body.removeClass("d-none");
    }
    

});