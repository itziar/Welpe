
function manage_likePropuesta(id, url) {
    if (url) {
        url = '/' + url + '/like'
    } else {
        url = 'like'
    }
    $.ajax({
        url: url,
        type: 'post',
        sync: true,
        data: $('#likePropuesta_form_' + id).serialize(),
        dataType: 'json',
        success: function (data) {
            if (id.indexOf("propuesta") == 0) {
                change_text_to_show(id, data);
                change_text_to_show(id.substring(7), data);
            } else {
                change_text_to_show(id, data);
                change_text_to_show('likePropuesta' + id, data);
            }
        },
        error: function (data) {
            alert("An unexpected error has happened");
        }
    });
};

function change_text_to_show(id, data) {

    if (data["status"] === "unliked") {
        $("#propuesta_like_" + id).html(data["number_of_likes"]);
        // TODO: use i18n engine
        $("#submit_likePropuesta_" + id).removeClass("corazon");
        $("#submit_likePropuesta_" + id).addClass("corazon_gray");
        $("#card_" + id).toggleClass("panel-success");
    } else {
        $("#propuesta_like_" + id).html(data["number_of_likes"]);
        // TODO: use i18n engine
        $("#submit_likePropuesta_" + id).removeClass("corazon_gray");
        $("#submit_likePropuesta_" + id).addClass("corazon");
        $("#card_" + id).toggleClass("panel-success");
    }
}
