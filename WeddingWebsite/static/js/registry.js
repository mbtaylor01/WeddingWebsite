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

// get the CSRF token for the request header
const csrftoken = getCookie('csrftoken');

// get all the registry item container divs
const itemContainers = document.querySelectorAll('.item_container');

async function updateItem(e) {
    // get hidden input that contains the item's ID
    let input = e.target.parentElement.querySelector('[name="item_id"]');

    // post item to server
    const response = await fetch("/reserve-item", {
        method: 'POST',
        body: JSON.stringify({ "item_id" : input.value }),
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': csrftoken
        },
        mode: 'same-origin'
    });
    
    await response

    if (response.ok) {
        // get the item's container div from the input element and toggle "reserved" class
        const container = input.parentElement.parentElement.parentElement;
        container.classList.toggle("reserved");

        // if container's class after toggle says reserved, change button and text appropriately
        if (container.className === "item_container reserved") {
            const reserveText = document.createElement('p');
            reserveText.textContent = "You have reserved this item!"; 

            const unreserveButton = document.createElement('button');
            unreserveButton.textContent = "Click to unreserve."

            const reserveButton = container.querySelector('button');
            const purchText = container.querySelector('p');

            reserveButton.replaceWith(reserveText);
            purchText.replaceWith(unreserveButton);

            // give button the "button" type so it doesn't submit the form when clicked
            unreserveButton.type = "button";

        } else if (container.className === "item_container") {
            const reserveButton = document.createElement('button');
            reserveButton.textContent = "Click here if bringing this item!"; 

            const purchText = document.createElement('p');
            purchText.textContent = "Click picture to purchase."

            const reserveText = container.querySelector('p');
            const unreserveButton = container.querySelector('button');

            reserveText.replaceWith(reserveButton);
            unreserveButton.replaceWith(purchText);

            reserveButton.type = "button";
        }
    }
}

/* add event listener to all item container divs that only does 
something if the button inside is clicked */
for (let itemContainer of itemContainers) {
    itemContainer.addEventListener('click', (e) => {
        if (e.target.tagName === 'BUTTON') {
            updateItem(e);
        }
    });
}