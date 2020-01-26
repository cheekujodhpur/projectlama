var game_status_poller = null;

var purl = 'http://localhost:1144';
//var purl = 'https://llama.kumar-ayush.com';

function stateHandler(data) {
    var myAlias = readCookie("alias");
    // Display all players
    $("#l-lobby-members").html('');
    data.players.forEach(function(name) {
        if (name == myAlias) {
            var listitem = '<li class="list-group-item list-group-item-primary">' + name  + '</li>';
        }
        else {
            var listitem = '<li class="list-group-item">' + name  + '</li>';
        };
        $("#l-lobby-members").append(listitem);
    });
};

function queryState() {
    var lama_game_id = readCookie("gameid");
    var lama_player_token = readCookie("playertoken");
    $.xmlrpc({
        url: purl,
        methodName: 'query_state',
        params: [lama_game_id, lama_player_token],
        success: function(res, status, jqXHR) {
            stateHandler(res[0]);
        },
        error: function(jqXHR, status, error) {
            console.log('Encountered an error');
            console.log(error);
        }
    });
    game_status_poller = setTimeout(queryState, 500);
};

function push_input(inp) {
    $.xmlrpc({
        url: purl,
        methodName: 'push_input',
        params: [lama_game_id, lama_player_id, inp],
        success: function(res, status, jqXHR) {
            // console.log(res);
        },
        error: function(jqXHR, status, error) {
            // console.log('Error sending input');
            // console.log(error);
        }
    });
};

function createGame() {
    $.xmlrpc({
        url: purl,
        methodName: 'open',
        params: [],
        success: function(res, status, jqXHR) {
            var lama_game_id=res[0];
            setCookie("gameid", lama_game_id, 1);
            joinGame(lama_game_id);
        },
        error: function(jqXHR, status, error) {
            console.log("Error opening game");
            console.log(error);
        }
    });
};

var dbg = null;

function joinGame(game_id) {
    var alias = readCookie("alias");
    $.xmlrpc({
        url: purl,
        methodName: 'join',
        params: [game_id, alias],
        success: function(res, status, jqXHR) {
            var lama_player_token=res[0]['token'];
            // set if new joiner
            if (readCookie(game_id) == null)
                setCookie("gameid", game_id);

            setCookie("playertoken", lama_player_token, 1);
            $("#l-menu-form").submit();
        },
        error: function(jqXHR, status, error) {
            console.log('Error joining game');
            dbg = error;
            console.log(error);
        }
    });
};

$(document).ready(function(){
    $("#btn-play").children().click(function(el){
        push_input($(this).attr("llama-val"));
    });

    $("#btn-play-draw").click(function(){
        push_input("Draw");
    });

    $("#btn-play-fold").click(function(){
        push_input("Fold");
    });

    $("#btn-start-game").click(function(){
        $.xmlrpc({
            url: purl,
            methodName: 'start_game',
            params: [lama_game_id, lama_player_id],
            success: function(res, status, jqXHR) {
                $("#btn-start-game").hide();
            },
            error: function(jqXHR, status, error) {
                // console.log('Error starting game');
                // console.log(error);
            }
        });
    });
});
