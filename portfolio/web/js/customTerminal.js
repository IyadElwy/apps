

(function ($) {
    "use strict";

   
    $('#myTerminal').terminal(function(command, term) {
        if (command !== '') {
            term.echo(`You typed: ${command}`);
        } else {
            term.echo('Please enter a command');
        }
    }, {
        greetings: 'Welcome to my terminal!',
        prompt: '> '
    });
    
})(jQuery);

