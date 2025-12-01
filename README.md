# System Project

## Overview
This project is designed to manage a system that includes categories, brands, products, purchase prices, and selling prices. It provides a structured way to handle data related to these entities through models, controllers, and routes.

## Project Structure
```
system-project
├── src
│   ├── models
│   │   ├── category_model.py
│   │   ├── brand_model.py
│   │   ├── product_model.py
│   │   ├── purchase_price_model.py
│   │   └── selling_price_model.py
│   ├── controllers
│   │   ├── category_controller.py
│   │   ├── brand_controller.py
│   │   ├── product_controller.py
│   │   ├── purchase_price_controller.py
│   │   └── selling_price_controller.py
│   ├── routes
│   │   ├── category_routes.py
│   │   ├── brand_routes.py
│   │   ├── product_routes.py
│   │   ├── purchase_price_routes.py
│   │   └── selling_price_routes.py
│   └── types
│       └── index.py
├── requirements.txt
└── README.md
```

## Setup Instructions
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using:
   ```
   pip install -r requirements.txt
   ```

## Usage
- The application provides endpoints for managing categories, brands, products, purchase prices, and selling prices.
- Each entity has its own model, controller, and routes to handle CRUD operations.

## New: Exportar Relatório de Vendas (CSV)
Você pode exportar o relatório de vendas por período em formato CSV com a nova rota:

- Endpoint: `GET /relatorios/periodo/export?inicio=YYYY-MM-DD&fim=YYYY-MM-DD`
- Exemplo: `GET /relatorios/periodo/export?inicio=2025-01-01&fim=2025-01-31`

O endpoint retorna um arquivo CSV com colunas: `id, produto, vendedor, quantidade, data, total_venda, lucro, forma_pagamento`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.