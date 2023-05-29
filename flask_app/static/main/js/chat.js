var socket;
    $(document).ready(function(){
        
        socket = io.connect('https://' + document.domain + ':' + location.port + '/chat');
        socket.on('connect', function() {
            socket.emit('joined', {});
        });
        
        socket.on('status', function(data) {     
            let tag  = document.createElement("p");
            let text = document.createTextNode(data.msg);
            let element = document.getElementById("chat");
            tag.appendChild(text);
            tag.style.cssText = data.style;
            element.appendChild(tag);
            $('#chat').scrollTop($('#chat')[0].scrollHeight);

        });
        let message = $('input#message');
        message.keypress(function(e) {
            if (e.which == 13) {
                data = message.val()
                message.attr('value','')
                socket.emit('send', {msg : data})
            }
        });  
        $('input#leave').click(function(event) {
            socket.emit('leave', {},function () { 
                socket.disconnect();
                window.location.href = '/home';
            });
        })    
    });