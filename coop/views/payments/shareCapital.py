import logging
import uuid
from paynow import Paynow  # Import the Paynow class

# Set up logging
logger = logging.getLogger(__name__)


def process_payment(data):
    try:
        # Validate required fields
        required_fields = ['mobile_number', 'amount']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # Validate amount type
        if not isinstance(data['amount'], (int, float)):
            raise ValueError("amount must be a number")

        # Generate a unique reference for the payment
        payment_reference = generate_unique_reference()
        customer_email = 'africafreedom17@gmail.com'  # Adjust as necessary

        # Hard-coded Paynow Integration details
        integration_id = 19095
        integration_key = 'bfaf70ac-8493-4abd-a640-d2099ff3df13'
        update_url = 'http://example.com/gateways/paynow/update'  # Replace with actual URL
        return_url = 'http://example.com/return?gateway=paynow'   # Replace with actual URL

        # Initialize Paynow instance
        paynow = Paynow(
            integration_id,
            integration_key,
            update_url,
            return_url
        )

        # Create payment
        payment = paynow.create_payment(payment_reference, customer_email)
        payment.add('Subscripstion Payment', data['amount'])

        # Log the payment creation details
        logger.info(f"Payment created: Reference {payment_reference}, Amount {data['amount']}")

        # Send payment
        response = paynow.send_mobile(payment, data['mobile_number'], 'ecocash')

        # Log the response details
        logger.info(f"Payment response: {response}")

        success = response.success  # Ensure this is a boolean attribute
        poll_url = response.poll_url if success else None

        if success:
            return {'success': True, 'poll_url': poll_url}
        else:
            return {'error': 'Payment unsuccessful. Please try again.'}

    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        return {'error': str(e)}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {'error': 'An unexpected error occurred.'}
    
def generate_unique_reference():
    # Option 1: Using UUID
    unique_id = str(uuid.uuid4())
    return f"REF-{unique_id}"

    # Option 2: Using Timestamp and Random Number
    # timestamp = int(time.time() * 1000)  # Current time in milliseconds
    # random_number = random.randint(1000, 9999)  # Random number to ensure uniqueness
    # return f"REF-{timestamp}-{random_number}"

    # Option 3: Combining UUID and Timestamp
    # timestamp = int(time.time() * 1000)  # Current time in milliseconds
    # unique_id = str(uuid.uuid4())  # UUID for additional uniqueness
    # return f"REF-{timestamp}-{unique_id}"
