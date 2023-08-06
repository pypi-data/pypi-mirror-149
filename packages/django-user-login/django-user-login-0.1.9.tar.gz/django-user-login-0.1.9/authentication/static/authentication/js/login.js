var prevent_default = false;

window.addEventListener('beforeunload', function (e) {
    if (prevent_default) {
        e.preventDefault();
        e.returnValue = 'Are you sure you want to cancel this process?';
    }
    return;
});


/* Register Start */
var registerModal = document.getElementById('registerModal');
var registerInput = document.getElementById('registerFormFirstName');

registerModal.addEventListener('shown.bs.modal', function () {
    clearFormInputAndErrors();
    registerInput.focus();
})

var verifyRegisterModal = document.getElementById('verifyRegisterModal');
var verificationCodeInputReg = document.getElementById('verifyRegistrationFormCode');

verifyRegisterModal.addEventListener('shown.bs.modal', function () {
    clearFormInputAndErrors();
    verificationCodeInputReg.focus();
})
  
function register(event) {
    event.preventDefault();
    let first_name = document.querySelector("#registerFormFirstName").value.replace(/^\s+|\s+$/gm,'');
    let last_name = document.querySelector("#registerFormLastName").value.replace(/^\s+|\s+$/gm,'');
    let username = document.querySelector("#registerFormUsername").value.replace(/^\s+|\s+$/gm,'');
    let email = document.querySelector("#registerFormEmail").value.replace(/^\s+|\s+$/gm,'');
    let password1 = document.querySelector("#registerFormPassword1").value.replace(/^\s+|\s+$/gm,'');
    let password2 = document.querySelector("#registerFormPassword2").value.replace(/^\s+|\s+$/gm,'');

    if (!first_name || !last_name || !username || !email || !password1 || !password2) {
        document.querySelector("#register_error").innerHTML = "Incomplete Form Data";
        registerInput.focus();
        return false;
    }

    if (password1 != password2) {
        document.querySelector("#register_error").innerHTML = "Passwords Don't Match";
        registerInput.focus();
        return false;
    }

    hide_buttons();
    prevent_default = true;

    const csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', '/authentication/register/');
    request.setRequestHeader("X-CSRFToken", csrftoken);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            show_buttons();
            clearFormInputAndErrors();
            document.querySelector("#closeRegisterFormBtn").click();
            document.querySelector("#verifyRegisterModalBtn").click();
            document.querySelector("#verifyRegistrationEmailDiv").innerHTML = res.email;
        } else {
            show_buttons();
            prevent_default = false;
            document.querySelector("#register_error").innerHTML = res.message;
            registerInput.focus();
        }
    };

    const data = new FormData();
    data.append('first_name', first_name);
    data.append('last_name', last_name);
    data.append('password2', password2);
    data.append('password1', password1);
    data.append('email', email);
    data.append('username', username);
    request.send(data);
    return false;
}


function verifyRegistration(event) {
    event.preventDefault();
    let code = document.querySelector("#verifyRegistrationFormCode").value.replace(/^\s+|\s+$/g, '');
    if (!code) {
        document.querySelector("#verifyRegistrationError").innerHTML = "Incomplete Form";
        verificationCodeInputReg.focus();
        return false;
    }

    hide_buttons();
    const csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', '/authentication/register/verify/');
    request.setRequestHeader("X-CSRFToken", csrftoken);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            prevent_default = false;
            show_buttons();
            clearFormInputAndErrors();
            document.querySelector("#closeVerifyRegFormBtn").disabled = false;
            document.querySelector("#closeVerifyRegFormBtn").click();
            document.querySelector("#regSuccessMsgBtn").click();
        } else {
            document.querySelector("#verifyRegistrationError").innerHTML = res.message;
            show_buttons();
            verificationCodeInputReg.focus();
        }
    };

    const data = new FormData();
    data.append('code', code);
    request.send(data);
    return false;
}


function cancelVerifyRegistration() {
    const request = new XMLHttpRequest();
    request.open('GET', '/authentication/register/cancel/');
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            prevent_default = false;
            show_buttons();
            clearFormInputAndErrors();
        }
    };
    request.send();
    return false;
}


