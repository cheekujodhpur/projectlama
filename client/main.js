$(document).ready(function(){
    $("#btn-create-game").click(function(){
        $.xmlrpc({
            url: 'http://localhost:1144',
            methodName: 'open',
            success: function(res, status, jqXHR) {
                console.log(res);
                console.log(status);
                console.log(jqXHR);
            },
            error: function(jqXHR, status, error) {
                console.log(error);
                console.log(status);
                console.log(jqXHR);
            }
        });
    });
});
