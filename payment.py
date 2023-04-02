from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe, os

app = Flask(__name__)
CORS(app)
stripe.api_key = os.environ.get('stripeKey')

@app.route('/payment', methods=['POST'])
def payment():
  try:
    data = request.get_json() 
    print("Data from JS:", data)

    # Set correct price amount for Stripe
    price = int(float(data['TotalPrice'])*100)
    print("Price:", price)

    print("--Stripe Create Checkout Session--")
    session = stripe.checkout.Session.create(
      line_items=[{
        'price_data': {
          'currency': 'sgd',
          'product_data': {
            'name': 'Healthcare Services & Medication',
          },
          'unit_amount': price,
        },
        'quantity': 1,
      }],
      mode='payment',
      success_url='http://127.0.0.1:5100/success?session_id={CHECKOUT_SESSION_ID}',
      cancel_url='http://127.0.0.1:5100/',
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
    return jsonify({"status": "error"}),500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)