var updateBtn = document.getElementsByClassName('update-cart');


for (var i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)
        console.log('USER:', user)
        if (user == 'AnonymousUser') {
            // alert('You are not logged in') 
            // this function will run for anonymous user
            addCookieItem(productId, action)
        } else { //else condition is run for authentic user like admin
            updateUserOrder(productId, action)
        }
    })
}
// for anonymous user 
function addCookieItem(productId, action){
    console.log('NOT LOGGED IN')

    if(action  == 'add'){
        if(cart[productId] == undefined){//this cart[productId] kahabata aako vanda base.html ma function getCookie ma cart vanne variable xa and  this took a productId in cart.js
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }

    }
    if (action  == 'remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            console.log('Remove Item')
            delete cart[productId ]
        }
    }
    console.log('CCart:', cart)
    document.cookie = 'cart=' +JSON.stringify(cart)+ ";domain=;path=/" 
    location.reload()
}










// user logged in vako case ma productid add hune ho where this function will runs on else condition which is in above  
function updateUserOrder(productId, action) {
    console.log("user is logged in and sending data...")
    var url = '/update-Item/';

    fetch(url,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'productId': productId, 'action': action })
        })

        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data:', data);
            location.reload()
        })
}