odoo.define('sisvac.partner_form', function (require) {
    'use strict';

    require('web.dom_ready');

    let patient_api = "/sisvac/patient_api/"
    let $name = $("#welcome_name");
    let $patient_form = $(".patient_form");
    let $submit_button = $(".sisvac_patient_submit");
    let $form_body = $(".form_body");
    let $partner_vat = $("#partner_vat");
    let $hidden_vat = $("#vat");
    if (!$partner_vat.length) {
        return;
    }

    $partner_vat.on('keyup', function (ev) {
        let partner_vat = $partner_vat.val();
        if (partner_vat.length !== 11) {
            return;
        }
        console.count("Partner Vat");
        
        $.ajax({
            url: patient_api + partner_vat,
            dataType: 'json',
            success: function (data) {
                $partner_vat.prop("disabled", true);
                $hidden_vat.html($partner_vat.html());
                $form_body.removeClass("d-none");
                $name.html(data.patient_name);
            },
        });
    });

});