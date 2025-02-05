(function ($) {
    "use strict";

   
    $('#myTerminal').terminal(function(command, term) {
         if (command === 'clear'){
            term.clear();
        } else if (command !== '') {
            term.pause();
            fetch('https://portfolio.iyadelwy.xyz/cmd', {
                method: 'POST',
                body: JSON.stringify({command: command}),
                headers: {
                    "Content-Type": "application/json",
                  },
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
        greetings: `
              ░▒▓██████████████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓████████▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓█▓▒░         
              ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░         
              ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░         
              ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░        ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░         
              ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░         
              ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░         
              ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░   ░▒▓██▓▒░  ░▒▓█▓▒░▒▓████████▓▒░       ░▒▓██████▓▒░░▒▓████████▓▒░▒▓█▓▒░         

                                                                              
Welcome to the Movie data interactive terminal tool. Use the "movies --help" command to get started.\n\nThis environment was carefully designed to ensure robustness and security by running it on my own self-hosted Kubernetes Multi-Node cluster, running in my kitchen :)\n\nTo know more about how this environment was built check out the "Portfolio Projects" section down bellow to access the project\'s GitHub Page.\n\nTo get started type "movies --help"\n\n\n`,
        prompt: '> '
    });
    
})(jQuery);