function resendVerificationCodeReg(event) {
    event.preventDefault();
    hide_buttons();
    clearFormInputAndErrors();

    const request = new XMLHttpRequest();
    request.open('GET', '/authentication/register/resend/');
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            show_buttons();
            if (document.querySelector("#verifyRegistrationError")) {
                document.querySelector("#verifyRegistrationError").innerHTML = "A new verification code was sent to your email address.";
            }
            verificationCodeInputReg.focus();
        } else {
            prevent_default = false;
            show_buttons();
            if (document.querySelector("#verifyRegistrationError")) {
                document.querySelector("#verifyRegistrationError").innerHTML = res.message;
            }
            verificationCodeInputReg.focus();
        }
    };
    request.send();
    return false;
}
/* Register End */


/* Recover Account Start */
var recoverModal = document.getElementById('recoverModal');
var recoverInput = document.getElementById('modalRecoverFormUsername');

recoverModal.addEventListener('shown.bs.modal', function () {
    clearFormInputAndErrors();
    recoverInput.focus();
})

var verifyRecoverModal = document.getElementById('verifyRecoveryModal');
var verifyRecoverInput = document.getElementById('verifyRecoveryFormCode');

verifyRecoverModal.addEventListener('shown.bs.modal', function () {
    clearFormInputAndErrors();
    verifyRecoverInput.focus();
})

var pswdChngModal = document.getElementById('pswdChngFormModal');
var pswdChngInput = document.getElementById('pswdChngFormInput1');

pswdChngModal.addEventListener('shown.bs.modal', function () {
    clearFormInputAndErrors();
    pswdChngInput.focus();
})


function recover(event) {
    event.preventDefault();
    let username = document.querySelector("#modalRecoverFormUsername").value.replace(/^\s+|\s+$/g, '');
    if (!username) {
        document.querySelector("#pswdRecovery_error").innerHTML = "Incomplete Form";
        recoverInput.focus();
        return false;
    }

    hide_buttons();
    prevent_default = true;

    const csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', '/authentication/recover/');
    request.setRequestHeader("X-CSRFToken", csrftoken);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            show_buttons();
            clearFormInputAndErrors();
            document.querySelector("#closeRecoveryFormBtn").click();
            document.querySelector("#verifyRecoveryFormModalBtn").click();
            document.querySelector("#verifyRecoveryEmailDiv").innerHTML = res.email;
        } else {
            show_buttons();
            prevent_default = false;
            recoverInput.focus();
            document.querySelector("#pswdRecovery_error").innerHTML = res.message;
        }
    };

    const data = new FormData();
    data.append('username', username);
    request.send(data);
    return false;
}


function verifyRecovery(event) {
    event.preventDefault();
    let code = document.querySelector("#verifyRecoveryFormCode").value.replace(/^\s+|\s+$/g, '');
    if (!code) {
        document.querySelector("#verifyRecoveryError").innerHTML = "Incomplete Form";
        verifyRecoverInput.focus();
        return false;
    }

    hide_buttons();
    const csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', '/authentication/recover/verify/');
    request.setRequestHeader("X-CSRFToken", csrftoken);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            clearFormInputAndErrors();
            show_buttons();
            document.querySelector("#closeVerifyRecoveryFormBtn").disabled = false;
            document.querySelector("#closeVerifyRecoveryFormBtn").click();
            document.querySelector("#pswdChngFormModalBtn").click();
            document.querySelector("#pswdChngFormInput3").value = res.username;
        } else {
            show_buttons();
            document.querySelector("#verifyRecoveryError").innerHTML = res.message;
            verifyRecoverInput.focus();
        }
    };

    const data = new FormData();
    data.append('code', code);
    request.send(data);
    return false;
}


