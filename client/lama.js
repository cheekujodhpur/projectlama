var lama_game_id='';
var lama_player_token='';
var game_status_poller = null;

var purl = 'http://localhost:1144';
//var purl = 'https://llama.kumar-ayush.com';

function query_state() {
    $.xmlrpc({
        url: purl,
        methodName: 'query_state',
        params: [lama_game_id, lama_player_id],
        success: function(res, status, jqXHR) {
            // console.log(res);

            status_html = '';
            score_html = '';
            if (res[0]["player_action"]=="None")
                status_html += 'Game has not started or it is not your turn<br/>';
            else if (res[0]["player_action"]=="Prompt.PF")
                status_html += 'You can play or fold<br/>';
            else if (res[0]["player_action"]=="Prompt.FD")
                status_html += 'You can draw or fold<br/>';

            if (typeof res[0]["score_package"] != "undefined")
                score_html = res[0]["score_package"] + '<br />';

            status_html += 'Current top card is ' + res[0]["top_card"] + '<br/>';
            player_hand = res[0]["player_hand"].map(function(x){
                if (x==7)
                    return 'llama';
                else
                    return x;
            });
            status_html += 'Your hand is ' + player_hand + '<br/>';

            $("#game-status").html(status_html);
            $("#score-status").append(score_html);
        },
        error: function(jqXHR, status, error) {
            // console.log('Error');
            // console.log(error);
        }
    });
    game_status_poller = setTimeout(query_state, 500);
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
            lama_game_id=res[0];
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
    $.xmlrpc({
        url: purl,
        methodName: 'join',
        params: [game_id, alias],
        success: function(res, status, jqXHR) {
            lama_player_token=res[0]['token'];
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
