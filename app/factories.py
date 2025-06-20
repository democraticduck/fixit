from .forms import LoginForm, SignUpForm, ReportForm, ReportUpdateForm, RegistrationForm

class FormFactory:
    @staticmethod
    def create_form(form_type, *args, **kwargs):
        """
        Factory Method: Returns the appropriate form instance based on the type
        """
        if form_type == 'login':
            return LoginForm(*args, **kwargs)
        elif form_type == 'signup':
            return SignUpForm(*args, **kwargs)
        elif form_type == 'report':
            return ReportForm(*args, **kwargs)
        elif form_type == 'report_update':
            return ReportUpdateForm(*args, **kwargs)
        elif form_type == 'registration':
            return RegistrationForm(*args, **kwargs)
        else:
            raise ValueError(f"Unknown form type: {form_type}")
