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
    speech_text = ''
    display_text = ''
    if reg:
        speech_text += reg + '. '
        display_text += reg + '\n'
        intent = EnquiryIntent()
        result = intent.execute(reg)
        if result['make']:
            speech_text += result['make'] + '. '
            display_text += result['make'] + ' '
        if result['colour']:
            speech_text += result['colour'] + '. '
            display_text += '(' + result['colour'] + ')'
        display_text += '\n'
        if result['tax']['unknown'] and result['mot']['unknown']:
            speech_text += 'Could not find any details for this vehicle. '
            display_text += '? Vehicle\n'
        else:
            if result['tax']['unknown']:
                speech_text += 'Could not find any tax details for this vehicle. '
                display_text += '? Tax\n' + result['tax']['text'] + '\n'
            else:
                if result['tax']['valid']:
                    speech_text += 'This vehicle is taxed. '
                    display_text += '✓ Taxed\n'
                else:
                    speech_text += 'The tax for this vehicle is overdue. '
                    display_text += '✗ Untaxed\n'
                speech_text += result['tax']['text'] + ' '
                display_text += result['tax']['text'] + '\n'
            if result['mot']['unknown']:
                speech_text += 'Could not find any MOT details for this vehicle. '
                display_text += '? MOT\n' + result['mot']['text'] + '\n'
            else:
                if result['mot']['valid']:
                    speech_text += 'This vehicle has a valid M. O. T. '
                    display_text += '✓ MOT\n'
                else:
                    speech_text += 'The M. O. T. for this vehicle is overdue. '
                    display_text += '✗ No MOT\n'
                speech_text += result['mot']['text'] + ' '
                display_text += result['mot']['text'] + '\n'
    else:
        speech_text = 'Registration not supplied.'
    return statement(speech_text).simple_card(TITLE, display_text)

if __name__ == '__main__':
    app.run()