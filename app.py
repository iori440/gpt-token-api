from flask import Flask, jsonify
import jwt
import time
import os
import requests

app = Flask(__name__)

# === サービスアカウント情報は環境変数から取得 ===
CLIENT_EMAIL = os.getenv("CLIENT_EMAIL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY").replace("\\n", "\n")
TOKEN_URI = os.getenv("TOKEN_URI", "https://oauth2.googleapis.com/token")

@app.route("/get-token", methods=["GET"])
def get_token():
    issued_at = int(time.time())
    expiration_time = issued_at + 3600

    payload = {
        "iss": CLIENT_EMAIL,
        "scope": "https://www.googleapis.com/auth/cloud-platform",
        "aud": TOKEN_URI,
        "iat": issued_at,
        "exp": expiration_time,
    }

    signed_jwt = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "assertion": signed_jwt,
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer"
    }

    response = requests.post(TOKEN_URI, headers=headers, data=data)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
