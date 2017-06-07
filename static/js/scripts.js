/**
 * Created by Mathi_000 on 6/06/2017.
 */

$(document).ready(function()
{
    if (typeof window.sessionStorage != undefined){
        if (!sessionStorage.getItem('mySessionVal')){
            document.getElementById('flash').style.display = "block";
            $("#flash").fadeIn("slow").delay(2500).fadeOut("slow");
            sessionStorage.setItem('mySessionVal', true);
            sessionStorage.setItem('storedWhen', Date.now());
        }
    }
});

