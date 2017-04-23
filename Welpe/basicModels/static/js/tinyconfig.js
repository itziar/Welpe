
var language_codes = {
    'ar': 'ar',
    'ca': 'ca',
    'cs': 'cs',
    'da': 'da',
    'de': 'de',
    'es': 'es',
    'et': 'et',
    'fa': 'fa',
    'fa_IR': 'fa_IR',
    'fi': 'fi',
    'fr': 'fr_FR',
    'hr_HR': 'hr',
    'hu': 'hu_HU',
    'id_ID': 'id',
    'is_IS': 'is_IS',
    'it': 'it',
    'ja': 'ja',
    'ko': 'ko_KR',
    'lv': 'lv',
    'nb': 'nb_NO',
    'nl': 'nl',
    'pl': 'pl',
    'pt_BR': 'pt_BR',
    'pt_PT': 'pt_PT',
    'ru': 'ru',
    'sk': 'sk',
    'sr': 'sr_Latn',
    'sv': 'sv_SE',
    'tr': 'tr',
    'uk': 'uk_UA',
    'vi': 'vi',
    'zh_CN': 'zh_CN',
    'zh_TW': 'zh_TW'
};

function custom_file_browser(field_name, url, type, win) {
    tinyMCE.activeEditor.windowManager.open({
        title: 'Select ' + type + ' to insert',
        file: window.__filebrowser_url + '?pop=5&type=' + type,
        width: 800,
        height: 500,
        resizable: 'yes',
        scrollbars: 'yes',
        inline: 'yes',
        close_previous: 'no'
    }, {
        window: win,
        input: field_name
    });
    return false;
}

jQuery(function($) {

    if (typeof tinyMCE != 'undefined') {

        tinyMCE.init({
            selector: "textarea.mceEditor",
            height: '500px',
            language: language_codes[window.__language_code] || 'en',
            plugins: [
                "advlist autolink lists link image charmap print preview anchor",
                "searchreplace visualblocks code fullscreen",
                "insertdatetime media table contextmenu paste"
            ],
            link_list: '/displayable_links.js',
            relative_urls: false,
            convert_urls: false,
            menubar: false,
            statusbar: false,
            toolbar: ("insertfile undo redo | styleselect | bold italic | " +
                      "alignleft aligncenter alignright alignjustify | " +
                      "bullist numlist outdent indent | link image table | " +
                      "code fullscreen"),
            file_browser_callback: custom_file_browser,
            content_css: window.__tinymce_css,
             style_formats: [

{title: 'Headers', items: [
  {title: 'Header 1', format: 'h1'},
  {title: 'Header 2', format: 'h2'},
  {title: 'Header 3', format: 'h3'},
  {title: 'Header 4', format: 'h4'},
  {title: 'Header 5', format: 'h5'},
  {title: 'Header 6', format: 'h6'}
 ]},
 {title: 'Inline', items: [
  {title: 'Bold', icon: 'bold', format: 'bold'},
  {title: 'Italic', icon: 'italic', format: 'italic'},
  {title: 'Underline', icon: 'underline', format: 'underline'},
  {title: 'Strikethrough', icon: 'strikethrough', format: 'strikethrough'},
  {title: 'Superscript', icon: 'superscript', format: 'superscript'},
  {title: 'Subscript', icon: 'subscript', format: 'subscript'},
  {title: 'Code', icon: 'code', format: 'code'}
 ]},
 {title: 'Blocks', items: [
  {title: 'Paragraph', format: 'p'},
  {title: 'Blockquote', format: 'blockquote'},
  {title: 'Div', format: 'div'},
  {title: 'Pre', format: 'pre'},
   {title: 'Code', block: 'pre', classes: "prettyprint"}
 ]},
 {title: 'Alignment', items: [
  {title: 'Left', icon: 'alignleft', format: 'alignleft'},
  {title: 'Center', icon: 'aligncenter', format: 'aligncenter'},
  {title: 'Right', icon: 'alignright', format: 'alignright'},
  {title: 'Justify', icon: 'alignjustify', format: 'alignjustify'}
 ]}
]
        });

    }

});


