var prevent_default = false;

window.addEventListener('beforeunload', function (e) {
    if (prevent_default) {
        e.preventDefault();
        e.returnValue = 'Are you sure you want to cancel this process?';
    }
    return;
});


/* edit email start */

// Function to check password confirmation
function editProfileEmail(event, username) {
    event.preventDefault();
    const request = new XMLHttpRequest();
    request.open('GET', `/authentication/${username}/details/edit/check`);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        show_buttons();
        if (res.success) {
            if (res.status) {
                /* show email change div/modal */
                displayChangeEmailModal(res.username, res.email);
            } else {
                /* show confirm password div/modal */
                const details_template = Handlebars.compile(document.querySelector('#confirmPasswordFormHandlebars').innerHTML);
                const details = details_template({"username": res.username});
                document.querySelector("#confirmPasswordForm-modalBody").innerHTML = details;
                document.querySelector("#confirmPasswordModalBtn").click();

                var ConfirmPasswordModal = document.getElementById('confirmPasswordModal');
                var ConfirmPasswordInput = document.getElementById('inputPassword');

                ConfirmPasswordModal.addEventListener('shown.bs.modal', function () {
                    ConfirmPasswordInput.focus();
                })
            }
        }
    };
    
    request.send();
    return false;
}


// function to check password
function confirmPassword(event, username) {
    event.preventDefault();
    var ConfirmPasswordModal = document.getElementById('confirmPasswordModal');
    var ConfirmPasswordInput = document.getElementById('inputPassword');

    ConfirmPasswordModal.addEventListener('shown.bs.modal', function () {
        ConfirmPasswordInput.focus();
    })

    let password = document.querySelector("#inputPassword").value.replace(/^\s+|\s+$/g, '');
    if (!password) {
        document.querySelector("#confirm_password_error").innerHTML = "Incomplete Form";
        ConfirmPasswordInput.focus();
        return false;
    }

    hide_buttons();
    prevent_default = true;

    const csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', `/authentication/${username}/details/edit/check/confirm/`);
    request.setRequestHeader("X-CSRFToken", csrftoken);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            show_buttons();
            prevent_default = false;
            document.querySelector("#confirmPasswordModalBtnClose").click();
            displayChangeEmailModal(res.username, res.email);
        } else {
            show_buttons();
            prevent_default = false;
            document.querySelector("#confirm_password_error").innerHTML = res.message;
            ConfirmPasswordInput.focus();
        }
    };

    const data = new FormData();
    data.append('password', password);
    request.send(data);
    return false;
}


// displayChangeEmailModal
function displayChangeEmailModal(username, email) {
    const details_template = Handlebars.compile(document.querySelector('#changeEmailFormHandlebars').innerHTML);
    const details = details_template({"username": username, "email": email});
    document.querySelector("#changeEmailFormDiv").innerHTML = details;
    document.querySelector("#changeEmailFormModalBtn").click();

    var myModal = document.getElementById('changeEmailFormModal');
    var myInput = document.getElementById('inputEmail_new');

    myModal.addEventListener('shown.bs.modal', function () {
        myInput.focus();
    })
}


function changeEmail(event, username) {
    event.preventDefault();
    var myModal = document.getElementById('changeEmailFormModal');
    var myInput = document.getElementById('inputEmail_new');

    myModal.addEventListener('shown.bs.modal', function () {
        myInput.focus();
    })
    
    let email = document.querySelector("#inputEmail_new").value.replace(/^\s+|\s+$/g, '');
    if (!email) {
        document.querySelector("#change_email_error").innerHTML = "Incomplete Form";
        myInput.focus();
        return false;
    }
    hide_buttons();
    prevent_default = true;

    const csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', `/authentication/${username}/details/edit/check/email/`);
    request.setRequestHeader("X-CSRFToken", csrftoken);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            show_buttons();
            document.querySelector("#changeEmailModalBtnClose").click();

            const details_template = Handlebars.compile(document.querySelector('#verifyChangeEmailFormHandlebars').innerHTML);
            const details = details_template({"username": res.username, "new_email": res.new_email});
            document.querySelector("#verifyChangeEmailFormDiv").innerHTML = details;
            document.querySelector("#verifyRecoveryFormModalBtn").click();

            var myModal = document.getElementById('verifyRecoveryModal');
            var myInput = document.getElementById('verifyRecoveryFormCode');

            myModal.addEventListener('shown.bs.modal', function () {
                myInput.focus();
            })
        } else {
            show_buttons();
            prevent_default = false;
            document.querySelector("#change_email_error").innerHTML = res.message;
        }
    };

    const data = new FormData();
    data.append('email', email);
    request.send(data);
    return false;
}


