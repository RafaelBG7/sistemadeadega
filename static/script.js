document.addEventListener('DOMContentLoaded', function () {
    // Função para exibir mensagens de erro
    function exibirErro(mensagem) {
        console.error(mensagem);
        alert(mensagem);
    }

    // ==========================
    // Categorias
    // ==========================
    // Adicionar Categoria
    document.getElementById('category-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const categoryName = document.getElementById('category-name').value;

        fetch('/categorias/cadastrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nome: categoryName }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao cadastrar categoria');
                }
                return response.json();
            })
            .then(data => {
                alert(data.message || 'Categoria cadastrada com sucesso!');
                listarCategorias();
            })
            .catch(error => exibirErro('Erro ao cadastrar categoria: ' + error.message));
    });

    // Listar Categorias
    function listarCategorias() {
        fetch('/categorias/listar')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao listar categorias');
                }
                return response.json();
            })
            .then(data => {
                const categoryList = document.getElementById('category-list');
                categoryList.innerHTML = '';
                data.forEach(categoria => {
                    const li = document.createElement('li');
                    li.textContent = categoria.nome;
                    categoryList.appendChild(li);
                });
            })
            .catch(error => exibirErro('Erro ao listar categorias: ' + error.message));
    }

    listarCategorias();

    // ==========================
    // Produtos
    // ==========================
    // Adicionar Produto
    document.getElementById('product-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const productName = document.getElementById('product-name').value;
        const categoryId = parseInt(document.getElementById('product-category-id').value, 10);
        const purchasePrice = parseFloat(document.getElementById('purchase-price').value);
        const sellingPrice = parseFloat(document.getElementById('selling-price').value);
        const quantity = parseInt(document.getElementById('product-quantity').value, 10);

        // Verificar se todos os campos estão preenchidos
        if (!productName || isNaN(categoryId) || isNaN(purchasePrice) || isNaN(sellingPrice) || isNaN(quantity)) {
            alert('Todos os campos são obrigatórios!');
            return;
        }

        // Enviar requisição para o backend
        fetch('/produtos/cadastrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                produto: productName,
                categoria_id: categoryId,
                preco_custo: purchasePrice,
                preco_venda: sellingPrice,
                quantidade: quantity,
            }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao cadastrar produto');
                }
                return response.json();
            })
            .then(data => {
                alert(data.message || 'Produto cadastrado com sucesso!');
                listarProdutos(); // Atualizar a lista de produtos
            })
            .catch(error => exibirErro('Erro ao cadastrar produto: ' + error.message));
    });

    // Listar Produtos
    function listarProdutos() {
        fetch('/produtos/listar')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao listar produtos');
                }
                return response.json();
            })
            .then(data => {
                const productList = document.getElementById('product-list');
                productList.innerHTML = '';
                data.forEach(produto => {
                    const li = document.createElement('li');
                    li.textContent = `ID: ${produto.id} | Nome: ${produto.produto} | Preço de Venda: R$${produto.preco_venda.toFixed(2)} | Quantidade: ${produto.quantidade}`;
                    productList.appendChild(li);
                });
            })
            .catch(error => exibirErro('Erro ao listar produtos: ' + error.message));
    }

    // Inicializar listagem de produtos ao carregar a página
    listarProdutos();

    // ==========================
    // Vendedores
    // ==========================
    // Adicionar Vendedor
    document.getElementById('vendor-form').addEventListener('submit', function (event) {
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
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao cadastrar vendedor');
                }
                return response.json();
            })
            .then(data => {
                alert(data.message || 'Vendedor cadastrado com sucesso!');
                listarVendedores();
            })
            .catch(error => exibirErro('Erro ao cadastrar vendedor: ' + error.message));
    });

    // Listar Vendedores
    function listarVendedores() {
        fetch('/vendedores/listar')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao listar vendedores');
                }
                return response.json();
            })
            .then(data => {
                const vendorList = document.getElementById('vendor-list');
                vendorList.innerHTML = '';
                data.forEach(vendedor => {
                    const li = document.createElement('li');
                    li.textContent = `ID: ${vendedor.id} | Nome: ${vendedor.nome} | Email: ${vendedor.email} | Telefone: ${vendedor.telefone}`;
                    vendorList.appendChild(li);
                });
            })
            .catch(error => exibirErro('Erro ao listar vendedores: ' + error.message));
    }

    listarVendedores();

    // ==========================
    // Vendas
    // ==========================
    // Realizar Venda
    document.getElementById('sale-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const productName = document.getElementById('sale-product-name').value;
        const quantity = parseInt(document.getElementById('sale-quantity').value, 10);
        const paymentMethod = document.getElementById('sale-payment-method').value;
        const vendorId = parseInt(document.getElementById('sale-vendor-id').value, 10);

        fetch('/vendas/realizar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                produtos: [{ produto_nome: productName, quantidade: quantity }],
                forma_pagamento: paymentMethod,
                vendedor_id: vendorId,
            }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao realizar venda');
                }
                return response.json();
            })
            .then(data => {
                alert(data.message || 'Venda realizada com sucesso!');
            })
            .catch(error => exibirErro('Erro ao realizar venda: ' + error.message));
    });
});