var prod_nameError = document.getElementById('prod_name-error');
var prod_priceError = document.getElementById('prod_price-error');
var prod_descError = document.getElementById('prod_desc-error');
// var prod_qtyError = document.getElementById('prod_qty-error');
// var messageError = document.getElementById('message-error');
// var submitError = document.getElementById('submit-error');

var prod_name,prod_price,prod_qty,prod_desc,categ_name;
function validateProdname() {
    var prod_name=document.getElementById('prod_name').value.trim();  

    if (prod_name.length==0 || prod_name.length<3) {
        prod_nameError.innerHTML='Enter min 3 characters';
        prod_nameError.style.color='red'
        return false;
    }

    if (!prod_name.match(/^[A-Za-z 0-9]*$/)){
        prod_nameError.innerHTML='Name is incorrect';
        prod_nameError.style.color='red'
        return false;
    }
    
    prod_nameError.innerHTML='Name is valid';
    prod_nameError.style.color='green'
    return true;
}

function validateProdprice() {
    var prod_price =document.getElementById('prod_price').value.trim();
    
        if(prod_price.match(/^[0-9.]+$/))
        {
            prod_priceError.innerHTML='Message is valid';
            prod_priceError.style.color='green'
            return true;
        }

        else{
            prod_priceError.innerHTML ='Enter the Price of Item';
            prod_priceError.style.color='red'
            return false;
        }
    }

function validateDesc() {
    var prod_desc =document.getElementById('prod_desc').value.trim();
    
    if(prod_desc.length==0 || prod_desc.length<10){
        prod_descError.innerHTML ='More Characters are Required';
        prod_descError.style.color='red'
        return false;
    }
    prod_descError.innerHTML='Message is valid';
    prod_descError.style.color='green'
    return true;
}








// function validat_eProdprice(){
//     var email = document.getElementById('email').value.trim();
//     if (email.length==0 && Tel.length>10 && Tel.length<12) {
//         emailError.innerHTML='Email is Required';
//         emailError.style.color='red'
//         return false;
//     }

//     if (!email.match(/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)) {
//         emailError.innerHTML='Email is Invalid';
//         emailError.style.color='red'
//         return false;
//     }
//     emailError.innerHTML='Email is valid';
//     emailError.style.color='green'
//     return true;
// }




    // function validateSubject() {
    //     var subject=document.getElementById('subject').value.trim();  

    //     if (subject.length==0) {
    //         subjectError.innerHTML='This field is Required';
    //         subjectError.style.color='red'
    //         return false;
    //     }
    
    //     if (!subject.match(/^[A-Za-z ]*$/)){
    //         subjectError.innerHTML='Enter valid subject';
    //         subjectError.style.color='red'
    //         return false;
    //     }
        
    //     subjectError.innerHTML='Subject is valid';
    //     subjectError.style.color='green'
    //     return true;
    // }