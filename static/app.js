const $form  = $('#form');
const $feedback = $('#feedback')
const $score = $('#score')
const $timer = $(`#timer`)
const $startBtn = $('#startBtn');
const $resetBtn = $('#resetBtn')
$form.hide()

$form.on('submit', function(e){
    e.preventDefault()
    let formValue = e.target.guess.value
    checkWord(formValue)
    e.target.guess.value = ''
})

async function checkWord(guess){
    
    let res = await axios.get(
        "/check-word", {params:{guess}}
    );
    console.log(typeof(res))
    displayMessage(res.data.feedback, res.data.score)
}

async function reset(){
    
    let res = await axios.post(
        "/reset-game"
    );
    window.location.reload()
    console.log(res)
    
}

function displayMessage(msg, score){
    console.log(msg)
    $feedback.text(`${msg}`)
    $score.text(`Score: ${score}`)
}

function startClock(startTime){
    let start =startTime;
    let myInterval = setInterval(function(){
        if(start >  0){
            start -= 1
            $timer.text(`${start} seconds`)
        }else{
            $timer.text('Game Over');
            clearInterval(myInterval)
            $form.hide()
        }
        
    },1000)
}

$startBtn.on('click', function(){
    $startBtn.hide();
    $form.show();
    startClock(60)
})

$resetBtn.on('click', function(){
    reset();
})