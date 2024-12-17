from django_filters.widgets import SuffixedMultiWidget
from django.forms.widgets import DateTimeInput

class CustomRangeWidget(SuffixedMultiWidget):
    template_name = "django_filters/widgets/multiwidget.html"
    suffixes = ["min", "max"]

    def __init__(self, attrs=None):
        widgets = (DateTimeInput, DateTimeInput)
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]