from flask import Flask, request, jsonify, send_from_directory, abort
import pyautogui, os, platform, subprocess, time


SECRET_TOKEN = "nathan321"
HOST = "0.0.0.0"
PORT = 5050
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=os.path.join(ROOT_DIR, "static"))

def require_token():
    token = request.args.get("token")
    if token != SECRET_TOKEN:
        abort(401)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "mobile_ui.html")

@app.route("/api/ping")
def ping():
    require_token()
    return jsonify({"ok": True, "time": time.ctime()})

@app.route("/api/mouse/rel", methods=["POST"])
def mouse_rel():
    require_token()
    data = request.json or {}
    dx = data.get("dx", 0)
    dy = data.get("dy", 0)
    pyautogui.moveRel(dx, dy)
    return jsonify({"ok": True})

@app.route("/api/mouse/click", methods=["POST"])
def mouse_click():
    require_token()
    data = request.json or {}
    btn = data.get("button", "left")
    pyautogui.click(button=btn)
    return jsonify({"ok": True})

@app.route("/api/keyboard/type", methods=["POST"])
def keyboard_type():
    require_token()
    data = request.json or {}
    text = data.get("text", "")
    pyautogui.typewrite(text)
    return jsonify({"ok": True})

@app.route("/api/keyboard/press", methods=["POST"])
def keyboard_press():
    require_token()
    key = (request.json or {}).get("key")
    if not key:
        return jsonify({"error": "key required"}), 400
    pyautogui.press(key)
    return jsonify({"ok": True})

@app.route("/api/screenshot")
def screenshot():
    require_token()
    img = pyautogui.screenshot()
    path = os.path.join(ROOT_DIR, "screenshot.png")
    img.save(path)
    return send_from_directory(ROOT_DIR, "screenshot.png")

@app.route("/api/shutdown", methods=["POST"])
def shutdown():
    require_token()
    subprocess.Popen(["shutdown", "/s", "/t", "5"])
    return jsonify({"ok": True, "msg": "Laptop akan mati dalam 5 detik"})

if __name__ == "__main__":
    print(f"Server berjalan di http://localhost:{PORT}")
    print(f"Token: {SECRET_TOKEN}")
    app.run(host=HOST, port=PORT, debug=False)