from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your bank's API endpoint for initiating transfers
TRANSFER_URL = 'https://standardbank.com/transfer'

# Replace 'your_client_id' and 'your_secret' with your actual bank API credentials
CLIENT_ID = '24208070'
SECRET = 'i3peel1sar694'

# Integrated bank amount
INTEGRATED_AMOUNT = 20000  # Example amount, you can change it as needed


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/transfer', methods=['POST'])
def transfer_money():
    recipient_account_number = request.form.get('recipient_account')
    account_holder = request.form.get('account_holder')
    bank_name = request.form.get('bank_name')
    branch_name = request.form.get('branch_name')
    account_type = request.form.get('account_type')
    swift_code = request.form.get('swift_code')

    if not all([recipient_account_number, account_holder, bank_name, branch_name, account_type, swift_code]):
        return "Please fill out all fields", 400

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CLIENT_ID}:{SECRET}'
    }

    payload = {
        'recipient_account': recipient_account_number,
        'recipient_name': account_holder,
        'amount': INTEGRATED_AMOUNT,
        'purpose': 'Received as a Gift From DesignX'
    }

    try:
        response = requests.post(TRANSFER_URL, json=payload, headers=headers)
        if response.status_code == 200:
            return 'Transfer successful!'
        else:
            return f'Transfer failed with status code: {response.status_code}\n{response.text}', 500
    except Exception as e:
        return f'An error occurred: {e}', 500


if __name__ == '__main__':
    app.run(debug=True)

