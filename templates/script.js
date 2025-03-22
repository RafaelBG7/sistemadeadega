document.addEventListener('DOMContentLoaded', () => {
    const categoryForm = document.getElementById('category-form');
    const brandForm = document.getElementById('brand-form');
    const productForm = document.getElementById('product-form');

    const categoryList = document.getElementById('category-list');
    const brandList = document.getElementById('brand-list');
    const productList = document.getElementById('product-list');

    const apiUrl = 'http://localhost:5000';

    // Fetch and display categories
    const fetchCategories = async () => {
        const response = await fetch(`${apiUrl}/categories`);
        const categories = await response.json();
        categoryList.innerHTML = '';
        categories.forEach(category => {
            const li = document.createElement('li');
            li.textContent = category.name;
            categoryList.appendChild(li);
        });
    };

    // Fetch and display brands
    const fetchBrands = async () => {
        const response = await fetch(`${apiUrl}/brands`);
        const brands = await response.json();
        brandList.innerHTML = '';
        brands.forEach(brand => {
            const li = document.createElement('li');
            li.textContent = brand.name;
            brandList.appendChild(li);
        });
    };

    // Fetch and display products
    const fetchProducts = async () => {
        const response = await fetch(`${apiUrl}/products`);
        const products = await response.json();
        productList.innerHTML = '';
        products.forEach(product => {
            const li = document.createElement('li');
            li.textContent = product.name;
            productList.appendChild(li);
        });
    };

    // Add new category
    categoryForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('category-name').value;
        await fetch(`${apiUrl}/categories`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name })
        });
        fetchCategories();
        categoryForm.reset();
    });

    // Add new brand
    brandForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('brand-name').value;
        await fetch(`${apiUrl}/brands`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name })
        });
        fetchBrands();
        brandForm.reset();
    });

    // Add new product
    productForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('product-name').value;
        const category_id = document.getElementById('product-category').value;
        const brand_id = document.getElementById('product-brand').value;
        const purchase_price = document.getElementById('purchase-price').value;
        const selling_price = document.getElementById('selling-price').value;
        await fetch(`${apiUrl}/products`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, category_id, brand_id, purchase_price, selling_price })
        });
        fetchProducts();
        productForm.reset();
    });

    // Initial fetch
    fetchCategories();
    fetchBrands();
    fetchProducts();
});