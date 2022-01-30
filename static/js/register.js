var email = document.getElementById("email");
var username = document.getElementById("username");
var passwordOne = document.getElementById("password1");
var passwordTwo = document.getElementById("password2");
var handleEmail = document.getElementById("handleemail");
var handleUsername = document.getElementById("handleusername");
var handleShortPassword = document.getElementById("handleshortpassword");
var handlePassNoMatch = document.getElementById("handlepassnonmatch");
var allUsernames = [];

for (let i = 0; i < all_users.length; i++) {

    allUsernames.push(all_users[i].username);

}

console.log(allUsernames);

function testEmail(email) {

    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);

}

function validateRegistration(e) {

    console.log(testEmail(email.value));
    var correctEmail = testEmail(email.value);
    var correctUsername = username.value != "";
    var correctUniqueUsername = !allUsernames.includes(username.value);
    var correctPasswordsLengths = password1.value.length > 7;
    var correctPasswordsMatching = password1.value == password2.value;

    var registrationSuccessful = correctEmail && correctUsername && correctPasswordsLengths && correctPasswordsMatching;
    if (registrationSuccessful) return true;
    else {

    {if (!correctEmail) handleEmail.style.display = "block"; else handleEmail.style.display = "none";
    if (!correctUsername) { handleUsername.style.display = "block"; handleUsername.innerText = "Username must exist"; } else {handleUsername.style.display = "none"; handleUsername.innerText = "Username already exists"; }
    if (!correctPasswordsLengths) handleShortPassword.style.display = "block"; else handleShortPassword.style.display = "none";
    if (!correctPasswordsMatching) handlePassNoMatch.style.display = "block"; else handlePassNoMatch.style.display = "none";
    }
    return false;
    }

}