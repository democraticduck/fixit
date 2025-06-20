from abc import ABC, abstractmethod
import re

class BaseValidator(ABC):
    @abstractmethod
    def validate(self, value):
        pass

class DefaultValidator(BaseValidator):
    def validate(self, value):
        return True

class PasswordValidator(BaseValidator):
    def validate(self, value):
        return len(value) > 8


class EmailValidator(BaseValidator):
    def validate(self, value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return bool(re.fullmatch(regex, value))

class ICValidator(BaseValidator):
    def validate(self, value):
        return len(value) == 12 and value.isdigit()

class PhoneNumValidator(BaseValidator):
    def validate(self, value):
        return len(value) == 10 or len(value) == 11

def getValidator(key):
    match key:
        case 'ic_num':
            return ICValidator

        case 'password' | 'password1' | 'password2':
            return PasswordValidator

        case 'email':
            return EmailValidator
        
        case 'phone_num':
            return PhoneNumValidator

        case _:
            return DefaultValidator

            