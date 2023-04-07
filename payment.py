from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe, os, json 

app = Flask(__name__)
CORS(app)
stripe.api_key = os.environ.get('stripeKey')
successURL = os.environ.get('successUrl')
cancelURL = os.environ.get('cancelUrl')

@app.route('/payment', methods=['POST'])
def payment():
  try:
    data = request.get_json() 
    print("Data from JS:", data)

    # Get appointment id
    appointment_id = data['appointment_id']
    print("Appointment ID:", appointment_id)

    # Create list of all medicines (if any) and services
    medicineService = []
    if "medicines" in data:
      medicineData = data["medicines"]
      if isinstance(data["medicines"], str): # Check if pass as JSON or string
         medicineData = json.loads(data["medicines"])
      for medicine in medicineData:
          medicine_name = medicine['medicineName']
          medicine_price = int(float(medicine["price"]["$numberDecimal"]) * 100)
          medicine_quantity = medicine["quantity"]
          medicineService.append({
              'price_data': {
                'currency': 'sgd',
                'product_data': {
                  'name': medicine_name,
                },
                'unit_amount': medicine_price,
              },
              'quantity': medicine_quantity,
          })

    serviceData = data["services"]
    if isinstance(data["services"], str): # Check if pass as JSON or string
        serviceData = json.loads(data["services"])
    for service in serviceData:
        service_name = service["serviceName"]
        service_price = int(float(service["price"]["$numberDecimal"]) * 100)
        medicineService.append({
            'price_data': {
              'currency': 'sgd',
              'product_data': {
                'name': service_name,
              },
              'unit_amount': service_price,
            },
            'quantity': 1,
        })

    print("Verify list of medicines & services:", medicineService)

    print("--Stripe Create Checkout Session--")
    session = stripe.checkout.Session.create(
      metadata={
       "appointment_id": appointment_id
      },
      line_items=medicineService,
      mode='payment',
      success_url= successURL + '?session_id={CHECKOUT_SESSION_ID}',
      cancel_url = cancelURL
    )

    print("Generated Payment Link:", session.url)
    
    return jsonify(
      {
          "code": 200,
          "link": session.url,
          "message": "Payment Link Generated."
      }
    ), 200
  
  except Exception as e:
    print(f"An Error Occurred: {e}")
    return jsonify({"code": 500, "status": "Error generating payment link"}),500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)