$(document).ready(function(){
    PonerCookie();
});

function getCookie(c_name){
  var c_value = document.cookie;
  var c_start = c_value.indexOf(" " + c_name + "=");
  if (c_start == -1){
      c_start = c_value.indexOf(c_name + "=");
  }
  if (c_start == -1){
      c_value = null;
  }else{
      c_start = c_value.indexOf("=", c_start) + 1;
      var c_end = c_value.indexOf(";", c_start);
      if (c_end == -1){
          c_end = c_value.length;
      }
      c_value = unescape(c_value.substring(c_start,c_end));
  }
  return c_value;
}

function setCookie(c_name,value,exdays){
  var exdate=new Date();
  exdate.setDate(exdate.getDate() + exdays);
  var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
  document.cookie=c_name + "=" + c_value +"; path=/";
}

function PonerCookie () {
  if (document.getElementById('msg-cookie')) {

    var myCookie = getCookie('aviso_cookies');
    if (myCookie == null) {
      document.getElementById("msg-cookie").style.display = "block";
      
      document.getElementsByClassName('accept-button')[0].addEventListener('click', function(){
        instalarCookies();
        ocultarBannerCookies();
      }, false);
  	}else{
  		ocultarBannerCookies();
  	}
  }
}

function ocultarBannerCookies () {
  document.getElementById("msg-cookie").style.display="none";
}

function instalarCookies (e) {
  window.removeEventListener('scroll', instalarCookies, false);
  document.getElementsByTagName('body')[0].removeEventListener('click', instalarCookies, false);
  
  if (getCookie('aviso_cookies') == null) setCookie('aviso_cookies','1',365);

}