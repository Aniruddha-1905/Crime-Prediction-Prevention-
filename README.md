# Crime Rate Predictor with SMS Alerts

This project is a **Crime Rate Predictor** that uses a **Random Forest Regression Model** to predict crime rates in 19 metropolitan cities in India. It provides predictions for 10 different crime categories based on input parameters like year, city, and crime type. The project also features **real-time SMS alerts** to notify stakeholders if the predicted crime rate is high.

---

## Features

- Predicts crime rate and provides estimated number of cases.
- Uses a **Random Forest Regression** model for predictions.
- Accepts input for:
  - **Year** (2000–2050)
  - **City** (19 metropolitan cities in India)
  - **Crime Type** (10 categories, e.g., Murder, Kidnapping, Cyber Crimes, etc.)
- Dynamically adjusts population based on the year.
- Sends **real-time SMS alerts** for high crime rate predictions using **Twilio API**.
- Web interface for user interaction.

---

## Project Structure

```plaintext
.
├── Model/
│   └── model.pkl               # Pre-trained Random Forest Regression model
├── static/
│   ├── images/
│   │   └── favicon.png         # Favicon image
│   ├── styles.css              # Styling for the web application
│   └── main.js                 # JavaScript for dynamic dropdown
├── templates/
│   ├── index.html              # Input form for prediction
│   └── result.html             # Display prediction results
├── app.py                      # Flask application
├── README.md                   # Project documentation
├── Report_Sem7.pdf             # Detailed project report
└── requirements.txt            # List of Python dependencies
