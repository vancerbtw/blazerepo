var username = name;
var profilePictureURL = avatar;

//Function to return nicely formatted date
function returnDate() {
    let months = ["Janurary", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    let date = new Date()
    return date.getDate().toString() + " " + months[date.getMonth()] + " " + date.getFullYear()
}

//Set Values
document.getElementById("date").innerText = returnDate()
document.getElementById("balance").innerText = "$" + balance
document.getElementById("profilePicture").style.backgroundImage = "url(" + profilePictureURL + ")"
document.getElementById("username").innerText = username
document.getElementById("email").innerText = email
document.getElementById("userId").innerText = "Blaze ID: " + userId

for (i=0; i<linkedAccounts.length; i++) {
    var element = document.getElementById(linkedAccounts[i].type)
    if (linkedAccounts[i].type === "blaze") {
        element.setAttribute("onclick","");
    } else {
        element.innerHTML = linkedAccounts[i].account + '<div class="accountsAddIcon"></div>';
        element.setAttribute("onclick","unlinkAccount(this)");
        element.classList.add("linkedAccount");
    }
    element.classList.remove("unlinkedAccount");

}

// ========================
// Placeholder Functions
// ========================

//Signout Function
function signout() {
    location.href = '/logout'
}

//Unlick Account Function
function unlinkAccount(element) {
    location.href = '/unlink/' + element.id
}

//Link Account Function
function linkAccount(element) {
    location.href = '/auth/link/' + element.id
}

function linkBlaze(element) {
    location.href = '/blazeLink';
}

//Add Funds Function
function addFunds() {
    location.href = '/addFunds'
}

function goToDetails() {
    location.href = '/accountDetails'
}