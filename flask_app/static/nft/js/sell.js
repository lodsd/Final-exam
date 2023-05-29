function createNFT(){
    var data_d = {
        'description': document.getElementById('nft-description').value,
        'token': document.getElementById('nft-token').value,
    }
    jQuery.ajax({
        url: "/createNFT",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
            window.location.href = "/nftSell";
        }
    });
}

function uploadNFT() { 
    var formData = new FormData();
    formData.append('image', document.getElementById('nft-image').files[0]);
    formData.append('description', document.getElementById('nft-description').value);
    formData.append('token', document.getElementById('nft-token').value);

    jQuery.ajax({
        url: "/uploadNFT",
        data: formData,
        type: "POST",
        processData: false,
        contentType: false,
        success:function(retruned_data){
            window.location.href = "/nftSell";
        }
    });
 }

function updateNFT(id){
    var data_d = {
        'id' : id,
        'description': document.getElementById('card-description-'+id).value,
        'token': document.getElementById('card-token-'+id).value,
    }
    console.log(data_d);
    jQuery.ajax({
        url: "/updateNFT",
        data: data_d,
        type: "POST",
        success:function(retruned_data){
            window.location.href = "/nftSell";
        }
    });
}