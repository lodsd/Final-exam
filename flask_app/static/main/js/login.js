let count     = 0
function checkCredentials() {
    // package data in a JSON object
    let email = $('input#input-email').val()
    let password = $('input#input-password').val()
    var data_d = {'email': email, 'password': password}
    console.log('data_d', data_d)

    // SEND DATA TO SERVER VIA jQuery.ajax({})
    jQuery.ajax({
        url: "/processlogin",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
              retruned_data = JSON.parse(retruned_data);
              if(retruned_data['success'] == 1){
                window.location.href = "/home";
              }else{
                count++;
                if(count != 0){
                    let failure_login = $("p#failure-login")
                    failure_login.text(`Authentication failure: ${count} `)
                }
              }
            }
    });
}