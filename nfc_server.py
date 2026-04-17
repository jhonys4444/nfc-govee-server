from flask import Flask
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("GOVEE_API_KEY")

headers = {
    "Govee-API-Key": API_KEY,
    "Content-Type": "application/json"
}

devices = [
    "6D:78:98:17:3C:6F:29:90",
    "89:95:98:17:3C:6F:FE:10",
    "96:05:98:17:3C:6F:0E:2E",
    "8C:57:98:17:3C:6F:FD:E4"
]

def set_light(device, state):
    url = "https://openapi.api.govee.com/router/api/v1/device/control"

    payload = {
        "requestId": "nfc-render",
        "payload": {
            "sku": "H6008",
            "device": device,
            "capability": {
                "type": "devices.capabilities.on_off",
                "instance": "powerSwitch",
                "value": 1 if state else 0
            }
        }
    }

    requests.post(url, json=payload, headers=headers)

@app.route("/cuarto_cami")
def cuarto_cami():
    for d in devices:
        set_light(d, 1)
    return "Cuarto Cami ON"

@app.route("/dormir")
def dormir():
    for d in devices:
        set_light(d, 0)
    return "Dormir ON"

@app.route("/gaming")
def gaming():
    for d in devices:
        set_light(d, 1)
    return "Gaming ON"

if __name__ == "__main__":
    app.run()