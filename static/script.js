document.addEventListener('DOMContentLoaded', function() {
    // Função para abrir uma aba
    window.openTab = function(tabName) {
        const tabContents = document.querySelectorAll('.tab-content');
        tabContents.forEach(tabContent => {
            tabContent.classList.remove('active-tab');
        });
        document.getElementById(tabName).classList.add('active-tab');
    };

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
            console.log('Categoria adicionada:', data);
        })
        .catch(error => console.error('Erro ao adicionar categoria:', error));
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
            console.log('Marca adicionada:', data);
        })
        .catch(error => console.error('Erro ao adicionar marca:', error));
    });

    // Adicionar Produto
    document.getElementById('product-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const productName = document.getElementById('product-name').value;
        const productCategory = document.getElementById('product-category').value;
        const productBrand = document.getElementById('product-brand').value;
        const purchasePrice = document.getElementById('purchase-price').value;
        const sellingPrice = document.getElementById('selling-price').value;
        const productQuantity = document.getElementById('product-quantity').value;

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
                quantidade: productQuantity,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Produto adicionado:', data);
        })
        .catch(error => console.error('Erro ao adicionar produto:', error));
    });

    // Realizar Venda
    document.getElementById('sales-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const productId = document.getElementById('sales-product-id').value;
        const vendorId = document.getElementById('sales-vendor-id').value;
        const quantity = document.getElementById('sales-quantity').value;

        fetch('/vendas/realizar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                produto_id: productId,
                vendedor_id: vendorId,
                quantidade: quantity,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Venda realizada:', data);
        })
        .catch(error => console.error('Erro ao realizar venda:', error));
    });

    // Adicionar Vendedor
    document.getElementById('vendor-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const vendorName = document.getElementById('vendor-name').value;
        const vendorEmail = document.getElementById('vendor-email').value;
        const vendorPhone = document.getElementById('vendor-phone').value;

        fetch('/vendedores/cadastrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                nome: vendorName,
                email: vendorEmail,
                telefone: vendorPhone,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Vendedor adicionado:', data);
        })
        .catch(error => console.error('Erro ao adicionar vendedor:', error));
    });
});