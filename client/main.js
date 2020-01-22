const cookie_list = [ "alias", "gameid", "playertoken" ];

function setCookie(key, value, expiry) {
    var expires = new Date();
    expires.setTime(expires.getTime() + (expiry * 24 * 60 * 60 * 1000));
    document.cookie = key + '=' + value + ';expires=' + expires.toUTCString();
};

function readCookie(key) {
    var keyValue = document.cookie.match('(^|;) ?' + key + '=([^;]*)(;|$)');
    return keyValue ? keyValue[2] : null;
};

function eraseCookie(key) {
    setCookie(key, "", -1);
};

$(document).ready(function(){
    var alias = readCookie("alias");
    var gameid = readCookie("gameid");
    if(gameid != null) {
        $("#l-lobby-container").removeClass("d-none");
        var listitem = '<li class="list-group-item">' + alias + '</li>';
        $("#l-lobby-members").append(listitem);
    }
    else if(alias != null) {
        $("#l-menu-container").removeClass("d-none");
    }
    else {
        $("#l-clear-container").addClass("d-none");
        $("#l-alias-container").removeClass("d-none");
    };
    $("#l-topbar").html(alias);

    // focus on alias textbox
    $("#l-alias").focus();

    // alias form
    $("#l-alias-form").submit(function(e) {
        alias = $("#l-alias").val();
        $("#l-alias").val("");
        if(alias === "")
            alias = "Anonymous";

        setCookie("alias", alias, 1);
    });

    $("#l-clear-form").submit(function(e) {
        cookie_list.forEach(function(x) {
            eraseCookie(x);
        });
    });

    // Menu items
    $("#l-create-button").click(function(){
        createGame(); 
    });
});
