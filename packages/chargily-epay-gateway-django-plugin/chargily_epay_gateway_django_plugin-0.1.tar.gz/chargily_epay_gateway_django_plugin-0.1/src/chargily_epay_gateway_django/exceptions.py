CHARGILY_ERROR_CODE_DJANGO_KEYS_MISSING = 1

CHARGILY_ERROR_CODES_DJANGO = [
    CHARGILY_ERROR_CODE_DJANGO_KEYS_MISSING,
]


class ChargilyErrorBaseDjango(ValueError):
    def __str__(self):
        return self.chargily_msg

    def __init__(self, error_code, *args):
        super().__init__(*args)
        self.error_code = 0
        self.chargily_msg = None

        if error_code is None or (isinstance(error_code, int) and error_code < 1):
            self.chargily_msg = 'Invalid Error Code ({error_code})!'.format(error_code=error_code or None)
        elif not isinstance(error_code, int):
            self.chargily_msg = 'Invalid Data Type for Error Code ({data_type})!'.format(
                data_type=type(error_code).__name__
            )
        elif error_code not in CHARGILY_ERROR_CODES_DJANGO:
            self.chargily_msg = 'Invalid Value for Error Code ({error_code})!'.format(error_code=error_code)
        else:
            self.error_code = error_code


class ChargilyErrorDjangoKeysMissing(ChargilyErrorBaseDjango):
    class_error_code = CHARGILY_ERROR_CODE_DJANGO_KEYS_MISSING

    def __init__(self, api_var, *args):
        super().__init__(error_code=self.class_error_code, *args)
        self.chargily_msg = 'Failed to load your API credentials, please make sure you set ({api_var}) in your settings.py file.'.format(api_var=api_var)
