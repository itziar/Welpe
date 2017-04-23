if ($('.confirm-2').length) {
    document.querySelector('.confirm-2').onclick = function () {
        swal({
            title: "Saved correctly",
            text: "The proposal was saved successfully",
            type: "success",
            confirmButtonClass: 'btn-success',
            confirmButtonText: 'Success!'
        });
    };
}


function change_display(idUnico, elemToShow) {
//show an elem if you need to fill it
    if (elemToShow == "inscripcion") {
        a = $("#allow_assist_datepickers_" + idUnico);
        element = "checkbox_allow_assist_" + idUnico
    }
    else if (elemToShow == "limit") {
        a = $("#limit_span_" + idUnico);
        element="checkbox_limit_"+idUnico
    }
    else if (elemToShow == "rac") {
        a = $("#creditos_span_" + idUnico);
        element="checkbox_rac_"+idUnico
    }
    console.log( a);
    if (document.getElementById(element).checked) {
        a.show();
        if (elemToShow == "inscripcion" ){
            $("#fecha_" + elemToShow + "_inicial_" + idUnico).prop('required', true);
            $("#fecha_" + elemToShow + "_final_" + idUnico).prop('required', true);
        }
    } else {
        a.hide();
        if (elemToShow == "inscripcion" || elemToShow == "proposicion") {
            $("#fecha_" + elemToShow + "_inicial_" + idUnico).prop('required', false);
            $("#fecha_" + elemToShow + "_final_" + idUnico).prop('required', false);
        }
    }
};


$(document).ready(function () {
    //$('#showSpeeches').click(function(){setTimeout(function(){$(window).resize();},500)});
    // checkbox square-blue
    $('.special-checkbox').iCheck({
        checkboxClass: 'icheckbox_square-blue',
        increaseArea: '20%' // optional
    });
    //para el checkbox del registro de participantes no se pueda seleccionar
    $(".no-edit").attr("disabled", true);

});

function manage_preregistration(id) {
    $.ajax({
        url: 'preregistrate',
        type: 'post',
        sync: true,
        data: $('#preregistrate_form_' + id).serialize(),
        dataType: 'json',
        success: function (data) {
            if (id.indexOf("speech") == 0) {
                change_text_to_show(id, data);
                change_text_to_show(id.substring(7), data);
            } else {
                change_text_to_show(id, data);
                change_text_to_show('speech_' + id, data);
            }
        },
        error: function (data) {
            alert("An unexpected error has happened");
        }
    });
};

function change_text_to_show(id, data) {

    if (data["status"] === "unregistred") {
        $("#speech_asistents_" + id).html(data["number_of_assistants"]);
        // TODO: use i18n engine
        $("#submit_preregistrate_" + id).text("Choose");
        $("#submit_preregistrate_" + id).removeClass("btn-success");
        $("#submit_preregistrate_" + id).addClass("btn-default");
        $("#card_" + id).toggleClass("panel-success");
    } else {
        $("#speech_asistents_" + id).html(data["number_of_assistants"]);
        // TODO: use i18n engine
        $("#submit_preregistrate_" + id).text("I will go!");
        $("#submit_preregistrate_" + id).removeClass("btn-default");
        $("#submit_preregistrate_" + id).addClass("btn-success");
        $("#card_" + id).toggleClass("panel-success");
    }
}

function registration(phone, passport) {
    if ((($('#' + phone).val()).length > 15) || (($('#' + passport).val()).length > 15)) {
        swal(
            {
                title: 'Oops...',
                text: 'The ID/Passport and the phone cannot have more than 15 digits or letters.',
                type: 'warning',
                showCancelButton: true, confirmButtonClass: 'btn-warning', confirmButtonText: 'OK'
            }
        );
        return false;
    }
    else {
        swal(
            {
                title: 'Saved correctly',
                text: 'The registration was done successfully',
                type: 'success',
                confirmButtonClass: 'btn-success',
                confirmButtonText: 'Success!'
            }
        );
        return true;
    }
}


function edition(check) {
    if ((($(check).val()).length > 15) || (($(check).val()).length > 15)) {
        swal({
            title: 'Oops...', text: 'The ID/Passport and the phone cannot have more than 15 digits or letters.',
            type: 'warning',
            showCancelButton: true,
            confirmButtonClass: 'btn-warning',
            confirmButtonText: 'OK'
        });
        return false;
    }
    else {
        swal({
            title: 'Saved correctly',
            text: 'The registration was done successfully',
            type: 'success',
            confirmButtonClass: 'btn-success',
            confirmButtonText: 'Success!'
        });
        return true;
    }
}


function cancela() {
    swal({
            title: 'Are you sure?',
            text: 'Your registration will be cancelled!',
            type: 'warning',
            showCancelButton: true,
            confirmButtonClass: 'btn-danger',
            confirmButtonText: 'Yes, cancel it!',
            cancelButtonText: 'No, do not cancel plx!',
            closeOnConfirm: false,
            closeOnCancel: false
        },
        function (isConfirm) {
            if (isConfirm) {
                $('.confirm_').click();
                swal('Cancelled!', 'Your registration has been cancelled.', 'success');
                return true;
            } else {
                swal('Calm...', 'We have not cancelled your registration :)', 'error');
                return false;
            }
        });
}



function manage_likeAct(id, url) {
    if (url) {
        url = '/' + url + '/like'
    } else {
        url = 'like'
    }
    $.ajax({
        url: url,
        type: 'post',
        sync: true,
        data: $('#likeAct_form_' + id).serialize(),
        dataType: 'json',
        success: function (data) {
            if (id.indexOf("actividad") == 0) {
                change_text_to_show_like(id, data);
                change_text_to_show_like(id.substring(7), data);
            } else {
                change_text_to_show_like(id, data);
                change_text_to_show_like('likeAct' + id, data);
            }
        },
        error: function (data) {
            alert("An unexpected error has happened");
        }
    });
};




function change_text_to_show_like(id, data) {

    if (data["status"] === "unliked") {
        $("#actividad_like_" + id).html(data["number_of_likes"]);
        // TODO: use i18n engine
        $("#submit_likeAct_" + id).removeClass("corazon");
        $("#submit_likeAct_" + id).addClass("corazon_gray");
        $("#card_" + id).toggleClass("panel-success");
    } else {
        $("#actividad_like_" + id).html(data["number_of_likes"]);
        // TODO: use i18n engine
        $("#submit_likeAct_" + id).removeClass("corazon_gray");
        $("#submit_likeAct_" + id).addClass("corazon");
        $("#card_" + id).toggleClass("panel-success");
    }
}

