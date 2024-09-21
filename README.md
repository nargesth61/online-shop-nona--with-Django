# E-Commerce Platform

## Project Overview

This project is a fully responsive e-commerce platform designed with flexibility and scalability in mind. It allows users to easily register and log in using their email and password, and provides separate admin and user panels for management and browsing.

Key features include:
- **Responsive Design**: The frontend is optimized for various screen sizes, ensuring a seamless shopping experience on both desktop and mobile devices.
- **Customizable Product Attributes**: For each product, you can add any number of attributes (e.g., color, size, material), making the platform adaptable to various product types.
- **Automatic Slug Generation**: The slug for each product is automatically generated based on the product name, ensuring clean and user-friendly URLs.
- **Admin and User Panels**: The admin panel is separate from the user panel, offering administrators the ability to manage products, orders, and users efficiently.
- **Discount System**: Discounts can be applied as a percentage to the base price of products, and the final price is automatically adjusted.
- **Email-Based Authentication**: Users can register and log in using their email and password.

The project is containerized using **Docker** and orchestrated with **Docker Compose**, ensuring an easy setup and consistent development environment.

## Features

1. **Responsive Design**
    - Mobile-first approach with a fully responsive layout.
    - Adaptable to any device size (mobile, tablet, desktop).

2. **Product Management**
    - Unlimited product attributes (color, size, material, etc.) for each product.
    - Automatic slug generation based on the product name for SEO-friendly URLs.

3. **Discount System**
    - Admins can set a percentage-based discount on the base price of any product.
    - The discount is automatically applied to display the final price.

4. **Authentication**
    - User registration and login are handled via email and password.
    - Password reset functionality included.

5. **Admin Panel**
    - Separate admin panel for product management, order processing, and user management.
    - Only accessible by admin users.

6. **User Panel**
    - Simple user panel for viewing order history and account details.

7. **Dockerized Environment**
    - The project uses Docker and Docker Compose for easy setup and deployment.
    - All dependencies are containerized, ensuring consistency across environments.

## Technologies

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla or React, based on preference)
- **Backend**: Django (Python)
- **Database**: PostgreSQL (or MySQL, depending on configuration)
- **Authentication**: Django Allauth
- **Containerization**: Docker & Docker Compose

## Prerequisites

Ensure you have the following installed:
- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Setup and Installation

Follow these steps to set up the project locally:

1. **Clone the repository**:
    ```bash
   
    ```

2. **Create a `.enve` file**:
    Create a `.enve` file at the project root and specify environment variables for database, email, and other configurations. Example:
    ```env
    DEBUG=True
    SECRET_KEY=your-secret-key
    DATABASE_NAME=ecommerce_db
    DATABASE_USER=postgres
    DATABASE_PASSWORD=yourpassword
    DATABASE_HOST=db
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=your-email@gmail.com
    EMAIL_HOST_PASSWORD=your-email-password
    ```

3. **Build and start the containers**:
    ```bash
    docker-compose up --build
    ```

4. **Apply migrations and create a superuser**:
    Open a new terminal and run the following commands inside the container:
    ```bash
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    ```

5. **Access the application**:
    - The project will be accessible at `http://localhost:8000/`.
    - Admin panel: `http://localhost:8000/admin/` (log in with the superuser credentials).

## Usage

### Admin Panel
- Admins can add, update, and delete products.
- Set discounts for products, manage orders, and oversee user accounts.

### User Panel
- Users can view product listings, add items to their cart, and place orders.
- Registered users can log in to view order history and manage their accounts.

## File Structure