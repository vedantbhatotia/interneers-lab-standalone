document.addEventListener('DOMContentLoaded', () => {
    fetchProducts();
});
async function fetchProducts() {
    try {
        const response = await fetch('http://localhost:8000/api/products/');

        if (!response.ok) {
            throw new Error('Error ' + response.statusText);
        }
        const data = await response.json();
        console.log('Fetched products:', data);

        displayProducts(data);
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayProducts(products) {
    const productListContainer = document.getElementById('product-list');
    productListContainer.innerHTML = ''; 
    products.forEach((product, index) => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card'; 
        productCard.style.animationDelay = `${index * 0.1}s`; 
        const categoryTitle = product.category_object?.title || "Uncategorized";
        productCard.innerHTML = `
            <div class="product-name">${product.name}</div>
            <div class="product-price">$${product.price}</div>
            <div class="product-stock">In Stock: ${product.stock}</div>
            <div class="product-category">Category: ${categoryTitle}</div>
        `;
        productListContainer.appendChild(productCard);
    });
}
