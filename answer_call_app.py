from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

@app.route("/twilio", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls."""
    resp = VoiceResponse()

    gather = Gather(num_digits=1, action='/gather')
    gather.say('Thank you for calling Greg\'s test server. Please press 1 for these hands, or 2 for support.')
    resp.append(gather)

    return str(resp)

@app.route("/gather", methods=['GET', 'POST'])
def gather():
    """Processes the caller's input."""
    choice = request.form['Digits']
    resp = VoiceResponse()

    if choice == '1':
        resp.say('Connecting you to these hands rated E for everyone.')
        # Add TwiML to connect to sales
    elif choice == '2':
        resp.say('Connecting you to support.')
        # Add TwiML to connect to support
    else:
        resp.say('Invalid choice.')
        resp.redirect('/twilio') #restart the process.

    return str(resp)

if __name__ == "__main__":
    app.run(port=5005, debug=True)
