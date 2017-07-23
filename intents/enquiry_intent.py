import requests
from pyquery import PyQuery

CONFIRM_URL = 'https://vehicleenquiry.service.gov.uk/ConfirmVehicle'
VIEW_URL = 'https://vehicleenquiry.service.gov.uk/ViewVehicle'

class EnquiryIntent:
    def execute(self, vrm):
        confirm_data = {
            'Vrm': vrm,
            'Continue': ''
        }
        confirm_response = requests.post(url=CONFIRM_URL, data=confirm_data).content
        html = PyQuery(confirm_response)
        form = html('form[action="/ViewVehicle"]')
        view_state = form('#viewstate').attr('value')
        make = form('#Make').attr('value')
        colour = form('#Colour').attr('value')
        view_data = {
            'viewstate': view_state,
            'Vrm': vrm,
            'Make': make,
            'Colour': colour,
            'Correct': 'True',
            'Continue': ''
        }
        view_response = requests.post(url=VIEW_URL, data=view_data).content
        html = PyQuery(view_response)
        tax = html('.status-bar > div').eq(0)
        tax_valid = tax('.isValid')
        tax_valid_text = tax_valid('p').text()
        tax_valid_valid = bool(tax_valid.length)
        response = {
            'tax': {
                'text': tax_valid_text,
                'valid': tax_valid_valid
            }
        }
        print(response)
        return response