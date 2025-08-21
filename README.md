# Food Donation Management & Analysis Web App

This project is a web application for managing, analyzing, and distributing surplus food donations. It connects food providers (restaurants, grocery stores, supermarkets) with receivers (NGOs, community centers, individuals) to minimize food wastage and ensure timely distribution.

***The application provides***:

- SQL-powered insights into food donations and claims.
- A user-friendly Streamlit interface to visualize and filter data.
- CRUD operations to manage food listings and claims in real-time.
- Contact details for providers and receivers to facilitate coordination.

## Features

**Data Analysis**

- Track food providers and receivers by city.
- Identify the most frequent contributors and popular food types.
- Monitor claim status (completed, pending, cancelled) and food wastage trends.

**Streamlit Web Interface**
- Display results of 15 pre-defined SQL queries.
- Filter data by city, provider, food type, and meal type.
- Show contact information of providers and receivers.
- Add, update, or remove food listings and claims (CRUD operations).

**Database Management**

- SQL database stores all provider, receiver, food, and claim data.
- Queries retrieve insights and generate reports for effective distribution.


**Installation**
1. Clone the repository:
```
git clone https://github.com/your-username/food-donation-app.git
cd food-donation-app
```

2. Install dependencies:
```
pip install -r requirements.txt
```


3. Run the app:
```
streamlit run app.py
```


**Usage**
- Launch the Streamlit app to access the dashboard.
- Use filters to view food listings by city, provider, food type, or meal type.
- View contact info to coordinate food distribution.
- Perform CRUD operations to update food listings or claims.
- View SQL-based reports and insights directly on the interface.

**Technologies Used**
- Python – Backend logic and Streamlit interface
- Streamlit – Interactive web app framework
- SQL (SQLite/PostgreSQL/MySQL) – Database management
- Pandas – Data handling and preprocessing

**Project Goals**
- Reduce food wastage by improving coordination between providers and receivers.
- Provide real-time insights into food availability and demand.
- Enable easy management of food donations and claims.
