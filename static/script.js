document.addEventListener('DOMContentLoaded', function() {
    // Adicionar Categoria
    document.getElementById('category-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const categoryName = document.getElementById('category-name').value;

        fetch('/categorias/cadastrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nome: categoryName }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Atualizar a lista de categorias
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    // Adicionar Marca
    document.getElementById('brand-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const brandName = document.getElementById('brand-name').value;

        fetch('/marcas/cadastrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nome: brandName }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Atualizar a lista de marcas
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    // Adicionar Produto
    document.getElementById('product-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const productName = document.getElementById('product-name').value;
        const productCategory = document.getElementById('product-category').value;
        const productBrand = document.getElementById('product-brand').value;
        const purchasePrice = document.getElementById('purchase-price').value;
        const sellingPrice = document.getElementById('selling-price').value;

        fetch('/produtos/cadastrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                produto: productName,
                categoria_id: productCategory,
                marca_id: productBrand,
                preco_custo: purchasePrice,
                preco_venda: sellingPrice,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Atualizar a lista de produtos
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});