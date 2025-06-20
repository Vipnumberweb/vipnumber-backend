import random
import requests

def generate_otp():
    return str(random.randint(100000, 999999))

def send_sms_otp(mobile, otp):
    api_key = "4f7a69d4-35f3-4c1e-a43a-e0a6203e18bd"
    message = f"Your OTP is {otp}"
    url = f"https://teleduce.corefactors.in/sendsms/?key={api_key}&text={message}&route=0&from=CORFCT&to={mobile}"
    try:
        response = requests.get(url)
        return response.status_code == 200
    except Exception:
        return False