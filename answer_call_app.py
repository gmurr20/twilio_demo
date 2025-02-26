from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

voice_cfg = "Google.en-US-Standard-G"

app = Flask(__name__)

@app.route("/intro", methods=['GET', 'POST'])
def intro():
    resp = VoiceResponse()
    resp.say('Thank you for calling my restaurant!', voice=voice_cfg)
    resp.redirect('/answer')
    return str(resp)

@app.route("/answer", methods=['GET', 'POST'])
def answer():
    """Respond to incoming phone calls."""
    resp = VoiceResponse()

    gather = Gather(num_digits=1, action='/choice', timeout=60)
    gather.say('Please press 1 for reservations, 2 to place a delivery or takeout order, 3 for hours, or 4 to talk to the host. To repeat this message press 5.', voice=voice_cfg)
    resp.append(gather)

    return str(resp)


@app.route("/choice", methods=['GET', 'POST'])
def menu():
    choice = request.form['Digits']
    resp = VoiceResponse()

    if choice == '1':  # Reservations
        resp.say("Please go to Open table to place a reservation. We also accept walk-ins at a first come first serve basis. Thank you!", voice=voice_cfg)
        resp.redirect("/follow_up", voice=voice_cfg)
    elif choice == '2':  # Takeout Orders
        resp.say("Please go to our website to place a takeout order.", voice=voice_cfg)
        resp.redirect("/follow_up", voice=voice_cfg)
    elif choice == '3':  # Hours
        resp.say("We are open from 10 am to 2 pm for lunch and 5 pm to 10 pm for dinner Tuesday through Sunday. We are closed on Monday.", voice=voice_cfg)
        resp.redirect("/follow_up", voice=voice_cfg)
    elif choice == '4':  # Host
        resp.say("Please stay on the line while we connect you the host.", voice=voice_cfg)
        resp.dial('+16305555555')
    elif choice == '5':  # Repeat
        resp.redirect("/answer", voice=voice_cfg)
    else:
        resp.say("Sorry, I didn't understand.", voice=voice_cfg)
        resp.redirect("/answer")

    return str(resp)

@app.route("/follow_up", methods=['GET', 'POST'])
def follow_up():
    resp = VoiceResponse()
    resp.say('Anything else I could help with?', voice=voice_cfg)
    resp.redirect('/answer')
    return str(resp)

if __name__ == "__main__":
    app.run(port=5005, debug=True)
