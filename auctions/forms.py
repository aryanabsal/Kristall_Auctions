from django import forms


class CommentForm(forms.Form):
    text = forms.CharField(label="",required=True, widget=forms.Textarea(attrs={'class': 'form-control-md lead from-group', 'rows':'3', 'cols':'63'}))

class BidForm(forms.Form):
    text = forms.DecimalField(label="",required=True, max_digits=10, decimal_places=2)

class SearchForm(forms.Form):
    query = forms.CharField(label="", max_length=100)

class AuctionListingForm(forms.Form):
    title = forms.CharField(
        label='Title',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Give it a title'
        }
        )
    )
    description = forms.CharField(
        label='Description',
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Tell more about the product',
            'rows': '3'
        }
        )
    )
    price = forms.DecimalField(
        label='Price',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Estimated price (optional)',
            'min': '0.01',
            'max': '999999999.99',
            'step': '0.01'
        }
        )
    )
    start_bid = forms.DecimalField(
        label='Starting Bid',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Starting bid',
            'min': '0.01',
            'max': '99999999999.99',
            'step': '0.01'
        }
        )
    )
    category = forms.CharField(
        label='Category',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-group',
            'autocomplete': 'on',
            'placeholder': 'Category (optional)'
        }
        )
    )
    image_url = forms.URLField(
        label='Image URL',
        required=False,
        initial='https://pineridge.glfconnect.com/store/content/images/thumbs/default-image_450.png',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-group',
            'placeholder': 'Image URL (optional)',
        }
        )
    )
