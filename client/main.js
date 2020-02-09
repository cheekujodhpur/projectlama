const cookie_list = [ "alias", "gameid", "playertoken", "started" ];

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
    var playertoken = readCookie("playertoken");
    var started = readCookie("started");
    if (gameid != null && playertoken != null) {
        $("#l-game-container").removeClass("d-none");
        if (started != null)
            revealGame();
        queryState();
    }
    else if (alias != null) {
        $("#l-menu-container").removeClass("d-none");
    }
    else {
        $("#l-clear-container").addClass("d-none");
        $("#l-alias-container").removeClass("d-none");
    };
    $("#l-topbar-info").html(alias);
    if(gameid != null)
        $("#l-topbar-info").append(' - ' + gameid);

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
    $("#l-create-button").click(function() {
        createGame(); 
    });

    $("#l-start-game-button").click(function() {
        startGame();
    });

    $("#l-sidebar-toggle").click(function() {
        $("#l-sidebar").toggleClass("toggled");
    });

    $("#l-menu-form").submit(function(e) {
        var join_game_id = $("#l-join-game-id").val();
        $("#l-join-game-id").val('');
        if(join_game_id.length > 0) {
            joinGame(join_game_id);
            e.preventDefault();
        };
    });
});
