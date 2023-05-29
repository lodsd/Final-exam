function buyNFT(id){
    var data_d = {
        'nft_id' : id,
    }
    jQuery.ajax({
        url: "/buyNFT",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
            if(retruned_data['success'] == "1"){
                window.location.href = "/nftBuy";
            }else{
                document.getElementById("buy-result").value = retruned_data.message;
            }
            
        }
    });
}