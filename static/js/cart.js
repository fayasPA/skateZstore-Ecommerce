function minus(orderid, qty, item_tot_price) {
    console.log("FAY")
    $.ajax({
        type: "GET",
        url: "qty_minus/" + orderid,
        success: function (response) {
            if (response.qty == 1) {
                $("#minusbtn" + orderid).attr("disabled", true);
                document.getElementById(orderid).innerHTML = response.qty;
                document.getElementById(item_tot_price).innerHTML = response.updated_price;
                document.getElementById('total').innerHTML = response.tot_amount;
            }
            else {
                document.getElementById(orderid).innerHTML = response.qty;
                document.getElementById(item_tot_price).innerHTML = response.updated_price;
                document.getElementById('total').innerHTML = response.tot_amount;
            }
        }
    });
}

function plus(orderid, qty, item_tot_price) {
    console.log("plus", orderid, qty)
    $.ajax({
        type: "GET",
        url: "qty_plus/" + orderid,
        success: function (response) {
            document.getElementById(orderid).innerHTML = response.qty;
            document.getElementById(item_tot_price).innerHTML = response.updated_price;
            document.getElementById('total').innerHTML = response.tot_amount;
            $("#minusbtn" + orderid).attr("disabled", false);
        }
    })
}