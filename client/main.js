var lama_game_id='';
var lama_player_id='';
var game_status_poller = null;

function join_game(game_id) {
    $.xmlrpc({
        url: 'http://localhost:1144',
        methodName: 'join',
        params: [game_id],
        success: function(res, status, jqXHR) {
            lama_game_id=game_id
            $("#lama-game-id").html(lama_game_id);

            lama_player_id=res[0];
            $("#lama-player-id").html(lama_player_id);
            console.log(`Game ${lama_game_id} joined wih id ${lama_player_id}`);

            // disable button
            $("#join-game-group").hide();
            $("#btn-create-game").hide();

            query_state();
        },
        error: function(jqXHR, status, error) {
            console.log('Error joining game');
            console.log(error);
            $("#lama-player-id").html('Error joining game');
        }
    });
};

function query_state() {
    $.xmlrpc({
        url: 'http://localhost:1144',
        methodName: 'query_state',
        params: [lama_game_id, lama_player_id],
        success: function(res, status, jqXHR) {
            console.log(res);
            $("#game-status").html(res);
        },
        error: function(jqXHR, status, error) {
            console.log('Error');
            console.log(error);
        }
    });
    game_status_poller = setTimeout(query_state, 500);
};

$(document).ready(function(){
    // hide until needed
    $("#btn-start-game").hide();

    $("#btn-create-game").click(function(){
        $.xmlrpc({
            url: 'http://localhost:1144',
            methodName: 'open',
            params: [],
            success: function(res, status, jqXHR) {
                lama_game_id=res[0];
                $("#lama-game-id").html(lama_game_id);

                console.log(`Game opened wih id ${lama_game_id}`);
                join_game(lama_game_id);
                $("#btn-start-game").show();
            },
            error: function(jqXHR, status, error) {
                console.log('Error opening game');
                console.log(error);
                $("#lama-game-id").html('Error opening game');
            }
        });
    });

    $("#btn-join-game").click(function(){
        join_game($("#join-game-id").val());
    });

    $("#btn-push-input").click(function(){
        $.xmlrpc({
            url: 'http://localhost:1144',
            methodName: 'push_input',
            params: [lama_game_id, lama_player_id, $("#push-input").val()],
            success: function(res, status, jqXHR) {
                console.log(res);
            },
            error: function(jqXHR, status, error) {
                console.log('Error sending input');
                console.log(error);
            }
        });
    });

    $("#btn-start-game").click(function(){
        $.xmlrpc({
            url: 'http://localhost:1144',
            methodName: 'start_game',
            params: [lama_game_id, lama_player_id],
            success: function(res, status, jqXHR) {
                $("#btn-start-game").hide();
            },
            error: function(jqXHR, status, error) {
                console.log('Error starting game');
                console.log(error);
            }
        });
    });
});
