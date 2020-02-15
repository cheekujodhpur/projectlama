var game_status_poller = null;

var purl = 'http://localhost:1144';
//var purl = 'https://llama.kumar-ayush.com';

var stateMap = {
    'none': lobbyWaitHandler,
    'round_running': roundRunHandler
};

var colorMap = {
    '1': '#e00',
    '2': '#0e0',
    '3': '#00e',
    '4': '#ee0',
    '5': '#0ee',
    '6': '#e0e',
    '7': '#eee'
}

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
    renderDiscardPile(data.top_card);
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

var globalStateStore = null;
function stateHandler(data) {
    if (JSON.stringify(data) === JSON.stringify(globalStateStore))
        return;
    globalStateStore = data;
    if (data["game_state"] in stateMap)
        stateMap[data["game_state"]](data);
    else
        defaultStateHandler(data);
};

function renderCard(card, playable=false) {
    bgStyle = 'style="background-image:linear-gradient(to right,' + colorMap[card] + ', #fff)"'; 
    card_text = card == '7' ? 'llama' : card;
    card_html = '<li ' + bgStyle + '>' + card_text + '</li>';

    jel = $(card_html);
    if (playable) {
        jel.attr('onclick', 'playCard(this)');
        jel.attr('l-data', card);
    }
    return jel;
}

function renderDiscardPile(card) {
    card_html = renderCard(card);
    $("#l-discard").append(card_html);
};

function renderHand(cards) {
    $("#l-hand").html('');
    cards.forEach(function(card) {
        card_html = renderCard(card, playable=true);
        $("#l-hand").append(card_html);
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

function playCard(elem) {
    inp = $(elem).attr('l-data');
    pushInput(inp);
};

function pushInput(inp) {
    var lama_game_id = readCookie("gameid");
    var lama_player_token = readCookie("playertoken");
    $.xmlrpc({
        url: purl,
        methodName: 'push_input',
        params: [lama_game_id, lama_player_token, inp],
        success: function(res, status, jqXHR) {
        },
        error: function(jqXHR, status, error) {
            console.log('Error sending input');
            console.log(error);
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
                setCookie("gameid", game_id, 1);

            setCookie("playertoken", lama_player_token, 1);
            $("#l-menu-form").submit();
        },
        error: function(jqXHR, status, error) {
            console.log('Error joining game');
            console.log(error);
        }
    });
};
