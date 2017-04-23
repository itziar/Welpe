function applyCleaner(idList) {
    for (var index in idList){
        var valor = tinyMCE.get(idList[index]).getContent()
        if (valor){
            html = $.htmlClean(valor);
            $("#"+idList[index]).val(html);
            $("#"+idList[index]).html(html);
            var editor = tinyMCE.get(idList[index]);
            editor.setContent($("#"+idList[index]).val());
        }
    }
}

function selectFile(idUnico, elemToShow){
    html = $("#"+idUnico).val()
    html = html.replace(/^.*[\\\/]/, '');
    document.getElementById(elemToShow).value = html;
}