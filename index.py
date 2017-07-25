from flask import Flask
from flask_ask import Ask, statement
from intents.enquiry_intent import EnquiryIntent
from utilities.phonetic import Phonetic

TITLE = 'UK Vehicle Enquiry'

app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('Enquiry')
def enquiry(subject, vehicle, validity, reg_i, reg_ii, reg_iii, reg_iv, reg_v, reg_vi, reg_vii):
    phonetic = Phonetic()
    reg_list = [reg_i, reg_ii, reg_iii, reg_iv, reg_v, reg_vi, reg_vii]
    reg_list = phonetic.from_phonetic_or_value(reg_list)
    reg = ''.join(filter(None, reg_list)).upper()
    speech_text = 'Registration not supplied'
    if reg:
        intent = EnquiryIntent()
        result = intent.execute(reg)
        speech_text = "{} {} {} {} - {} {} - {} {}".format(subject, vehicle, validity, reg,
                                                           result['tax']['valid'],
                                                           result['tax']['text'],
                                                           result['mot']['valid'],
                                                           result['mot']['text'])
    return statement(speech_text).simple_card(TITLE, speech_text)

if __name__ == '__main__':
    app.run()