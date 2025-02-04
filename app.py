from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "12345"  # Set this to match what you entered in the Facebook Developer Console

@app.route("/", methods=["GET"])
def webhook_verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200  # Respond with the challenge to verify
    else:
        return "Verification failed", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
