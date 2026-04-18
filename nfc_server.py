from flask import Flask
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("GOVEE_API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

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

def set_light(state):
    url = "https://openapi.api.govee.com/router/api/v1/device/control"

    for device in devices:
        payload = {
            "requestId": "nfc",
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


@app.route("/on/<token>")
def on(token):
    if token != SECRET_KEY:
        return "unauthorized", 403

    set_light(1)
    return "ON OK"


@app.route("/off/<token>")
def off(token):
    if token != SECRET_KEY:
        return "unauthorized", 403

    set_light(0)
    return "OFF OK"


if __name__ == "__main__":
    app.run()