var log = function() {
    console.log.apply(console, arguments)
}

var body = document.querySelector('body')
var form = document.querySelector('.login-form')
var loginButton = document.querySelector('#id-button-login')
var user = document.querySelector('#id-input-username')
var userValue = user.getAttribute()

user.setAttribute('value', 'new username')

user.removeAttribute('value')
user.hasAttribute('value')

var button = document.createElement('button')
button.innerHTML = 'new user'

var form = document.querySelector('.login-form')
form.appendChild(button)

var pwd = document.querySelector('#id-input-password')
form.removeChild(pwd)
pwd.remove()

var loginButton = document.querySelector('#id-input-login')
var clicked = function () {
    log('is clicked')
}

loginButton.addEventListener('click', clicked)

var buttons = document.querySelectorAll('.radio-button')

for(var i = 0; i < buttons.length; i++) {
    var button = buttons[i]
    button.addEventListener('click', function (event) {
        var self = event.target
        clearActive()
        self.classList.add('active')
    })
}

var clearActive = function () {
    var active = document.querySelector('.active')
    if (active != null) {
        active.classList.remove("active")
    }
}


var __main = function () {
}

__main()