function change_password(event) {
    event.preventDefault();
    let password1 = document.querySelector("#pswdChngFormInput1").value.replace(/^\s+|\s+$/g, '');
    let password2 = document.querySelector("#pswdChngFormInput2").value.replace(/^\s+|\s+$/g, '');

    if (!password1 || !password2) {
        document.querySelector("#pswdChng_error").innerHTML = "Incomplete Form";
        pswdChngInput.focus();
        return false;
    }
    if (password1 != password2) {
        document.querySelector("#pswdChng_error").innerHTML = "Passwords Don't Match";
        pswdChngInput.focus();
        return false;
    }

    hide_buttons();
    const csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', '/authentication/recover/changepassword/');
    request.setRequestHeader("X-CSRFToken", csrftoken);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            clearFormInputAndErrors();
            prevent_default = false;
            show_buttons();
            document.querySelector("#closePswdChngFrmBtn").disabled = false;
            document.querySelector("#closePswdChngFrmBtn").click();
            document.querySelector("#pswdChngSuccessMsgBtn").click();
        } else {
            show_buttons();
            pswdChngInput.focus();
            document.querySelector("#pswdChng_error").innerHTML = res.message;
        }
    };

    const data = new FormData();
    data.append('password1', password1);
    data.append('password2', password2);
    request.send(data);
    return false;
}



function cancelVerifyRecovery() {
    const request = new XMLHttpRequest();
    request.open('GET', '/authentication/recover/cancel/');
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            prevent_default = false;
            show_buttons();
            clearFormInputAndErrors();
        }
    };
    request.send();
    return false;
}


function resendVerificationCodeRecovery(event) {
    event.preventDefault();
    hide_buttons();
    clearFormInputAndErrors();

    const request = new XMLHttpRequest();
    request.open('GET', '/authentication/recover/resend/');
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            show_buttons();
            if (document.querySelector("#verifyRecoveryError")) {
                document.querySelector("#verifyRecoveryError").innerHTML = "A new verification code was sent to your email address.";
            }
            verifyRecoverInput.focus();
        } else {
            prevent_default = false;
            show_buttons();
            if (document.querySelector("#verifyRecoveryError")) {
                document.querySelector("#verifyRecoveryError").innerHTML = res.message;
            }
            verifyRecoverInput.focus();
        }
    };
    request.send();
    return false;
}
/* Recover Account End */


/* Login JS */
var LoginModal = document.getElementById('loginModal');
var LoginInput = document.getElementById('modalLoginFormUsername');

LoginModal.addEventListener('shown.bs.modal', function () {
    clearFormInputAndErrors();
    LoginInput.focus();
})


function login(event) {
    event.preventDefault();
    let username = document.querySelector("#modalLoginFormUsername").value.replace(/^\s+|\s+$/g, '');
    let password = document.querySelector("#modalLoginFormPassword").value.replace(/^\s+|\s+$/g, '');

    if (!username || !password) {
        document.querySelector("#login_error").innerHTML = "Incomplete Form";
        LoginInput.focus();
        return false;
    }

    hide_buttons();
    prevent_default = true;

    const csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', '/authentication/login/');
    request.setRequestHeader("X-CSRFToken", csrftoken);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            prevent_default = false;
            location.reload();
        } else {
            show_buttons();
            LoginInput.focus();
            prevent_default = false;
            document.querySelector("#login_error").innerHTML = res.message;
        }
    };

    const data = new FormData();
    data.append('username', username);
    data.append('password', password);
    request.send(data);
    return false;
}
/* Login JS End */


/* Logout JS */
function logout(event) {
    event.preventDefault();
    const request = new XMLHttpRequest();
    request.open('GET', '/authentication/logoutJS/');
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            prevent_default = false;
            location.reload();
        }
    };
    request.send();
    return false;
}
/* Logout JS End */


/* Common Functions */
function hide_buttons() {
    document.querySelectorAll(".auth-btn").forEach(b => {
        b.disabled = true;
    });

    document.querySelectorAll(".auth-spinner").forEach(s => {
        s.hidden = false;
    });

    document.querySelectorAll(".auth-link").forEach(l => {
        l.style.pointerEvents = "none";
        l.style.cursor = "default";
    });
}


function show_buttons() {
    document.querySelectorAll(".auth-btn").forEach(b => {
        b.disabled = false;
    });

    document.querySelectorAll(".auth-spinner").forEach(b => {
        b.hidden = true;
    });

    document.querySelectorAll(".auth-link").forEach(l => {
        l.style.pointerEvents = "auto";
        l.style.cursor = "pointer";
    });
}


function clearFormInputAndErrors() {
    document.querySelectorAll(".form-control").forEach(i => {
        i.value = '';
    })

    document.querySelectorAll(".errormessage").forEach(i => {
        i.innerHTML = '<br>';
    })
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}