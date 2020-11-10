var game_status_poller = null;

var purl = 'http://localhost:1144';
//var purl = 'https://llama.kumar-ayush.com';

var stateMap = {
    'none': lobbyWaitHandler,
    'round_running': roundRunHandler,
    'game_over': gameOverHandler
};

var colorMap = {
    '1': '#e74c3c',
    '2': '#8e44ad',
    '3': '#3498db',
    '4': '#2ecc71',
    '5': '#16a085',
    '6': '#e67e22',
    '7': '#34495e'
};

var imageMap = {
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'llama'
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

function gameOverHandler(data) {
  $("#l-new-game-button").removeClass("d-none");
};

function newGame() {
  let cookie_list = [ "gameid", "playertoken", "started" ];
  cookie_list.forEach(x => {
      eraseCookie(x);
  });
  location.reload();
}

function roundRunHandler(data) {
    revealGame();
    if ("my_turn" in data) {
        myTurnHandler(data);
    }
    else {
        var msg = "Whose turn is it? " + data.whose_turn;
        $("#l-lobby-message-container").html(msg);
    };
    renderHand(data.hand);
    renderDiscardPile(data.top_card, data.top_card_v);
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
    console.log(data);
    if ("error" in data) {
        alert(data.error);
    };
};

function messageHandler(data) {
    var currentDate = new Date();
    var time = currentDate.toLocaleTimeString('en-US', {
        hour12: false,
        hour: "numeric",
        minute: "numeric"
    });

    if ('message' in data && data['message'].length > 0) {
        data['message'].forEach(function(message) {
            procMessage = "<b>" + time + "</b>: " + message + "<br />";
            $("#l-lobby-log-container").prepend(procMessage);
        });
    };

    if('score' in data && data['score'].length > 0) {
        freshenDiscardPile();
        data['score'].forEach(function(message) {
            if (Array.isArray(message)) {
                // display score
                var table = "<table class='table'>";
                table +=    "<thead><tr><th scope='col'>Player</th><th scope='col'>Score</th></tr></thead>";
                table +=    "<tbody>";
                message.forEach(function(playerScore) {
                    table += "<tr><td>" + playerScore[0] + "</td><td>" + playerScore[1] + "</td></tr>";
                });
                table +=    "</tbody></table>";
                var preMessage = "<b>" + time + "</b>: Round over<br />";
                $("#l-lobby-log-container").prepend(preMessage);
                $("#l-lobby-log-container").prepend(table);
            }
            else {
                winner = message['winner']
                var procMessage = "<b>" + time + "</b>: <span class='l-player-name'>" + winner + "</span> wins.<br />";
                $("#l-lobby-log-container").prepend(procMessage);
            }
        });
    };
};

var globalStateStore = null;
function stateHandler(data) {
    if (JSON.stringify(data) === JSON.stringify(globalStateStore))
        return;
    globalStateStore = data;

    // first message handling
    messageHandler(data);

    if (data["game_state"] in stateMap)
        stateMap[data["game_state"]](data);
    else
        defaultStateHandler(data);

};

function renderCard(card, count, playable=false) {
    var card_image_name = imageMap[card];
    if (count === undefined) {
      card_text = '';
    } else {
      card_text = '<span class="l-multiple">' + count + '</span>';
    }
    card_html = '<li>' + card_text + '</li>';

    jel = $(card_html);
    jel.attr('l-data', card);
    if (playable) {
        jel.attr('onclick', 'playCard(this)');
    }
    return jel;
}

var discardPile_v = null;
function freshenDiscardPile() {
    discardPile_v = null;
    $("#l-discard").html('');
};

function renderDiscardPile(card, card_v) {
    if (card_v == discardPile_v)
        return;

    card_html = renderCard(card);
    $("#l-discard").html(card_html);
    discardPile_v = card_v;
};

function renderHand(cards) {
    let cardset = cards.sort().reduce(function(rv, x) {rv[x] = rv[x] || 0; rv[x] += 1; return rv;}, {});
    $("#l-hand").html('');
    Object.entries(cardset).forEach(([card, count]) => {
        card_html = renderCard(card, count, playable=true);
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
