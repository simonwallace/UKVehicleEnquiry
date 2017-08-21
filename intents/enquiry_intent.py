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
        response = {
            'colour': colour,
            'make': make,
            'vrm': vrm
        }
        for index, section_name in enumerate(['tax', 'mot']):
            section = html('.status-bar > div').eq(index)
            section_valid = section('.isValid')
            section_invalid = section('.isInvalid')
            is_populated = section_valid or section_invalid
            is_valid = False
            text = 'Unknown'
            if is_populated:
                is_valid = section_valid and not section_invalid
                if is_valid:
                    text = section_valid('p').text()
                else:
                    text = section_invalid('p').text()
            response[section_name] =  {
                'text': text,
                'unknown': not bool(is_populated),
                'valid': bool(is_valid)
            }
        print(response)
        return response
