from flask import Flask, request, jsonify, render_template, redirect, session
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
  data = request.get_json()
  session = stripe.checkout.Session.create(
    line_items=[{
      'price_data': {
        'currency': 'sgd',
        'product_data': {
          'name': 'Healthcare Services & Medication',
        },
        'unit_amount': data['TotalPrice'],
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url='http://127.0.0.1:5000/success',
    cancel_url='http://127.0.0.1:5000/',
  )

  return redirect(session.url, code=303)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)