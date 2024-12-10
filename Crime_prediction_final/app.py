from flask import Flask, request, render_template
import joblib
import math
from twilio.rest import Client  # Import Twilio for SMS alerts

# Load the model using joblib
model = joblib.load('Model/model.pkl')

app = Flask(__name__)

# Your Twilio credentials (replace these with your actual credentials)
#this details are random make your twilio account and enter them below(***details enteres here are random***)
account_sid = 'e1db698da439062f7e6f287958aa'
auth_token = '38ea0291226de87d236ae'
client = Client(account_sid, auth_token)

# City and crime details (same as before)
city_names = {
    '0': 'Andheri', '1': 'Dadar', '2': 'Borivali', '3': 'Kurla', 
    '4': 'Ghatkopar', '5': 'Malad', '6': 'Goregaon', '7': 'Powai', 
    '8': 'Chembur', '9': 'Sion', '10': 'Juhu', '11': 'Airoli', 
    '12': 'Vashi', '13': 'Colaba', '14': 'Thane', '15': 'Panvel', 
    '16': 'Byculla', '17': 'Wadala', '18':'Parel'
}

crimes_names = {
    '0': 'Crime Committed by Juveniles', '1': 'Crime against SC', 
    '2': 'Crime against ST', '3': 'Crime against Senior Citizen', 
    '4': 'Crime against children', '5': 'Crime against women', 
    '6': 'Cyber Crimes', '7': 'Economic Offences', '8': 'Kidnapping', 
    '9':'Murder'
}

population = {
    '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10, 
    '5': 23.60, '6': 77.50, '7': 21.70, '8': 30.70, '9': 29.20, 
    '10': 21.20, '11': 141.10, '12': 20.30, '13': 29.00, '14': 184.10, 
    '15': 25.00, '16': 20.50, '17': 50.50, '18': 45.80
}

# Function to send SMS alert if crime rate is high
def send_sms_alert(city, crime_rate):
    message_body = f"Crime Alert: High crime rate predicted in {city}. Estimated crime rate: {crime_rate}"

    try:
        message = client.messages.create(
            body=message_body,
            from_= '+1---------',  # Your Twilio phone number
            to= '+91----------'     # Recipient's phone number
            
        )
        return f"SMS sent successfully: {message.sid}"
    except Exception as e:
        return f"SMS failed to send: {e}"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict_result():
    city_code = request.form["city"]
    crime_code = request.form['crime']
    year = request.form['year']
    pop = population[city_code]

    # Adjust population based on the year
    year_diff = int(year) - 2011
    pop = pop + 0.01 * year_diff * pop

    # Predict the crime rate
    crime_rate = model.predict([[year, city_code, pop, crime_code]])[0]

    city_name = city_names[city_code]
    crime_type = crimes_names[crime_code]

    # Determine crime status based on crime rate
    if crime_rate <= 1:
        crime_status = "Very Low Crime Area"
    elif crime_rate <= 5:
        crime_status = "Low Crime Area"
    elif crime_rate <= 15:
        crime_status = "High Crime Area"
    else:
        crime_status = "Very High Crime Area"

    # Send SMS alert if crime rate is high and get SMS status message
    sms_status = ""
    if crime_rate > 1:
        sms_status = send_sms_alert(city_name, crime_rate)
    else:
        sms_status = "No SMS sent, crime rate below threshold."

    # Calculate the number of cases
    cases = math.ceil(crime_rate * pop)

    return render_template(
        'result.html',
        city_name=city_name,
        crime_type=crime_type,
        year=year,
        crime_status=crime_status,
        crime_rate=crime_rate,
        cases=cases,
        population=pop,
        sms_status=sms_status  # Pass SMS status to the template
    )

if __name__ == '__main__':
    app.run(debug=False)
