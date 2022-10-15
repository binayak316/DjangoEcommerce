var updateBtn = document.getElementsByClassName('update-cart');


for (var i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)
        console.log('USER:', user)
        if (user == 'AnonymousUser') {
            console.log('User Is Not Logged In')
        } else {
            updateUserOrder(productId, action)
        }
    })
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