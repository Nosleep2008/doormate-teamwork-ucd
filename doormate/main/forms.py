from django import forms

class CalendarsForm(forms.Form):
     def __init__(self, calendars, *args, **kwargs):
        super(CalendarsForm, self).__init__(*args, **kwargs)
        self.fields['calendars'] = forms.MultipleChoiceField(
            choices=[(cal["id"], cal["summary"]) for cal in calendars],
            widget=forms.CheckboxSelectMultiple,
        )