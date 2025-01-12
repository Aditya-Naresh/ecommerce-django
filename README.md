# E-commerce Platform

This is a comprehensive e-commerce platform built with Django. It includes features for managing products, categories, orders, carts, user accounts, and more.

## Project Structure

The project is organized as follows:

- **/ecommerce**: Contains the main Django project settings and configuration.
- **/products**: Manages product listings, categories, and related views.
- **/orders**: Handles order processing, order history, and order management.
- **/carts**: Manages shopping cart functionality and cart sessions.
- **/accounts**: Manages user registration, authentication, and profiles.
- **/static**: Contains static files such as CSS, JavaScript, and images.
- **/templates**: Contains HTML templates for rendering views.

## Features

- User authentication and authorization
- Product listing and categorization
- Shopping cart and checkout process
- Order management and history
- Admin dashboard for managing the platform

## Installation

1. Clone the repository:
    ```bash
    [Ecommerce Repo](https://github.com/Aditya-Naresh/ecommerce-django.git)
    ```
2. Navigate to the project directory:
    ```bash
    cd ecommerce
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Apply migrations:
    ```bash
    python manage.py migrate
    ```
5. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

- Access the platform at `http://127.0.0.1:8000/`
- Use the admin panel at `http://127.0.0.1:8000/admin/` for managing the platform

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