function cancelVerifyRecovery(username) {
    const request = new XMLHttpRequest();
    request.open('GET', `/authentication/${username}/details/edit/check/email/cancel/`);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        show_buttons();
        if (res.success) {
            cancelprocesses();
        }
    };
    request.send();
    return false;
}



function resendVerificationCodeRecovery(event, username) {
    event.preventDefault();
    var myModal = document.getElementById('verifyRecoveryModal');
    var myInput = document.getElementById('verifyRecoveryFormCode');

    myModal.addEventListener('shown.bs.modal', function () {
        myInput.focus();
    })

    hide_buttons();
    const request = new XMLHttpRequest();
    request.open('GET', `/authentication/${username}/details/edit/check/email/resend/`);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        show_buttons();
        if (res.success) {
            document.querySelector("#verifyRecoveryError").innerHTML = "A new verification code was sent to your email account.";
            myInput.focus();
        } else {
            if (document.querySelector("#verifyRecoveryError")) {
                document.querySelector("#verifyRecoveryError").innerHTML = res.message;
                myInput.focus();
            }
        }
    };
    request.send();
    return false;
}



function verifyRecovery(event, username) {
    event.preventDefault();
    var myModal = document.getElementById('verifyRecoveryModal');
    var myInput = document.getElementById('verifyRecoveryFormCode');

    myModal.addEventListener('shown.bs.modal', function () {
        myInput.focus();
    })

    let code = document.querySelector("#verifyRecoveryFormCode").value.replace(/^\s+|\s+$/g, '');
    if (!code) {
        document.querySelector("#verifyRecoveryError").innerHTML = "Incomplete Form";
        myInput.focus();
        return false;
    }
    hide_buttons();

    const csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', `/authentication/${username}/details/edit/check/email/change/`);
    request.setRequestHeader("X-CSRFToken", csrftoken);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            show_buttons();
            prevent_default = false;
            document.querySelector("#closeVerifyRecoveryFormBtn").disabled = false;
            document.querySelector("#closeVerifyRecoveryFormBtn").click();
            get_person();
        } else {
            show_buttons();
            document.querySelector("#verifyRecoveryError").innerHTML = res.message;
            myInput.focus();
        }
    };

    const data = new FormData();
    data.append('code', code);
    request.send(data);
    return false;
}
/* edit email end */


function changepassword(event, username) {
    event.preventDefault();
    
    var myModal = document.getElementById('changePasswordModal');
    var myInput = document.getElementById('currentpassword');

    myModal.addEventListener('shown.bs.modal', function () {
        myInput.focus();
    })

    let form_username = document.querySelector("#username_change_password").value.replace(/^\s+|\s+$/g, '');
    let current_password = document.querySelector("#currentpassword").value.replace(/^\s+|\s+$/g, '');
    let new_password1 = document.querySelector("#newpassword1").value.replace(/^\s+|\s+$/g, '');
    let new_password2 = document.querySelector("#newpassword2").value.replace(/^\s+|\s+$/g, '');

    if (!form_username || !current_password || !new_password1 || !new_password2 || form_username != username) {
        document.querySelector("#change_password_error").innerHTML = "Incomplete Form";
        myInput.focus();
        return false;
    }

    if (new_password1 != new_password2) {
        document.querySelector("#change_password_error").innerHTML = "Passwords Don't Match";
        myInput.focus();
        return false;
    }

    hide_buttons();
    prevent_default = true;

    const csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', `/authentication/${username}/details/edit/change/password/`);
    request.setRequestHeader("X-CSRFToken", csrftoken);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            show_buttons();
            prevent_default = false;
            document.querySelector("#changePasswordModalBtnClose").click();
            document.querySelector("#pswdChngSuccessMsgBtn").click();
        } else {
            show_buttons();
            prevent_default = false;
            document.querySelector("#change_password_error").innerHTML = res.message;
            myInput.focus();
        }
    };

    const data = new FormData();
    data.append('form_username', form_username);
    data.append('current_password', current_password);
    data.append('new_password1', new_password1);
    data.append('new_password2', new_password2);
    request.send(data);
    return false;
}


