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

        productItem.querySelector('.remove-product').addEventListener('click', function () {
            productItem.remove();
        });
    });

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
                console.log(data); 
                alert(data.message || 'Venda realizada com sucesso!');
                atualizarRelatorio();
            })
            .catch(error => console.error('Erro ao realizar venda:', error));
    });

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
        event.preventDefault(); // Prevenir o comportamento padrão do formulário

        const categoryName = document.getElementById('category-name').value;

        // Verificar se o campo está preenchido
        if (!categoryName.trim()) {
            alert('O nome da categoria é obrigatório!');
            return;
        }

        // Enviar a requisição POST para o backend
        fetch('/categorias/cadastrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache', // Evitar cache
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
                alert(data.message || 'Categoria adicionada com sucesso!');
                document.getElementById('category-name').value = ''; // Limpar o campo
                listarCategorias(); // Atualizar a lista de categorias
            })
            .catch(error => console.error('Erro ao adicionar categoria:', error));
    });

    // Listar Categorias
    function listarCategorias() {
        fetch('/categorias/listar', {
            method: 'GET',
            headers: {
                'Cache-Control': 'no-cache', // Evitar cache
            },
        })
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
            .catch(error => console.error('Erro ao listar categorias:', error));
    }

    // Inicializar listagem de categorias ao carregar a página
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

    // Atualizar vendas diárias
    document.getElementById('daily-sales-refresh').addEventListener('click', function () {
        fetch('/vendas/diarias')
            .then(response => response.json())
            .then(data => {
                document.getElementById('daily-total-sales').textContent = data.total_vendas.toFixed(2);
                document.getElementById('daily-total-profit').textContent = data.lucro_total.toFixed(2);

                const paymentMethodsList = document.getElementById('daily-payment-methods');
                paymentMethodsList.innerHTML = '';
                for (const [method, total] of Object.entries(data.formas_pagamento)) {
                    const li = document.createElement('li');
                    li.textContent = `${method}: R$${total.toFixed(2)}`;
                    paymentMethodsList.appendChild(li);
                }
            })
            .catch(error => console.error('Erro ao buscar vendas diárias:', error));
    });

    // Função para atualizar os dados do caixa
    function atualizarCaixa() {
        fetch('/vendas/diarias')
            .then(response => response.json())
            .then(data => {
                document.getElementById('total-sold-today').textContent = data.total_vendas.toFixed(2);
                document.getElementById('daily-profit').textContent = data.lucro_total.toFixed(2);
            })
            .catch(error => console.error('Erro ao atualizar dados do caixa:', error));
    }

    // Adicionar evento ao botão de atualizar caixa
    document.getElementById('refresh-cash-register').addEventListener('click', function () {
        atualizarCaixa();
    });

    // Função para atualizar o status do caixa
    function atualizarStatusCaixa() {
        fetch('/caixa/status')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao obter o status do caixa');
                }
                return response.json();
            })
            .then(data => {
                const statusElement = document.getElementById('cash-register-state');
                const openButton = document.getElementById('open-cash-register');
                const closeButton = document.getElementById('close-cash-register');

                // Atualizar o texto do status
                statusElement.textContent = data.status;

                // Habilitar/desabilitar botões com base no status
                if (data.status === 'Aberto') {
                    openButton.disabled = true;
                    closeButton.disabled = false;
                } else {
                    openButton.disabled = false;
                    closeButton.disabled = true;
                }
            })
            .catch(error => console.error('Erro ao atualizar status do caixa:', error));
    }

    // Abrir o caixa
    document.getElementById('open-cash-register').addEventListener('click', function () {
        fetch('/caixa/abrir', { method: 'POST' })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao abrir o caixa');
                }
                return response.json();
            })
            .then(data => {
                alert(data.message || 'Caixa aberto com sucesso!');
                atualizarStatusCaixa(); // Atualizar o status do caixa
            })
            .catch(error => console.error('Erro ao abrir o caixa:', error));
    });

    // Fechar o caixa
    document.getElementById('close-cash-register').addEventListener('click', function () {
        if (confirm('Deseja realmente fechar o caixa?')) {
            fetch('/caixa/fechar', { method: 'POST' })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erro ao fechar o caixa');
                    }
                    return response.json();
                })
                .then(data => {
                    alert(data.message || 'Caixa fechado com sucesso!');
                    atualizarStatusCaixa(); // Atualizar o status do caixa
                })
                .catch(error => console.error('Erro ao fechar o caixa:', error));
        }
    });

    // Inicializar o status do caixa ao carregar a página
    atualizarStatusCaixa();

    // Relatório por Período
    document.getElementById('gerar-relatorio-periodo').addEventListener('click', function () {
        const inicio = document.getElementById('inicio').value;
        const fim = document.getElementById('fim').value;

        fetch(`/relatorios/periodo?inicio=${inicio}&fim=${fim}`)
            .then(response => response.json())
            .then(data => {
                const resultado = document.getElementById('resultado-periodo');
                resultado.innerHTML = `
                    <p>Total de Vendas: R$ ${data.total_vendas.toFixed(2)}</p>
                    <p>Lucro Total: R$ ${data.lucro_total.toFixed(2)}</p>
                `;
            })
            .catch(error => console.error('Erro ao gerar relatório por período:', error));
    });

    // Relatório por Vendedor
    document.getElementById('gerar-relatorio-vendedor').addEventListener('click', function () {
        const vendedorId = document.getElementById('vendedor-id').value;

        fetch(`/relatorios/vendedor?vendedor_id=${vendedorId}`)
            .then(response => response.json())
            .then(data => {
                const resultado = document.getElementById('resultado-vendedor');
                resultado.innerHTML = `
                    <p>Total de Vendas: R$ ${data.total_vendas.toFixed(2)}</p>
                    <p>Lucro Total: R$ ${data.lucro_total.toFixed(2)}</p>
                `;
            })
            .catch(error => console.error('Erro ao gerar relatório por vendedor:', error));
    });

    // Relatório por Produto
    document.getElementById('gerar-relatorio-produto').addEventListener('click', function () {
        fetch('/relatorios/produto')
            .then(response => response.json())
            .then(data => {
                const resultado = document.getElementById('resultado-produto');
                resultado.innerHTML = data.map(produto => `
                    <p>Produto: ${produto.produto}</p>
                    <p>Total de Vendas: R$ ${produto.total_vendas.toFixed(2)}</p>
                    <p>Lucro Total: R$ ${produto.lucro_total.toFixed(2)}</p>
                    <hr>
                `).join('');
            })
            .catch(error => console.error('Erro ao gerar relatório por produto:', error));
    });
});