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

# 🔥 estado global (en Render es temporal, pero funciona para esto)
current_scene = 0

scenes = [
    {"r": 0, "g": 0, "b": 255, "bri": 100},   # gaming
    {"r": 255, "g": 200, "b": 150, "bri": 70}, # cuarto cami
    {"r": 255, "g": 80, "b": 0, "bri": 10},    # dormir
]


def set_light(device, r, g, b, bri):
    url = "https://openapi.api.govee.com/router/api/v1/device/control"

    rgb_value = (r << 16) + (g << 8) + b  # conversión a int

    payload_rgb = {
        "requestId": "nfc-render",
        "device": device,
        "model": "H6008",
        "cmd": {
            "name": "colorRgb",
            "value": rgb_value
        }
    }

    payload_bri = {
        "requestId": "nfc-render",
        "device": device,
        "model": "H6008",
        "cmd": {
            "name": "brightness",
            "value": bri
        }
    }

    requests.post(url, json=payload_rgb, headers=headers)
    requests.post(url, json=payload_bri, headers=headers)


# ---------------- NFC 1: ROTAR ESCENAS ----------------

@app.route("/next")
def next_scene():
    global current_scene

    scene = scenes[current_scene]

    for d in devices:
        set_light(d, scene["r"], scene["g"], scene["b"], scene["bri"])

    current_scene = (current_scene + 1) % len(scenes)

    return f"Scene {current_scene} activated"


# ---------------- NFC 2: OFF ----------------

@app.route("/off")
def off():
    for d in devices:
        set_light(d, 0, 0, 0, 0)

    return "All OFF"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)