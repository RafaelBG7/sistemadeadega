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

    // Preencher o select de clientes no formulário de venda
    function preencherClientesVenda() {
        fetch('/clientes/listar')
            .then(response => response.json())
            .then(clientes => {
                const select = document.getElementById('sales-client-id');
                select.innerHTML = '<option value="">Selecione o Cliente (opcional)</option>';
                clientes.forEach(cliente => {
                    const option = document.createElement('option');
                    option.value = cliente.id;
                    option.textContent = `${cliente.nome} (${cliente.cpf})`;
                    select.appendChild(option);
                });
            });
    }
    preencherClientesVenda();

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
        const clientId = document.getElementById('sales-client-id').value; // NOVO

        fetch('/vendas/realizar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                produtos: products,
                forma_pagamento: paymentMethod,
                vendedor_id: vendorId,
                cliente_id: clientId || null // NOVO
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
                showToast(data.message || 'Produto cadastrado com sucesso!');
                listarProdutos();
            })
            .catch(error => console.error('Erro ao cadastrar produto:', error));
    });

    // Atualizar a função listarProdutos
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
                    li.innerHTML = `
                        ID: ${produto.id} | Nome: ${produto.produto} | Preço de Venda: R$${produto.preco_venda.toFixed(2)} | Quantidade: ${produto.quantidade}
                        <button class="edit-product" data-id="${produto.id}" data-nome="${produto.produto}" data-categoria="${produto.categoria_id}" data-preco-custo="${produto.preco_custo}" data-preco-venda="${produto.preco_venda}" data-quantidade="${produto.quantidade}">Editar</button>
                        <button class="remove-product" data-id="${produto.id}">Remover</button>
                    `;
                    productList.appendChild(li);

                    // Adicionar evento de clique ao botão "Editar"
                    li.querySelector('.edit-product').addEventListener('click', function () {
                        const productId = this.getAttribute('data-id');
                        const productName = this.getAttribute('data-nome');
                        const categoryId = this.getAttribute('data-categoria');
                        const purchasePrice = this.getAttribute('data-preco-custo');
                        const sellingPrice = this.getAttribute('data-preco-venda');
                        const quantity = this.getAttribute('data-quantidade');

                        // Preencher o formulário de edição com os dados do produto
                        document.getElementById('edit-product-id').value = productId;
                        document.getElementById('edit-product-name').value = productName;
                        document.getElementById('edit-product-category-id').value = categoryId;
                        document.getElementById('edit-purchase-price').value = purchasePrice;
                        document.getElementById('edit-selling-price').value = sellingPrice;
                        document.getElementById('edit-product-quantity').value = quantity;

                        // Rolagem para o formulário de edição
                        document.querySelector('.editar-produto').scrollIntoView({ behavior: 'smooth' });
                    });

                    // Adicionar evento de clique ao botão "Remover"
                    li.querySelector('.remove-product').addEventListener('click', function () {
                        const productId = this.getAttribute('data-id');
                        removerProduto(productId);
                    });
                });
            })
            .catch(error => console.error('Erro ao listar produtos:', error));
    }

    function removerProduto(productId) {
        if (confirm('Tem certeza de que deseja remover este produto?')) {
            fetch(`/produtos/${productId}`, {
                method: 'DELETE',
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erro ao remover produto');
                    }
                    return response.json();
                })
                .then(data => {
                    alert(data.message || 'Produto removido com sucesso!');
                    listarProdutos(); // Atualizar a lista de produtos
                })
                .catch(error => console.error('Erro ao remover produto:', error));
        }
    }

    // Inicializar listagem de produtos
    listarProdutos();

    // Função para editar um produto
    function editarProduto() {
        const produtoId = document.getElementById('edit-product-id').value;
        const productName = document.getElementById('edit-product-name').value;
        const categoryId = document.getElementById('edit-product-category-id').value;
        const purchasePrice = parseFloat(document.getElementById('edit-purchase-price').value);
        const sellingPrice = parseFloat(document.getElementById('edit-selling-price').value);
        const quantity = parseInt(document.getElementById('edit-product-quantity').value, 10);

        if (!produtoId || isNaN(produtoId)) {
            alert('Por favor, insira um ID de produto válido.');
            return;
        }

        const payload = {
            produto: productName || undefined,
            categoria_id: categoryId || undefined,
            preco_custo: isNaN(purchasePrice) ? undefined : purchasePrice,
            preco_venda: isNaN(sellingPrice) ? undefined : sellingPrice,
            quantidade: isNaN(quantity) ? undefined : quantity,
        };

        fetch(`/produtos/editar/${produtoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao editar produto');
                }
                return response.json();
            })
            .then(data => {
                alert(data.message || 'Produto editado com sucesso!');
                listarProdutos(); // Atualizar a lista de produtos
            })
            .catch(error => console.error('Erro ao editar produto:', error));
    }

    // Adicionar evento ao botão de editar produto
    document.getElementById('edit-product-button').addEventListener('click', editarProduto);

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

    // Função para listar produtos com estoque baixo
    function listarEstoqueBaixo() {
        const limiteInput = document.getElementById('low-stock-limit');
        const limite = parseInt(limiteInput.value, 10);

        if (isNaN(limite) || limite <= 0) {
            alert('Por favor, insira um número válido para o limite de estoque.');
            return;
        }

        fetch(`/produtos/estoque-baixo?limite=${limite}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao buscar produtos com estoque baixo');
                }
                return response.json();
            })
            .then(data => {
                const lowStockList = document.getElementById('low-stock-list');
                lowStockList.innerHTML = '';
                if (data.length === 0) {
                    lowStockList.innerHTML = '<li>Nenhum produto com estoque baixo encontrado.</li>';
                    return;
                }
                data.forEach(produto => {
                    const li = document.createElement('li');
                    li.textContent = `ID: ${produto.id} | Nome: ${produto.produto} | Quantidade: ${produto.quantidade} | Categoria: ${produto.categoria}`;
                    lowStockList.appendChild(li);
                });
            })
            .catch(error => console.error('Erro ao listar produtos com estoque baixo:', error));
    }

    // Adicionar evento ao botão de estoque baixo
    document.getElementById('low-stock-button').addEventListener('click', listarEstoqueBaixo);

    // Cadastrar Cliente
    document.getElementById('client-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const nome = document.getElementById('client-name').value;
        const cpf = document.getElementById('client-cpf').value;
        const data_nascimento = document.getElementById('client-birthdate').value;
        const telefone = document.getElementById('client-phone').value;
        const email = document.getElementById('client-email').value;

        fetch('/clientes/cadastrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                nome,
                cpf,
                data_nascimento,
                telefone,
                email
            }),
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message || 'Cliente cadastrado com sucesso!');
                listarClientes();
            })
            .catch(error => console.error('Erro ao cadastrar cliente:', error));
    });

    // Listar Clientes
    function listarClientes() {
        fetch('/clientes/listar')
            .then(response => response.json())
            .then(data => {
                const clientList = document.getElementById('client-list');
                clientList.innerHTML = '';
                data.forEach(cliente => {
                    const li = document.createElement('li');
                    li.textContent = `Nome: ${cliente.nome} | CPF: ${cliente.cpf} | Nascimento: ${cliente.data_nascimento} | Telefone: ${cliente.telefone} | Email: ${cliente.email}`;
                    clientList.appendChild(li);
                });
            })
            .catch(error => console.error('Erro ao listar clientes:', error));
    }

    // Inicializar listagem de clientes
    listarClientes();

    // Preencher o select de clientes para relatório
    function preencherClientesRelatorio() {
        fetch('/clientes/listar')
            .then(response => response.json())
            .then(clientes => {
                const select = document.getElementById('cliente-relatorio-id');
                select.innerHTML = '<option value="">Selecione o Cliente</option>';
                clientes.forEach(cliente => {
                    const option = document.createElement('option');
                    option.value = cliente.id;
                    option.textContent = `${cliente.nome} (${cliente.cpf})`;
                    select.appendChild(option);
                });
            });
    }
    preencherClientesRelatorio();

    // Gerar relatório por cliente
    document.getElementById('gerar-relatorio-cliente').addEventListener('click', function () {
        const clienteId = document.getElementById('cliente-relatorio-id').value;
        if (!clienteId) {
            alert('Selecione um cliente!');
            return;
        }
        fetch(`/relatorios/cliente?cliente_id=${clienteId}`)
            .then(response => response.json())
            .then(data => {
                const resultado = document.getElementById('resultado-cliente');
                if (data.error) {
                    resultado.innerHTML = `<p>Erro: ${data.error}</p>`;
                    return;
                }
                resultado.innerHTML = `
                    <p>Total de Vendas: R$ ${data.total_vendas.toFixed(2)}</p>
                    <p>Lucro Total: R$ ${data.lucro_total.toFixed(2)}</p>
                    <h4>Vendas:</h4>
                    <ul>
                        ${data.vendas.map(venda => `
                            <li>
                                Produto: ${venda.produto} |
                                Quantidade: ${venda.quantidade} |
                                Data: ${venda.data} |
                                Total: R$${venda.total_venda.toFixed(2)} |
                                Lucro: R$${venda.lucro.toFixed(2)} |
                                Pagamento: ${venda.forma_pagamento}
                            </li>
                        `).join('')}
                    </ul>
                `;
            })
            .catch(error => {
                document.getElementById('resultado-cliente').innerHTML = `<p>Erro ao gerar relatório: ${error}</p>`;
            });
    });

    // Exibir status de fidelidade do cliente selecionado
    function mostrarStatusFidelidade(cliente) {
        const fidelidadeDiv = document.getElementById('fidelidade-status');
        if (!fidelidadeDiv) return;

        if (!cliente) {
            fidelidadeDiv.textContent = '';
            return;
        }

        if (cliente.fidelidade_ativo) {
            fidelidadeDiv.textContent = 'Desconto de 5% disponível para esta compra!';
            fidelidadeDiv.style.color = 'green';
        } else {
            const falta = 100 - (cliente.fidelidade_credito || 0);
            fidelidadeDiv.textContent = `Faltam R$${falta.toFixed(2)} em compras para ganhar 5% de desconto na próxima compra.`;
            fidelidadeDiv.style.color = 'black';
        }
    }

    // Atualizar status de fidelidade ao trocar o cliente
    function atualizarStatusFidelidade() {
        const select = document.getElementById('sales-client-id');
        const clienteId = select.value;
        if (!clienteId) {
            mostrarStatusFidelidade(null);
            return;
        }
        fetch('/clientes/listar')
            .then(response => response.json())
            .then(clientes => {
                const cliente = clientes.find(c => c.id == clienteId);
                mostrarStatusFidelidade(cliente);
            });
    }

    // Adicione um div no HTML onde deseja mostrar o status, por exemplo:
    // <div id="fidelidade-status"></div>

    // Chame a função ao trocar o cliente
    document.getElementById('sales-client-id').addEventListener('change', atualizarStatusFidelidade);

    // Também chame após preencher os clientes
    setTimeout(atualizarStatusFidelidade, 500); // Pequeno delay para garantir que o select foi preenchido

    function showToast(msg) {
        const toast = document.getElementById('toast');
        toast.textContent = msg;
        toast.style.display = 'block';
        setTimeout(() => { toast.style.display = 'none'; }, 2500);
    }
});