/* edit profile start */
function editprofile(event, username) {
    event.preventDefault();
    const request = new XMLHttpRequest();
    request.open('GET', `/authentication/${username}/details/`);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            const details_template = Handlebars.compile(document.querySelector('#EditProfileFormHandlebars').innerHTML);
            const details = details_template(res.person);
            document.querySelector("#editProfileForm-modalBody").innerHTML = details;
            document.querySelector("#editProfileModalBtn").click();

            var EditProfileModal = document.getElementById('editProfileModal');
            var EditProfileInput = document.getElementById('inputFirstName');

            EditProfileModal.addEventListener('shown.bs.modal', function () {
                EditProfileInput.focus();
            })
        }
    };
    request.send();
    return false;
}


function edit_profile(event, username) {
    event.preventDefault();
    let first_name = document.querySelector("#inputFirstName").value.replace(/^\s+|\s+$/g, '');
    let last_name = document.querySelector("#inputLastName").value.replace(/^\s+|\s+$/g, '');
    let username_new = document.querySelector("#inputUsername").value.replace(/^\s+|\s+$/g, '');
    let email = document.querySelector("#inputEmail").value.replace(/^\s+|\s+$/g, '');

    if (!first_name || !last_name || !username_new || !email) {
        document.querySelector("#edit_profile_error").innerHTML = "Incomplete Form";
        return false;
    }

    var EditProfileModal = document.getElementById('editProfileModal');
    var EditProfileInput = document.getElementById('inputFirstName');

    EditProfileModal.addEventListener('shown.bs.modal', function () {
        EditProfileInput.focus();
    })

    hide_buttons();
    prevent_default = true;

    const csrftoken = getCookie('csrftoken');
    const request = new XMLHttpRequest();
    request.open('POST', `/authentication/${username}/details/edit/`);
    request.setRequestHeader("X-CSRFToken", csrftoken);
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            show_buttons();
            prevent_default = false;
            document.querySelector("#editProfileModalBtnClose").click();
            get_person();
        } else {
            show_buttons();
            prevent_default = false;
            document.querySelector("#edit_profile_error").innerHTML = res.message;
            EditProfileInput.focus();
        }
    };

    const data = new FormData();
    data.append('first_name', first_name);
    data.append('last_name', last_name);
    data.append('username_new', username_new);
    data.append('email', email);
    request.send(data);
    return false;
}
/* edit profile end */


/* common code start */
document.addEventListener("DOMContentLoaded", ()=>{
    get_person();
    var myModal = document.getElementById('changePasswordModal');
    var myInput = document.getElementById('currentpassword');

    myModal.addEventListener('shown.bs.modal', function () {
        myInput.focus();
    })
});


function get_person() {
    const request = new XMLHttpRequest();
    request.open('GET', '/authentication/username/details/');
    
    request.onload = () => {
        const res = JSON.parse(request.responseText);
        if (res.success) {
            const details_template = Handlebars.compile(document.querySelector('#PersonDetailsHandlebars').innerHTML);
            const details = details_template(res.person);
            document.querySelector("#personDetailsDiv").innerHTML = details;
        }
    };
    request.send();
    return false;
}


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



function cancelprocesses() {
    clearFormInputAndErrors();
    show_buttons();
    prevent_default = false;
}