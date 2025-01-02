(function ($) {
    "use strict";

   
    $('#myTerminal').terminal(function(command, term) {
         if (command === 'clear'){
            term.clear();
        } else if (command === 'movie') {
            term.pause();
            fetch('https://portfolio.iyadelwy.xyz/cmd', {
                method: 'POST'
            }).then(function (response) {
                return response.json();
            }).then(function (data) {
                term.echo(data.result);
                term.resume()
            }).catch(function (err) {
                term.error("Network Error: Your command did not reach the host machine.");
                term.resume();
            });

        }
    }, {
        greetings: 'Welcome to my terminal!',
        prompt: '> '
    });
    
})(jQuery);

