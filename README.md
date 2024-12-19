# **MentalHealthCounsellor**

The **MentalHealthCounsellor** is a web application built using **Streamlit**, designed to provide mental health-related responses and stress predictions. It integrates advanced machine learning models and the **Llama-3.3-70b Versatile** model to offer helpful insights. The application has two core functionalities:

1. **Mental Health Counselling (via Llama-3.3-70b Versatile Model)**
2. **Stress Level Prediction (via Machine Learning Models)**

---

## **Features**

### **1. Mental Health Counselling (Chatbot)**
- The chatbot uses the **Llama-3.3-70b Versatile** model to provide therapeutic responses.
- A custom dataset consisting of questions and answers from real therapists is stored in a **ChromaDB** vector database.
- When a user inputs a question, the app performs a semantic search through the database to retrieve relevant responses.
- Based on the retrieved data, the **Llama model** generates a contextual and helpful reply.

### **2. Stress Level Prediction**
- This feature predicts the user's stress level based on personal details like age, gender, occupation, sleep patterns, and more.
- The dataset used for training is sourced from Kaggle.
- The data goes through cleaning and preprocessing before training with three models:
  - **Logistic Regression** (54% accuracy)
  - **Random Forest** (87% accuracy)
  - **Decision Tree** (97% accuracy)
- The **Decision Tree** model (with 97% accuracy) is then pickled and used for predictions in the app.
- Users can enter their details through a form in the app, and it will predict their stress level ranging from **Low** to **High**.

---

## **Tech Stack**
- **Frontend**: Streamlit
- **Backend**: Python
- **Machine Learning**: scikit-learn, Decision Tree, Random Forest, Logistic Regression
- **Natural Language Processing**: Llama-3.3-70b Versatile model
- **Database**: ChromaDB (for vector storage)
- **Deployment**: Linux-based servers (via shell script)

---

## **Installation**

### **Prerequisites**
- Python 3.8 or higher
- Required Python libraries:
  - `streamlit`
  - `pandas`
  - `numpy`
  - `scikit-learn`
  - `chromadb`
  - `joblib`
  - `llama-index`
  - `transformers`
  - Other dependencies listed in `requirements.txt`

### **Step-by-Step Guide**

1. **Clone the Repository**:
   git clone "repo link here"
   cd directory name

2. **Follow the Shell Script**