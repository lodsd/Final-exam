function openFeedback(){
    let x =document.getElementById("feedback-form")
    x.style.display = 'block'
}

function submitFeedback(){
    const xhr = new XMLHttpRequest()
    const formdata = new FormData()

    formdata.append('name',document.getElementById("name-input").value)
    formdata.append('email',document.getElementById("email-input").value)
    formdata.append('feedback',document.getElementById("feedback-input").value)

    xhr.onloadend = () =>{
        //console.log(xhr.response)
        window.location.href = "./processfeedback";
    }
        
    
    xhr.open('POST','/processfeedback')
    xhr.send(formdata)
}