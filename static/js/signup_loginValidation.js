// Login Form Starts
var usernameError = document.getElementById('username-error');
var passwordError = document.getElementById('password-error');
function validateUser(){
        var username=document.getElementById('username').value.trim();  
    
        if (username.length==0) {
            usernameError.innerHTML='Pls Enter Your Username';
            usernameError.style.color='black'
            return false;
        }
        usernameError.innerHTML='';
        usernameError.style.color='white'
        return true;
    }
function validatePassword(){
        var password=document.getElementById('password').value.trim();  
        if (password.length==0) {
            passwordError.innerHTML='Pls Enter Your Password';
            passwordError.style.color='black'
            return false;
        }
        passwordError.innerHTML='';
        passwordError.style.color='white'
        return true;       
}

$('#loginForm').submit(function(e){
    e.preventDefault();                             //This is used to prevent window from submitting the form
    if ( validateUser() && validatePassword()) {
      $(this).unbind().submit()             //This is used to undo preventDefault
    } 
    else {
    e.preventDefault();
    swal.fire({text :'Please enter your Username and Password',
    icon: 'error',
    confirmButtonColor: 'rgb(46, 44, 44)',
    });
    }
});
// Login Form Ends

// Sign Up Form Starts
var usernameError = document.getElementById('username-error');
var first_nameError = document.getElementById('first_name-error');
var emailError = document.getElementById('email-error');
var phone_numberError = document.getElementById('phone_number-error');
var password1Error = document.getElementById('password1-error');
var password2Error = document.getElementById('password2-error');

var name,email,message,Tel,subject;

function validateUname() {
    var username =document.getElementById('username').value.trim();
    if(username.length==0){
        usernameError.innerHTML ='Username is required';
        usernameError.style.color='black'
        return false;
    }
    if(username.length<4){
        usernameError.innerHTML ='Enter atleast 3 characters';
        usernameError.style.color='black'
        return false;
    }
    usernameError.innerHTML='';
    usernameError.style.color='white'
    return true;   
}

function validateFname() {
    var first_name=document.getElementById('first_name').value.trim();  
    if (first_name.length==0 || first_name.length<3) {
        first_nameError.innerHTML='Name is Required';
        first_nameError.style.color='black'
        return false;
    }

    if (!first_name.match(/^[A-Za-z ]*$/)){
        first_nameError.innerHTML='Only Letters Are To Be Entered';
        first_nameError.style.color='black'
        return false;
    }
    
    first_nameError.innerHTML='';
    first_nameError.style.color='white'
    return true;
}


function validateEmail(){
    var email = document.getElementById('email').value.trim();
    if (email.length==0) {
        emailError.innerHTML='Email is Required';
        emailError.style.color='black'
        return false;
    }

    if (!email.match(/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)) {
        emailError.innerHTML='Email is Invalid';
        emailError.style.color='black'
        return false;
    }
    emailError.innerHTML='';
    emailError.style.color='white'
    return true;
}


function validateTel() {
    var phone_number =document.getElementById('phone_number').value.trim();
    
        if(phone_number.match(/^[0-9]+$/) && phone_number.length>9 && phone_number.length<12)
        {
            phone_numberError.innerHTML='';
            phone_numberError.style.color='white'
            return true;
        }

        else{
            phone_numberError.innerHTML ='Mobile Number is Required';
            phone_numberError.style.color='black'
            return false;
        }
    }
    function validatePswd() {
        var password1=document.getElementById('password1').value.trim();  

        if (password1.length==0) {
            password1Error.innerHTML='Paswword is Required';
            password1Error.style.color='black'
            return false;
        }
        password1Error.innerHTML='';
        password1Error.style.color='white'
        return true;
    }
    function validateRePswd() {
        var password2=document.getElementById('password2').value.trim();  
        var password1=document.getElementById('password1').value.trim();  

        if (password2.length==0) {
            password2Error.innerHTML='Re-Enter Password';
            password2Error.style.color='black'
            return false;
        }
        
        if (password2 != password1){
            password2Error.innerHTML='Please Enter the same password';
            password2Error.style.color='black'
            return false;
        }
        
        password2Error.innerHTML='';
        password2Error.style.color='white'
        return true;
    }

    $('#signupForm').submit(function(e){
        e.preventDefault();                             //This is used to prevent window from submitting the form
        if ( validateUname() && validateFname() && validateEmail() && validateTel() && validatePswd() && validateRePswd()) {
          $(this).unbind().submit()             //This is used to undo preventDefault
        } 
        else {
        e.preventDefault();
        swal.fire({text :'Ensure You have entered All Data',
        icon: 'error',
        confirmButtonColor: 'rgb(46, 44, 44)',
        });
        }
    });
// Sign Up Form Ends
