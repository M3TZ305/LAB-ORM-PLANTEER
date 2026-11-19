from django import forms

from .models import Comment, Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "category", "about", "used_for", "image", "is_edible"]
        widgets = {
            "about": forms.Textarea(attrs={"rows": 4}),
            "used_for": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {"image": "Upload a photograph up to 8 MB."}

    def clean_image(self):
        image = self.cleaned_data["image"]
        if "image" in self.changed_data and image.size > 8 * 1024 * 1024:
            raise forms.ValidationError("Choose an image smaller than 8 MB.")
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["full_name", "content"]
        labels = {"content": "Comment"}
        widgets = {"content": forms.Textarea(attrs={"rows": 4})}
