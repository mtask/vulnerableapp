window.onload = function() {
     var url = window.location.href
     if ( url.indexOf('/home/id/') !== -1 ) {
         document.getElementById('home_form').style.display = "none";
     }
}