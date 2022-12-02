  $( function() {
    var availableTags = [
        
    ];

    /*$.ajax({
        type: "GET",
        url: "qty_plus/" + orderid,
        success: function (response) {
            document.getElementById(orderid).innerHTML = response.qty;
            document.getElementById(item_tot_price).innerHTML = response.updated_price;
            document.getElementById('total').innerHTML = response.tot_amount;
            $("#minusbtn" + orderid).attr("disabled", false);
        }
    })
*/
    $( "#tags" ).autocomplete({
      source: availableTags
    });
  } );