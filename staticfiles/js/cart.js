// AuraShop - E-Commerce Shopping Cart AJAX Handlers

function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begin with the name we want
            if (cookie.substring(0, 10) === ('csrftoken=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

function updateQuantity(productId, changeAction) {
    const qtyInput = document.getElementById(`qty-${productId}`);
    if (!qtyInput) return;
    
    let currentQty = parseInt(qtyInput.value);
    const minVal = parseInt(qtyInput.getAttribute('min') || 1);
    const maxVal = parseInt(qtyInput.getAttribute('max') || 999);
    
    let targetQty = currentQty;
    if (changeAction === 'inc') {
        targetQty = currentQty + 1;
    } else if (changeAction === 'dec') {
        targetQty = currentQty - 1;
    }
    
    // Bounds validation
    if (targetQty < minVal) {
        // Confirm removal if they try to go below 1
        if (confirm("Do you want to remove this item from your shopping bag?")) {
            removeFromCart(productId);
        }
        return;
    }
    
    if (targetQty > maxVal) {
        alert(`Sorry, only ${maxVal} units are available in stock.`);
        return;
    }
    
    // Submit AJAX Request
    const csrfToken = getCSRFToken();
    const formData = new FormData();
    formData.append('product_id', productId);
    formData.append('action', 'update');
    formData.append('qty', targetQty);
    
    fetch('/cart/api/update/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update fields
            qtyInput.value = data.item_qty;
            
            const subtotalText = document.getElementById(`subtotal-${productId}`);
            if (subtotalText) {
                subtotalText.innerText = `LKR ${data.item_subtotal}`;
            }
            
            updateCartSummary(data);
        } else {
            alert(data.error || "An error occurred while updating the cart.");
        }
    })
    .catch(error => {
        console.error("Cart update error:", error);
    });
}

function removeFromCart(productId) {
    const csrfToken = getCSRFToken();
    const formData = new FormData();
    formData.append('product_id', productId);
    formData.append('action', 'remove');
    
    fetch('/cart/api/update/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remove DOM element
            const itemRow = document.getElementById(`cart-item-${productId}`);
            if (itemRow) {
                itemRow.classList.add('animate-slide-out');
                setTimeout(() => {
                    itemRow.remove();
                    // If cart is now empty, reload to show empty state
                    if (data.cart_len === 0) {
                        window.location.reload();
                    }
                }, 300);
            }
            
            updateCartSummary(data);
        } else {
            alert(data.error || "An error occurred while removing the item.");
        }
    })
    .catch(error => {
        console.error("Cart remove error:", error);
    });
}

function updateCartSummary(data) {
    // 1. Update Cart Badge Count
    const cartBadge = document.getElementById('cartCount');
    if (cartBadge) {
        cartBadge.innerText = data.cart_len;
    }
    
    // 2. Update Subtotal & Total
    const subtotalText = document.getElementById('summarySubtotal');
    if (subtotalText) {
        subtotalText.innerText = `LKR ${data.cart_total}`;
    }
    
    const totalText = document.getElementById('summaryTotal');
    if (totalText) {
        totalText.innerText = `LKR ${data.cart_total}`;
    }
}
