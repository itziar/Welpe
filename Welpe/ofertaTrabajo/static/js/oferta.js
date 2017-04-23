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
    } else if (elemToShow == "proposicion") {
        a = $("#allow_papers_" + idUnico);
    }
    else if (elemToShow == "limit") {
        a = $("#limit_span_" + idUnico);
    } else if (elemToShow == "lopdText") {
        a = $("#show_" + elemToShow + "_" + idUnico)
    }
    if ($(event.target).prop("checked")) {
        a.show();
        if (elemToShow == "inscripcion" || elemToShow == "proposicion") {
            $("#fecha_" + elemToShow + "_inicial_" + idUnico).prop('required', true);
            $("#fecha_" + elemToShow + "_final_" + idUnico).prop('required', true);
        } else if (elemToShow != "lopdText") {
            $("#" + elemToShow + "_" + idUnico).prop('required', true);
        }
    } else {
        a.hide();
        if (elemToShow == "inscripcion" || elemToShow == "proposicion") {
            $("#fecha_" + elemToShow + "_inicial_" + idUnico).prop('required', false);
            $("#fecha_" + elemToShow + "_final_" + idUnico).prop('required', false);
        } else if (elemToShow != "lopdText") {
            $("#" + elemToShow + "_" + idUnico).prop('required', false);
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

function manage_likeOferta(id, url) {
    if (url) {
        url = '/' + url + '/like'
    } else {
        url = 'like'
    }
    $.ajax({
        url: url,
        type: 'post',
        sync: true,
        data: $('#likeOferta_form_' + id).serialize(),
        dataType: 'json',
        success: function (data) {
            if (id.indexOf("oferta") == 0) {
                change_text_to_show(id, data);
                change_text_to_show(id.substring(7), data);
            } else {
                change_text_to_show(id, data);
                change_text_to_show('likeOferta' + id, data);
            }
        },
        error: function (data) {
            alert("An unexpected error has happened");
        }
    });
};

function change_text_to_show(id, data) {

    if (data["status"] === "unliked") {
        $("#oferta_like_" + id).html(data["number_of_likes"]);
        // TODO: use i18n engine
        $("#submit_likeOferta_" + id).removeClass("corazon");
        $("#submit_likeOferta_" + id).addClass("corazon_gray");
        $("#card_" + id).toggleClass("panel-success");
    } else {
        $("#oferta_like_" + id).html(data["number_of_likes"]);
        // TODO: use i18n engine
        $("#submit_likeOferta_" + id).removeClass("corazon_gray");
        $("#submit_likeOferta_" + id).addClass("corazon");
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






