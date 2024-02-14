from django import forms
from .models import Ticket, Review

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        for i, (name, field) in enumerate(self.fields.items(), start=8):
            field.widget.attrs['tabindex'] = str(i)


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(6)]

    rating = forms.ChoiceField(
                                choices=RATING_CHOICES,
                                widget=forms.RadioSelect(attrs={'tabindex': '8'})
                            )

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for i, (name, field) in enumerate(self.fields.items(), start=9):
            field.widget.attrs['tabindex'] = str(i)