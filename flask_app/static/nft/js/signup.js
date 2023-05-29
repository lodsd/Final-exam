function signup(){
    var data_d = {
        'email' : document.getElementById('email').value,
        'password' : document.getElementById('password').value,
    }
    jQuery.ajax({
        url: "/nft_signup",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
              retruned_data = JSON.parse(retruned_data);
              if(retruned_data['success']){
                window.location.href = "/nft_login";
              }
            }
    });
}