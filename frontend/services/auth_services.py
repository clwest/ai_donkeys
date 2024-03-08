import os
import requests

def signup_user(email, username, password):
    # Construct the payload with the user details
    payload = {
        "email": email,
        "username": username,
        "password": password
    }

    # URL of the Flask backend's register endpoint
    url = f"{os.getenv('FLASK_URL')}/users/register"

    try:
        # Send a POST request to the Flask backend
        response = requests.post(url, json=payload)

        # Check if the request was successful
        if response.status_code == 201:
            # Registration was successful
            print("Registration successful.")
            
            # Extracting the JSON response which contains the access_token
            data = response.json()
            access_token = data.get('access_token')
            print("Access Token:", access_token)

            # Use the access_token as needed, save it for future requests
            return {"success": True, "access_token": access_token }
        else:
            # Handling cases where the server response with an error
            return {"success": False, "message": "Registration failed. Please try again"}

    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        print(f"An error occurred: {e}")
        return {"success": False, "message": str(e)}

def login_user(username, password):
    payload = {
        "username": username,
        "password": password          
    }
    # URL of the Flask backend's login endpoint
    url = f"{os.getenv('FLASK_URL')}/users/login"
    try:
        response = requests.post(url, json=payload)
        if response.status_code in [200, 201]:
            data = response.json()
            # print(f"log in data: {data}")
            return {"success": True, "token": data.get("access_token"), "username": data.get("user").get("username")}
        else:
            return {"success": False, "message": "Login failed. Please try again."}
    except Exception as e:
        return {"success": False, "message": str(e)}
