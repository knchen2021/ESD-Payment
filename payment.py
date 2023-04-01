from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import stripe

app = Flask(__name__)
CORS(app)
stripe.api_key = "sk_test_51MreNMAJME9DYeVIWdJQlEC35AwfQT9DVuYXzRdm4932kqOtDODFgqTazUHW4zf2vi7E9aebX1POK5YM4qeYGSoz0018UpgOD8"

@app.route('/')
def index():
  return render_template('index.html')

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
      success_url='http://127.0.0.1:5000/success',
      cancel_url='http://127.0.0.1:5000/',
    )
    
    print("Generated Payment Link:", session.url)
    
    return jsonify({"link": session.url})
  
  except Exception as e:
    print(f"An Error Occurred: here {e}")
    return jsonify({"status": "error"}),500
  
@app.route('/success')
def success():
  print("--Payment Completed!--")
  return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)