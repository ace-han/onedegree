import phonenumbers

def format_phonenumbers(phone_num_str, 
                   quiet=False,
                   desired_format=phonenumbers.PhoneNumberFormat.E164, 
                   country_code='CN'):
    '''
        Return a formatted phone number string in the desired_format
            phonenumbers.phonenumberutil.NumberParseException if not parse-able
            ValueError if not a valid phone number
        quiet=True will always return a str, empty str when violations for above exceptions detected
    '''
    x = None
    try:
        x = phonenumbers.parse(phone_num_str, country_code)
    except phonenumbers.phonenumberutil.NumberParseException as e:
        if quiet:
            return ''
        else:
            raise e
    if not phonenumbers.is_possible_number(x) or not phonenumbers.is_valid_number(x):
        if quiet:
            return ''
        else:
            raise ValueError('invalid phone number: %s' % phone_num_str)
    
    return phonenumbers.format_number(x, desired_format)
    