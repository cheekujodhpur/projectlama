var game_status_poller = null;

var purl = 'http://localhost:1144';
//var purl = 'https://llama.kumar-ayush.com';

var stateMap = {
    'none': lobbyWaitHandler,
    'round_running': roundRunHandler
};

function myTurnHandler(data) {
    var msg = "It is your turn. You can ";
    if (data.expected_action == "PF")
        msg += "play or fold.";
    else if (data.expected_action == "FD")
        msg += "draw or fold.";
    else
        msg += "<exterminate>";

    $("#l-lobby-message-container").html(msg);
};

function roundRunHandler(data) {
    if ("my_turn" in data) {
        myTurnHandler(data);
    }
    else {
        var msg = "Whose turn is it? " + data.whose_turn;
        $("#l-lobby-message-container").html(msg);
    }
    renderHand(data.hand);
};

function lobbyWaitHandler(data) {
    var myAlias = readCookie("alias");
    var gameId = readCookie("gameid");

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

    // print message
    var msg = "Waiting for lobby master to start the game.<br />";
    if( data.players.length < 6 ) {
        msg = msg + "Invite players with game id <b>" + gameId + "</b>.<br />";
    }
    else {
        msg = msg + "Lobby is full.<br />";
    };
    $("#l-lobby-message-container").html(msg);

    // display the start button
    if (data.players[0] == myAlias)
        $("#l-start-game-button").removeClass("d-none");
};

function defaultStateHandler(data) {
    if ("error" in data) {
        alert(data.error);
    };
};

function stateHandler(data) {
    if (data["game_state"] in stateMap)
        stateMap[data["game_state"]](data);
    else
        defaultStateHandler(data);
};

function renderHand(cards) {
    var card_list = '<ul>';
    cards.forEach(function(card) {
        card_list += '<li>' + card + '</li>';
    });
    card_list += '</ul>';
    $("#l-game-content-container").html(card_list);
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

function revealGame() {
    $("#l-game-content-container").removeClass('d-none');
    $("#l-sidebar").removeClass("toggled");
    $("#l-start-game-button").hide();
};

function startGame() {
    var lama_game_id = readCookie("gameid");
    var lama_player_token = readCookie("playertoken");
    $.xmlrpc({
        url: purl,
        methodName: 'start_game',
        params: [lama_game_id, lama_player_token],
        success: function(res, status, jqXHR) {
            revealGame();
            setCookie("started", 1, 1);
            stateHandler(res[0]);
        },
        error: function(jqXHR, status, error) {
            console.log('Error starting game');
            console.log(error);
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

function joinGame(game_id) {
    var alias = readCookie("alias");
    game_id = game_id.toUpperCase();
    $.xmlrpc({
        url: purl,
        methodName: 'join',
        params: [game_id, alias],
        success: function(res, status, jqXHR) {
            if("error" in res[0]) {
                alert(res[0]["error"]);
                return;
            };
            // else go on
            var lama_player_token=res[0]['token'];
            // set if new joiner
            if (readCookie(game_id) == null)
                setCookie("gameid", game_id);

            setCookie("playertoken", lama_player_token, 1);
            $("#l-menu-form").submit();
        },
        error: function(jqXHR, status, error) {
            console.log('Error joining game');
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
