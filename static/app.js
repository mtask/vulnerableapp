window.onload = function() {
     var url = window.location.href
     if ( url.indexOf('/home/id/') !== -1 ) {
         document.getElementById('home_form').style.display = "none";
         document.getElementById('comment_feed').style.display = "none";
     }
}

window.onload = document.getElementById('srchterm').onkeypress = function(e){
    if (!e) e = window.event;
    var keyCode = e.keyCode || e.which;
    if (keyCode == '13'){
      sendsrch();
      return false;
    }
  }

function sendsrch(){
    var term = document.getElementById("srchterm").value;
    location.href = "/search?term="+unescape(term);
}
