var lama_game_id='';
var lama_player_id='';

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
        },
        error: function(jqXHR, status, error) {
            console.log('Error joining game');
            console.log(error);
            $("#lama-player-id").html('Error joining game');
        }
    });
};

$(document).ready(function(){
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
});
