/**
 * Created by Mathi_000 on 6/06/2017.
 */
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


function register() {
    document.getElementById('login-page').style.display = "none";
    document.getElementById('register-button').style.opacity = "0.8";
    document.getElementById('login-button').style.opacity = "1";
    document.getElementById('register-page').style.display = "block";
     $("#register-page").fadeIn("slow");
}

function login() {
    document.getElementById('register-page').style.display = "none";
    document.getElementById('login-button').style.opacity = "0.8";
    document.getElementById('register-button').style.opacity = "1";
    document.getElementById('login-page').style.display = "block";
    $("#login-page").fadeIn("slow");
}

function refreshPage(){
    window.location.reload();
}