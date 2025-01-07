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
        greetings: 'Welcome to the Movie data interactive terminal tool. Use the "movies --help" command to get started.\n\nThis environment was carefully designed to ensure robustness and security by integrating docker containers, networks and volumes as well as cloudflare VPN, Apache Airflow and linux shell environments.\n\nTo know more about how this environment was built check out the "Portfolio Projects" section down bellow to access the project\'s GitHub Page.\n\n\n',
        prompt: '> '
    });
    
})(jQuery);

