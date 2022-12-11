var nameError = document.getElementById('name-error');
var emailError = document.getElementById('email-error');
var subjectError = document.getElementById('subject-error');
var telError = document.getElementById('tel-error');
var messageError = document.getElementById('message-error');
var submitError = document.getElementById('submit-error');

var name,email,message,Tel,subject;
function validateName() {
    var name=document.getElementById('name').value.trim();  

    if (name.length==0 || name.length<3) {
        nameError.innerHTML='Enter min 3 characters';
        nameError.style.color='black'
        return false;
    }

    if (!name.match(/^[A-Za-z ]*$/)){
        nameError.innerHTML='Write a FullName';
        nameError.style.color='black'
        return false;
    }
    
    nameError.innerHTML='Name is valid';
    nameError.style.color='white'
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
    emailError.innerHTML='Email is valid';
    emailError.style.color='white'
    return true;
}

function validateMsg() {
    var message =document.getElementById('message').value.trim();
    
    if(message.length==0 || message.length<10){
        messageError.innerHTML ='More character Required';
        messageError.style.color='black'
        return false;
    }
    messageError.innerHTML='Message is valid';
    messageError.style.color='white'
    return true;   
}
function validateTel() {
    var Tel =document.getElementById('telephone').value.trim();
    
        if(Tel.match(/^[0-9]+$/) && Tel.length>10 && Tel.length<12)
        {
            telError.innerHTML='Message is valid';
            telError.style.color='white'
            return true;
        }

        else{
            telError.innerHTML ='Mobile Number is Required';
            telError.style.color='black'
            return false;
        }
    }
    function validateSubject() {
        var subject=document.getElementById('subject').value.trim();  

        if (subject.length==0) {
            subjectError.innerHTML='This field is Required';
            subjectError.style.color='black'
            return false;
        }
    
        if (!subject.match(/^[A-Za-z ]*$/)){
            subjectError.innerHTML='Enter valid subject';
            subjectError.style.color='black'
            return false;
        }
        
        subjectError.innerHTML='Subject is valid';
        subjectError.style.color='white'
        return true;
    }

    $('#contactForm').submit(function(e){
        e.preventDefault();                             //This is used to prevent window from submitting the form
        validateName()
        validateEmail()
        validateMsg()
        validateTel()
        validateSubject()
        if ( validateName() && validateEmail() && validateMsg() && validateTel() && validateSubject()) {
          //$(this).unbind('submit').submit()             //This is used to undo preventDefault
          $.ajax({
            url:"https://script.google.com/macros/s/AKfycbxMmJ0V3ruUw2-1MyT5GHGMxRP3PWpoNG88zeJqgACrktr0y0umh7ou3PJIET1sS_gsYg/exec",
            data:$("#contactForm").serialize(),
            method:"post",
            success:function (response){
                //alert("Form submitted successfully")
                swal.fire({
                title:'Form submitted successfully',
                timer: 2000,
                icon: 'success',
                confirmButtonColor: 'rgb(46, 44, 44)',
                }).then(function () {
                    window.location.href = "/";
                  });
            },
            error:function (err){
                alert("Something Error")
            }
        })

        } else {
        e.preventDefault();
        swal.fire({text :'Ensure You have entered correct data',
        icon: 'error',
        confirmButtonColor: 'rgb(46, 44, 44)',
        });
        }
    });