document.addEventListener('DOMContentLoaded', function() {
    // Adicionar mais campos de produto
    document.getElementById('add-product').addEventListener('click', function() {
        const productsContainer = document.getElementById('products-container');
        const productItem = document.createElement('div');
        productItem.classList.add('product-item');
        productItem.innerHTML = `
            <input type="text" class="product-id" placeholder="ID do Produto" required>
            <input type="number" class="product-quantity" placeholder="Quantidade" required>
        `;
        productsContainer.appendChild(productItem);
    });

    // Realizar Venda
    document.getElementById('sales-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const products = [];
        document.querySelectorAll('.product-item').forEach(item => {
            const productId = item.querySelector('.product-id').value;
            const quantity = item.querySelector('.product-quantity').value;
            products.push({ produto_id: productId, quantidade: quantity });
        });

        const paymentMethod = document.getElementById('payment-method').value;
        const vendorId = document.getElementById('sales-vendor-id').value;

        fetch('/vendas/realizar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                produtos: products,
                forma_pagamento: paymentMethod,
                vendedor_id: vendorId,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Venda realizada:', data);
            // Atualizar relatório de vendas
        })
        .catch(error => console.error('Erro ao realizar venda:', error));
    });
});