/**
 * Created by Mathi_000 on 6/06/2017.
 */
var delayMillis = 500; //1 second

setTimeout(function() {
  //your code to be executed after 1 second
    $(document).ready(function()
{
    if (typeof window.sessionStorage != undefined){
        if (!sessionStorage.getItem('mySessionVal')){

            document.getElementById('flash').style.display = "block";
            $("#flash").fadeIn("slow").delay(2000).fadeOut("slow");
            sessionStorage.setItem('mySessionVal', true);
            sessionStorage.setItem('storedWhen', Date.now());
        }
    }
});
}, delayMillis);



