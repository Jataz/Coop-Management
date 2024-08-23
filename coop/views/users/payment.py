from paynow import Paynow  # Import the Paynow class

def charge_customer(data):
    try:
        # Validate required fields
        required_fields = ['mobile_number', 'amount']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # Validate types
        if not isinstance(data['amount'], (int, float)):
            raise ValueError("amount must be a number")

        # Hard-coded Paynow Integration details
        integration_id = 19095
        integration_key = 'bfaf70ac-8493-4abd-a640-d2099ff3df13'
        update_url = 'http://example.com/gateways/paynow/update'  # Replace with your actual update URL
        return_url = 'http://example.com/return?gateway=paynow'   # Replace with your actual return URL

        # Initialize Paynow instance
        paynow = Paynow(
            integration_id,
            integration_key,
            update_url,
            return_url
        )

        # Create payment
        payment = paynow.create_payment('REF-45', 'africafreedom17@gmail.com')
        payment.add('Registration Fee', data['amount'])  # Adjust item name accordingly

        # Send payment
        response = paynow.send_mobile(payment, data['mobile_number'], 'ecocash')

        success = response.success  # Access success as an attribute, not a method
        poll_url = response.poll_url if success else None

        if success:
            # Return success message and poll URL
            return {'success': 'Payment initiated successfully', 'poll_url': poll_url}
        else:
            # Return error message for unsuccessful payment
            return {'error': 'Payment unsuccessful. Please try again.'}

    except ValueError as e:
        return {'error': str(e)}
