document.addEventListener('DOMContentLoaded', function () {
    // Adicionar mais campos de produto na seção de vendas
    document.getElementById('add-product').addEventListener('click', function () {
        const productsContainer = document.getElementById('products-container');
        const productItem = document.createElement('div');
        productItem.classList.add('product-item');
        productItem.innerHTML = `
            <input type="text" class="product-name" placeholder="Nome do Produto" required>
            <input type="number" class="product-quantity" placeholder="Quantidade" required>
            <button type="button" class="remove-product">Remover</button>
        `;
        productsContainer.appendChild(productItem);

        // Adicionar funcionalidade para remover o produto
        productItem.querySelector('.remove-product').addEventListener('click', function () {
            productItem.remove();
        });
    });

    // Realizar Venda
    document.getElementById('sales-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const products = [];
        document.querySelectorAll('.product-item').forEach(item => {
            const productName = item.querySelector('.product-name').value;
            const quantity = parseInt(item.querySelector('.product-quantity').value, 10);
            products.push({ produto_nome: productName, quantidade: quantity });
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
                alert(data.message || 'Venda realizada com sucesso!');
                atualizarRelatorio();
            })
            .catch(error => console.error('Erro ao realizar venda:', error));
    });

    // Atualizar relatório de vendas
    function atualizarRelatorio() {
        fetch('/vendas/listar')
            .then(response => response.json())
            .then(data => {
                const salesReport = document.getElementById('sales-report');
                salesReport.innerHTML = '';
                data.forEach(venda => {
                    const li = document.createElement('li');
                    li.textContent = `Produto: ${venda.produto} | Vendedor: ${venda.vendedor} | Quantidade: ${venda.quantidade} | Total: R$${venda.total_venda.toFixed(2)} | Data: ${venda.data}`;
                    salesReport.appendChild(li);
                });
            })
            .catch(error => console.error('Erro ao atualizar relatório:', error));
    }

    // Inicializar relatório de vendas
    atualizarRelatorio();

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
            .then(response => response.json())
            .then(data => {
                alert(data.message || 'Categoria adicionada com sucesso!');
                listarCategorias();
            })
            .catch(error => console.error('Erro ao adicionar categoria:', error));
    });

    // Listar Categorias
    function listarCategorias() {
        fetch('/categorias/listar')
            .then(response => response.json())
            .then(data => {
                const categoryList = document.getElementById('category-list');
                categoryList.innerHTML = '';
                data.forEach(categoria => {
                    const li = document.createElement('li');
                    li.textContent = categoria.nome;
                    categoryList.appendChild(li);
                });
            })
            .catch(error => console.error('Erro ao listar categorias:', error));
    }

    // Inicializar listagem de categorias
    listarCategorias();

    // Função para buscar categorias pelo nome
    function buscarCategoriasPorNome(inputElement) {
        const query = inputElement.value;
        if (query.length < 2) return; // Buscar apenas se houver pelo menos 2 caracteres

        fetch(`/categorias/buscar?nome=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                const datalistId = `datalist-categorias`;
                let datalist = document.getElementById(datalistId);

                if (!datalist) {
                    datalist = document.createElement('datalist');
                    datalist.id = datalistId;
                    document.body.appendChild(datalist);
                }

                datalist.innerHTML = '';
                data.forEach(categoria => {
                    const option = document.createElement('option');
                    option.value = categoria.nome;
                    option.dataset.id = categoria.id;
                    datalist.appendChild(option);
                });

                inputElement.setAttribute('list', datalistId);

                // Atualizar o campo oculto com o ID da categoria selecionada
                inputElement.addEventListener('change', function () {
                    const selectedOption = Array.from(datalist.options).find(
                        option => option.value === inputElement.value
                    );
                    const categoryIdInput = document.getElementById('product-category-id');
                    categoryIdInput.value = selectedOption ? selectedOption.dataset.id : '';
                });
            })
            .catch(error => console.error('Erro ao buscar categorias:', error));
    }

    // Adicionar funcionalidade de autocompletar no campo de categoria
    const categoryInput = document.getElementById('product-category');
    categoryInput.addEventListener('input', function () {
        buscarCategoriasPorNome(categoryInput);
    });

    // Adicionar Produto
    document.getElementById('product-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const productName = document.getElementById('product-name').value;
        const categoryId = document.getElementById('product-category-id').value; // ID da categoria selecionada
        const purchasePrice = parseFloat(document.getElementById('purchase-price').value);
        const sellingPrice = parseFloat(document.getElementById('selling-price').value);
        const quantity = parseInt(document.getElementById('product-quantity').value, 10);

        if (!categoryId) {
            alert('Por favor, selecione uma categoria válida!');
            return;
        }

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
            .then(response => response.json())
            .then(data => {
                alert(data.message || 'Produto cadastrado com sucesso!');
                listarProdutos();
            })
            .catch(error => console.error('Erro ao cadastrar produto:', error));
    });

    // Função para listar produtos
    function listarProdutos() {
        fetch('/produtos/listar')
            .then(response => response.json())
            .then(data => {
                const productList = document.getElementById('product-list');
                productList.innerHTML = '';
                data.forEach(produto => {
                    const li = document.createElement('li');
                    li.textContent = `ID: ${produto.id} | Nome: ${produto.produto} | Preço de Venda: R$${produto.preco_venda.toFixed(2)} | Quantidade: ${produto.quantidade}`;
                    productList.appendChild(li);
                });
            })
            .catch(error => console.error('Erro ao listar produtos:', error));
    }

    // Inicializar listagem de produtos
    listarProdutos();

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
            .then(response => response.json())
            .then(data => {
                alert(data.message || 'Vendedor cadastrado com sucesso!');
                listarVendedores();
            })
            .catch(error => console.error('Erro ao cadastrar vendedor:', error));
    });

    // Listar Vendedores
    function listarVendedores() {
        fetch('/vendedores/listar')
            .then(response => response.json())
            .then(data => {
                const vendorList = document.getElementById('vendor-list');
                vendorList.innerHTML = '';
                data.forEach(vendedor => {
                    const li = document.createElement('li');
                    li.textContent = `ID: ${vendedor.id} | Nome: ${vendedor.nome} | Email: ${vendedor.email} | Telefone: ${vendedor.telefone} | Ativo: ${vendedor.ativo ? 'Sim' : 'Não'}`;
                    vendorList.appendChild(li);
                });
            })
            .catch(error => console.error('Erro ao listar vendedores:', error));
    }

    // Inicializar listagem de vendedores
    listarVendedores();
});