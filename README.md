# Personalized-Recommendation-System

<img width="50" height="20" alt="logo" src="https://github.com/user-attachments/assets/e841450b-f66c-4692-8335-79165065a2eb" /> ***TrendMatrix***

**TrendMatrix** is a personalized recommendation web app built with **Python and Streamlit**.
It demonstrates how real-world recommendation systems handle personalization, cold-start users, and UI robustness in a deployable application.

---

## ✨ Features

* Content-based recommendations using item metadata
* Cold-start handling with trending items
* Explainable sections
* Robust image and UI fallback handling
* Modular UI with HTML & CSS
* PostgreSQL-ready backend

---

## 🧠 Recommendation Logic

* Item similarity computed using **TF-IDF + cosine similarity**
* User interactions influence ranking over time
* Balanced relevance and diversity to avoid repetition

---

## 🗂 Project Structure

trendmatrix/
│
├── app.py                     
├── recommender.py             
├── db.py                      
├── requirements.txt
├── README.md
│
├── data/
│   └── items.csv              
│
├── ui/
│   ├── components.py          
│   ├── card.html
│   └── styles.css             
│
├── assets/
│   ├── logo.png
│   └── images/
│
└── .streamlit/
    └── secrets.toml

---

## 🚀 Run Locally

 **Clone the repository**
```bash
git clone https://github.com/Akshu121796/trendmatrix.git
cd trendmatrix
```
**Install dependencies**
```
pip install -r requirements.txt
```
**Run the server**
```
streamlit run app.py
```

---

## 🛠 Tech Stack

Python
• Streamlit
• TF-IDF 
• PostgreSQL 
• HTML 
• CSS

---
