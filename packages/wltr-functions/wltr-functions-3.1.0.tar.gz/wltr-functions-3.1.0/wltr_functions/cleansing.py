import re
from unicodedata import normalize
from email_validator import validate_email, EmailNotValidError


class Cleansing(object):
    class Normalize:
        def __init__(self, string):
            self.string = string

        def execute(self):
            try:
                rem = normalize('NFKD', self.string) \
                    .encode('ASCII', 'ignore') \
                    .decode('ASCII')
                return rem

            except ValueError as e:
                pass

    class Prepositions:
        def __init__(self, string, prepositions):
            self.string = string
            self.prepositions = prepositions

        def execute(self):
            try:
                ajust_name = (' '.join(word if word in self.prepositions else word.title()
                                       for word in self.string.capitalize().split(' ')))
                return ajust_name

            except ValueError as e:
                pass

    class Phone:
        def __init__(self, string):
            self.string = string

        def phone_cleansing(self):
            number_pattern = re.compile('\\d')

            try:
                number = re.sub(number_pattern, '', self.string)
                x = len(self.string)

                if x < 8:
                    self.string = None

                elif x > 11:
                    self.string = number[x - 11:]

                return self.string

            except Exception as e:
                raise Exception(str(e))

        def phone_validate(self):
            fixed_pattern = re.compile('(\\d{3})?(\\d{2})?(\\d{4})(\\d{4})')
            mobile_pattern = re.compile('(\\d{3})?(\\d{2})?(\\d{5})(\\d{4})')

            try:
                phone_number = self.phone_cleansing()

                x = len(str(phone_number))

                if x == 8 or x == 10:
                    re.match(fixed_pattern, phone_number).group(0)

                    return 'Phone'

                elif x == 9 or x == 11:
                    re.match(mobile_pattern, phone_number).group(0)

                    return 'Mobile'

                else:
                    return 'Invalid'

            except Exception as e:
                raise Exception(str(e))

    class EMail:
        def __init__(self, string):
            self.string = string

        def email_validate(self):
            if self.string is not None:
                try:
                    validate_email(self.string)

                    return True

                except EmailNotValidError as e:
                    print(str(e))

                    return False
