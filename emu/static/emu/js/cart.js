const addToCartBtn = document.getElementsByClassName('update-cart');
const removeItemBtn = document.getElementsByClassName('remove-item');

for (let i=0; i<addToCartBtn.length; i++){
    addToCartBtn[i].addEventListener('click',()=>{
        console.log(user)
        let itemID = addToCartBtn[i].dataset.item_id;
        let action = addToCartBtn[i].dataset.action;
        if (user !=='AnonymousUser'){
            updateCart(itemID, action)
        }else{
            updateGuestOrder(itemID, action)
        }
        
    })
}

for (let i=0; i<removeItemBtn.length; i++){
    removeItemBtn[i].addEventListener('click',()=>{
        console.log(user)
        let itemID = removeItemBtn[i].dataset.item_id;
        let action = removeItemBtn[i].dataset.action;
        if (user !=='AnonymousUser'){
            updateCart(itemID, action)
        }else{
            updateGuestOrder(itemID, action)
        }
        
    })
}

const updateGuestOrder = (itemID, action)=>{
    console.log("Guest User")
    console.log(itemID, action)
}

const updateCart= (itemID, action)=>{
    console.log(itemID, action)
    const url = "/add_to_cart/"
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({'item_id': itemID, 'action': action}),
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        location.reload()
    })
}