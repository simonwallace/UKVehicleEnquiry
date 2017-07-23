from flask import Flask
from flask_ask import Ask, statement
from intents.enquiry_intent import EnquiryIntent

app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('Enquiry')
def enquiry(enquiry_type, vehicle, validity, reg_one, reg_two, reg_three,
            reg_four, reg_five, reg_six, reg_seven):
    reg = reg_one + reg_two + reg_three + reg_four + reg_five + reg_six + reg_seven
    intent = EnquiryIntent()
    result = intent.execute(reg)
    speech_text = "{} {} {} {} - {} {}".format(enquiry_type, vehicle, validity, reg,
                                               result['tax']['valid'],
                                               result['tax']['text'])
    return statement(speech_text).simple_card('Hello', speech_text)

if __name__ == '__main__':
    app.run()