# LLM-based Product Recommendation System

This project implements a personalized product recommendation system using a pre-trained large language model (LLM).

---

## **Usuage**
1. Create a virtual environment and activate it.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the application: `uvicorn main:app --reload`.

---

## **Overview**
The system includes the following key components:
1. **User Management**: Handles user registration and retrieval.
2. **Product Management**: Enables adding and listing products.
3. **Recommendation Engine**: Provides personalized product recommendations.
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
- **Purpose**: Provide personalized product recommendations for a user.
- **Input**: User ID (e.g., `1`).
- **Process**:
  1. Fetches the user's preferences:
     - **Category**: The primary category for recommendations (e.g., `electronics`).
     - **Price Range**: Preferred price range for products (e.g., `[500, 1500]`).
     - **Brands**: Preferred brands or keywords (e.g., `["Laptop", "Tablet"]`).
  2. Queries the database for products matching the category.
  3. Scores each product based on:
     - **Price**: Adds points if the product falls within the preferred price range.
     - **Brand Match**: Adds points if the product name matches any preferred brands.
  4. Ranks products by their scores.
- **Output**:
  ```json
  {
    "user_id": 1,
    "preferred_category": "electronics",
    "recommendations": [
      {
        "id": 1,
        "name": "Laptop X1",
        "description": "High-performance laptop",
        "price": 1200,
        "category": "electronics",
        "score": 3
      },
      {
        "id": 2,
        "name": "Tablet Pro",
        "description": "Lightweight and powerful",
        "price": 800,
        "category": "electronics",
        "score": 2
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
  URL parameter: `user_id=1`.
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

### **5. Feedback-Enhanced Recommendations**
- The **recommendation engine** adjusts product scores based on feedback.
- Products with higher average ratings are ranked higher in recommendations.

---

## **Summary**

- **User Management**: Handles user registration, preferences, and retrieval.
- **Product Management**: Allows adding and listing products.
- **Recommendation Engine**: Matches user preferences with products and ranks them based on scores and feedback.
- **Feedback System**: Collects user ratings and comments to refine recommendations.

---