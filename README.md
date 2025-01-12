# LLM-based Product Recommendation System

This project implements a personalized product recommendation system enhanced by a **Large Language Model (LLM)** and **embedding-based ranking** for accurate, context-aware recommendations.

---

## **Usage**
1. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venvbin/activate  
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the API documentation**:
   - Open your browser and go to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## **Overview**
The system includes the following key components:
1. **User Management**: Handles user registration and retrieval.
2. **Product Management**: Enables adding and listing products.
3. **Recommendation Engine**: Matches user preferences with products and ranks them using LLMs and embeddings.
4. **Feedback System**: Allows users to submit feedback to improve recommendations.

---

## **Endpoints**

### **1. User Management (`auth.py`)**

#### **POST /auth/users/**
- **Purpose**: Create a new user in the system.
- **Input**:  
  ```json
  {
    "username": "test_user",
    "password": "test_pass",
    "preferences": {
      "category": "electronics",
      "price_range": [500, 1500],
      "brands": ["Laptop", "Tablet"]
    }
  }
  ```
- **Process**:
  - Validates if the `username` already exists.
  - Hashes the password using `bcrypt`.
  - Serializes the `preferences` dictionary into a JSON string for storage in the database.
  - Saves the user in the database with their preferences.
- **Output**:
  ```json
  {
    "id": 1,
    "username": "test_user",
    "preferences": {
      "category": "electronics",
      "price_range": [500, 1500],
      "brands": ["Laptop", "Tablet"]
    }
  }
  ```

---

#### **GET /auth/users/{user_id}**
- **Purpose**: Retrieve user details by their ID.
- **Input**: User ID (e.g., `1`).
- **Process**:
  - Queries the database for the user with the given ID.
  - Deserializes the `preferences` field from JSON into a dictionary.
- **Output**:
  ```json
  {
    "id": 1,
    "username": "test_user",
    "preferences": {
      "category": "electronics",
      "price_range": [500, 1500],
      "brands": ["Laptop", "Tablet"]
    }
  }
  ```

---

### **2. Product Management (`product.py`)**

#### **POST /products/**
- **Purpose**: Add a new product to the system.
- **Input**:  
  ```json
  {
    "name": "Laptop X1",
    "description": "High-performance laptop",
    "price": 1200,
    "category": "electronics"
  }
  ```
- **Process**:
  - Saves the product details into the database.
- **Output**:
  ```json
  {
    "id": 1,
    "name": "Laptop X1",
    "description": "High-performance laptop",
    "price": 1200,
    "category": "electronics"
  }
  ```

---

#### **GET /products/**
- **Purpose**: Retrieve a list of all products in the system.
- **Process**:
  - Queries the database for all products and returns them.
- **Output**:
  ```json
  [
    {
      "id": 1,
      "name": "Laptop X1",
      "description": "High-performance laptop",
      "price": 1200,
      "category": "electronics"
    },
    {
      "id": 2,
      "name": "Tablet Pro",
      "description": "Lightweight and powerful",
      "price": 800,
      "category": "electronics"
    }
  ]
  ```

---

### **3. Recommendation Engine (`recommendation.py`)**

#### **GET /recommendations/{user_id}**
- **Purpose**: Provide personalized recommendations for a user.
- **Input**: User ID (e.g., `1`).
- **Process**:
  1. Fetches the user's preferences:
     - **Category**: The primary category for recommendations (e.g., `electronics`).
     - **Price Range**: Filters products within the user's budget (e.g., `[500, 1500]`).
     - **Brands**: Matches user-specified brands or keywords (e.g., `["Laptop", "Tablet"]`).
  2. Queries the database for products matching the category.
  3. Uses **sentence-transformers** to compute similarity scores between user preferences and product descriptions.
  4. Ranks products by similarity scores for better relevance.
- **Output**:
  ```json
  {
    "user_id": 1,
    "preferred_category": "electronics",
    "ranked_products": [
      {
        "id": 1,
        "name": "Laptop X1",
        "description": "High-performance laptop",
        "price": 1200,
        "category": "electronics"
      },
      {
        "id": 2,
        "name": "Tablet Pro",
        "description": "Lightweight and powerful",
        "price": 800,
        "category": "electronics"
      }
    ]
  }
  ```

---

### **4. Feedback System (`feedback.py`)**

#### **POST /feedback/**
- **Purpose**: Collect user feedback on specific products.
- **Input**:  
  ```json
  {
    "product_id": 1,
    "rating": 5,
    "comment": "Excellent product!"
  }
  ```
- **Process**:
  - Validates if the user and product exist in the database.
  - Saves the feedback with the user ID, product ID, rating, and optional comment.
- **Output**:
  ```json
  {
    "id": 1,
    "user_id": 1,
    "product_id": 1,
    "rating": 5,
    "comment": "Excellent product!"
  }
  ```

---

## **Technologies Used**

1. **FastAPI**: Framework for building APIs.
2. **SQLAlchemy**: ORM for database management.
3. **bcrypt**: For password hashing.
4. **Transformers**: Hugging Face library for integrating Large Language Models.
5. **Sentence-Transformers**: For semantic similarity scoring.

---
