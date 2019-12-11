// Constant to improve runtime performance (prevent researching document)
var cardContainer = document.getElementById("cardsContainer")

// Hide grey highlight when tapping things on Mobile
document.addEventListener("touchstart", function(){}, true);

// Function called when user clicks a card
function bringCardToFront(element) {
    var card = element.parentNode
    // Validate user is not clicking the first card
    if (card != document.getElementsByClassName("card")[0]) {
        // Animate card down
        card.classList.remove("cardUp")
        card.classList.add("cardDown")
        // Wait for card to animate down
        setTimeout(rearrangeCards, 150)
        function rearrangeCards() {
            // Bring card to front
            cardContainer.removeChild(card)
            cardContainer.prepend(card)
            // Animate card up
            card.classList.remove("cardDown")
            card.classList.add("cardUp")
        }
    }
}
// Set Account
document.getElementById("accountImage").src = accountProfileImg
document.getElementById("accountName").innerText = accountName

// Fill in purchase total and list
var purchasesList = document.createElement("div")
var total = 0

for (i=0; i<purchases.length; i++) {
    // Card
    var tweakCard = document.createElement("div")
    tweakCard.className = "tweakCard"
    // Price
    var tweakPriceSpan = document.createElement("span")
    tweakPriceSpan.className = "tweakPrice"
    tweakPriceSpan.innerText = purchases[i].Price.toLocaleString(currencyRegion,{style:"currency",currency:currencyType})
    total += purchases[i].Price
    tweakCard.appendChild(tweakPriceSpan)
    // Tweak Icon
    var tweakImage = document.createElement("img")
    tweakImage.src = "https://cydia.saurik.com/icon@2x/com.saurik.iphone.fid.png"
    if (purchases[i].hasOwnProperty("Icon")) {
        tweakImage.src = purchases[i].Icon
    }
    tweakCard.appendChild(tweakImage)
    // Card Inner
    var tweakCardInner = document.createElement("div")
    // Tweak Name
    var tweakNameSpan = document.createElement("h1")
    tweakNameSpan.innerText = purchases[i].Name
    tweakCardInner.appendChild(tweakNameSpan)
    // Tweak Developer
    var tweakDevSpan = document.createElement("h2")
    tweakDevSpan.innerText = purchases[i].Developer
    tweakCardInner.appendChild(tweakDevSpan)
    // Add Card to Purchases List
    tweakCard.appendChild(tweakCardInner)
    purchasesList.appendChild(tweakCard)
}

// Total
var totalSpan = document.createElement("span")
totalSpan.className = "total"
// Blaze Wallet Subtraction
totalSpan.innerHTML = "Blaze Wallet: -"
if (blazeBalance < total) {
    totalSpan.innerHTML += blazeBalance.toLocaleString(currencyRegion,{style:"currency",currency:currencyType})
} else {
    totalSpan.innerHTML += total.toLocaleString(currencyRegion,{style:"currency",currency:currencyType})
}
// Final Total
totalSpan.innerHTML += "</br>Total: "
if (blazeBalance < total) {
    totalSpan.innerHTML += (total - blazeBalance).toLocaleString(currencyRegion,{style:"currency",currency:currencyType})
} else {
    totalSpan.innerHTML += (0).toLocaleString(currencyRegion,{style:"currency",currency:currencyType})
}
purchasesList.appendChild(totalSpan)

// Fill in Blaze Wallet Balance
document.getElementById("balance").innerText = blazeBalance.toLocaleString(currencyRegion,{style:"currency",currency:currencyType})
var newBlazeBalance = (blazeBalance - total)
if (newBlazeBalance > 0) {
    document.getElementById("newBalance").innerText = newBlazeBalance.toLocaleString(currencyRegion,{style:"currency",currency:currencyType})
} else {
    document.getElementById("newBalance").innerText = (0).toLocaleString(currencyRegion,{style:"currency",currency:currencyType})
}

// Add purchase list to all cards
var transactionLists = document.getElementsByClassName("transactionList")
for (i=0; i<transactionLists.length; i++) {
    transactionLists[i].innerHTML = purchasesList.innerHTML
}
var blockChain = document.getElementsByClassName("blockChain")
for (i=0; i<transactionLists.length; i++) {
    transactionLists[i].innerHTML = purchasesList.innerHTML
}
var priceTotal = total;
var total = document.getElementsByClassName("total")
for (i=0; i<total.length; i++) {
    if (total[i].parentElement.className === "transactionList blockChain") {
        total[i].innerHTML = "";
        total[i].innerHTML += "Total: -$"
        total[i].innerHTML += priceTotal
    }
}