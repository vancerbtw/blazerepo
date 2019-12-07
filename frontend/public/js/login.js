const sidebar = document.getElementsByClassName("sidebar")[0]
const main = document.getElementsByClassName("centerCardContent")[0]
const signUp = document.getElementById("signUp")
const signIn = document.getElementById("signIn")
const signUpWelcome = document.getElementById("signUpWelcomeMessage")
const signInWelcome = document.getElementById("signInWelcomeMessage")

function expandSignUp() {
    sidebar.style.width = "65%"
    main.style.width = "35%"
    main.style.left = "65%"
    signUp.style.display = "inline-block"
    signUpWelcome.style.display = "none"
    signIn.style.display = "none"
    signInWelcome.style.display = "inline-block"
}

function expandSignIn() {
    sidebar.style.width = "35%"
    main.style.width = "65%"
    main.style.left = "35%"
    signUp.style.display = "none"
    signUpWelcome.style.display = "inline-block"
    signIn.style.display = "inline-block"
    signInWelcome.style.display = "none"
}

function fadeIn(elem, ms) {
  if( ! elem )
    return;

  elem.style.opacity = 0;
  elem.style.filter = "alpha(opacity=0)";
  elem.style.display = "inline-block";
  elem.style.visibility = "visible";

  if( ms )
  {
    var opacity = 0;
    var timer = setInterval( function() {
      opacity += 50 / ms;
      if( opacity >= 1 )
      {
        clearInterval(timer);
        opacity = 1;
      }
      elem.style.opacity = opacity;
      elem.style.filter = "alpha(opacity=" + opacity * 100 + ")";
    }, 50 );
  }
  else
  {
    elem.style.opacity = 1;
    elem.style.filter = "alpha(opacity=1)";
  }
}

function fadeOut(elem, ms) {
  if( ! elem )
    return;

  if( ms )
  {
    var opacity = 1;
    var timer = setInterval( function() {
      opacity -= 50 / ms;
      if( opacity <= 0 )
      {
        clearInterval(timer);
        opacity = 0;
        elem.style.display = "none";
        elem.style.visibility = "hidden";
      }
      elem.style.opacity = opacity;
      elem.style.filter = "alpha(opacity=" + opacity * 100 + ")";
    }, 50 );
  }
  else
  {
    elem.style.opacity = 0;
    elem.style.filter = "alpha(opacity=0)";
    elem.style.display = "none";
    elem.style.visibility = "hidden";
  }
}

function togglePillSelector(element) {
    // Reset color of all Pill Texts
    pillTexts = document.getElementsByClassName("pillText")
    for (i=0; i<pillTexts.length; i++) {
        pillTexts[i].style.color = "var(--medium-text-color)"
    }
    // Show Correct Tab
    if (element.innerText == "Register") {
        signIn.style.transform = "translateX(-100vw)"
        signUp.style.left = "calc(50% + 12px)"
        setTimeout(function(){
            signIn.style.opacity = 0.0
            signIn.style.transform = "translateX(-100vw)"
        },  430);
    } else {
        signUp.style.left = "150vw"
        signIn.style.transform = "translateX(0)"
        setTimeout(function(){
            fadeIn( document.getElementById("signIn"), 180 );
        },  100);
    }
    // Move Pill Selector Line
    document.getElementsByClassName("pillSelectorLine")[0].style.left = element.style.left
    // Set Color of Selected Pill text
    element.style.color = "#487cdc"
}

var urlParams = new URLSearchParams(window.location.search);

if (urlParams.get('showSignUp')) {
  expandSignUp();
}