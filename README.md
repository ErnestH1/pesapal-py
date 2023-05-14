# PesaPal

This README file provides instructions on how to set up and use the PesaPal code for integrating with the PesaPal payment gateway. It includes steps for cloning the repository, installing necessary modules, and running the `app.py` file.

## Setup

Follow the steps below to set up and use the PesaPal code:

1. Clone the repository:
   ```
   git clone git@github.com:ErnestH1/pesapal-py.git
   ```

2. Navigate to the `app.py` file:
   ```
   cd pesapal-py
   ```

3. Install the necessary modules:
   ```
   pip install base64 hmac hashlib jwt json requests urllib.parse
   ```

4. Run the `app.py` file:
   ```
   python app.py or python3 app.py
   ```

## Code Details

The provided code is a Python class named `pesapal-py` that encapsulates the functionality for authenticating against PesaPal and generating the required JWT token for API authentication. It also includes a method for retrieving an iframe from PesaPal.

### Authentication

The `authenticate` method authenticates against PesaPal using the provided consumer key and consumer secret. It returns a dictionary with the following keys:

- `status`: Indicates whether the authentication was successful or failed.
- `error` (optional): Error message from PesaPal when authentication fails.
- `message` (optional): A brief description about the response received.
- `token` (optional): Bearer token to authenticate all other PesaPal APIs.
- `expiry` (optional): Date and time the token will expire.

### JWT Token Generation

The `generate_jwt_signature` method generates a JWT token for authentication. It takes the HTTP method, endpoint, parameters, and secret key as inputs and returns the JWT token.

### Signature Building

The `build_signature` method builds the signature required for making API calls to PesaPal. It takes the request, consumer, parameters, and token as inputs and returns the signature.

### Retrieving an iframe

The `get_iframe` method retrieves an iframe from PesaPal. It takes a token as input and returns a dictionary with the response content.

## Author

The code in this repository was written by Ernest Hanson.

## License

The code in this repository is licensed under the MIT license.