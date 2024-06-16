import phonenumbers

def normalize_phone_number(phone_number, default_region='IN'):
    try:
        parsed_number = phonenumbers.parse(phone_number, default_region)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number")
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        return formatted_number
    except phonenumbers.NumberParseException as e:
        print(f"Error parsing phone number {phone_number}: {e}")
        return None
    except ValueError as e:
        print(f"Error validating phone number {phone_number}: {e}")
        return None
