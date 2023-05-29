let sequence = ''
function appendSequences(char){
    sequence += char;
    // when the sequence beyond 8, substring it.
    if(sequence.length === 9){
        sequence = sequence.substring(1,9)
    }
    if (sequence === 'WESEEYOU'){
        let pianoBackground = document.getElementById('piano-background');
        pianoBackground.style.display = 'none';
        let greatOldOne = document.getElementById('great-old-one');
        greatOldOne.style.display = 'block';
        
        let player = new Audio('https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1')
        player.play();
    }
    
}
window.onload = function() {
    // Use constants to save audios' url
    const sound = {65:"http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
    87:"http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
    83:"http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
    69:"http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
    68:"http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
    70:"http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
    84:"http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
    71:"http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
    89:"http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
    72:"http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
    85:"http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
    74:"http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
    75:"http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
    79:"http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
    76:"http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
    80:"http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
    186:"http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"};
    // click listener for white keys
    let pianoKeys = document.querySelectorAll('.piano-white-key');
    pianoKeys.forEach(function(key) {
        key.addEventListener('click', function() {
            let player;
            switch (key.id) {
                case 'piano-key-A':
                    appendSequences('A')
                    player = new Audio(sound[65]);
                    break;
                case 'piano-key-S':
                    appendSequences('S')
                    player = new Audio(sound[87]);
                    break;
                case 'piano-key-D':
                    appendSequences('D')
                    player = new Audio(sound[83]);
                    break;
                case 'piano-key-F':
                    appendSequences('F')
                    player = new Audio(sound[69]);
                    break;
                case 'piano-key-G':
                    appendSequences('G')
                    player = new Audio(sound[68]);
                    break;
                case 'piano-key-H':
                    appendSequences('H')
                    player = new Audio(sound[70]);
                    break;
                case 'piano-key-J':
                    appendSequences('J')
                    player = new Audio(sound[84]);
                    break;
                case 'piano-key-K':
                    appendSequences('K')
                    player = new Audio(sound[71]);
                    break;
                case 'piano-key-L':
                    appendSequences('L')
                    player = new Audio(sound[89]);
                    break;
                case 'piano-key-Semicolon':
                    appendSequences(';')
                    player = new Audio(sound[72]);
                    break;
            }
            player.play();
            // update key's style to reflect that it has been pressed
            key.style.transform = 'scale(0.9)'
            setTimeout(() => {
                key.style.transform = 'scale(1)'
            }, 200);
        }, false);
    })
    // click listener for black keys
    let pianoBlackKeys = document.querySelectorAll('.piano-black-key');
    pianoBlackKeys.forEach((key) => {
        key.addEventListener('click', () => {
            let player;
            switch (key.id){
                case 'piano-black-key-W':
                    appendSequences('W')
                    player = new Audio(sound[85]);
                    break;
                case 'piano-black-key-E':
                    appendSequences('E')
                    player = new Audio(sound[74]);
                    break;
                case 'piano-black-key-T':
                    appendSequences('T')
                    player = new Audio(sound[75]);
                    break;
                case 'piano-black-key-Y':
                    appendSequences('Y')
                    player = new Audio(sound[79]);
                    break;
                case 'piano-black-key-U':
                    appendSequences('U')
                    player = new Audio(sound[76]);
                    break;
                case 'piano-black-key-O':
                    appendSequences('O')
                    player = new Audio(sound[80]);
                    break;
                case 'piano-black-key-P':
                    appendSequences('P')
                    player = new Audio(sound[186]);
                    break;
            }
            player.play();
            key.style.transform = 'scale(0.9)'
            setTimeout(() => {
                key.style.transform = 'scale(1)'
            }, 200);
            
        },false)
    })
}   

// set keyboard keys when the mouse hovers over any key or not
function setBodyTextDisplay(shown){
    let pianoBody = document.querySelectorAll(".piano-body p");
    pianoBody.forEach(div =>{
        div.style.display = shown;
    })
}