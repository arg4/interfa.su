from django import forms

from django.contrib.auth.models import User
from .models import Article, Draft, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        labels = {'comment_text':''}

class DraftFormLink(forms.ModelForm):
    """
    Form describing draft creation.
    """
    class Meta:
        model = Draft
        fields = [  'article_name',
                    #'article_type',
                    'article_external_url',
                    'name_author',
                    #'article_description',
                    #'article_body_text',
                    #'article_caption_styles',
                    'make_public',
                    ]
        labels = { 'name_author':"Additional Authors"
        }
        widgets = {'name_author':forms.CheckboxSelectMultiple()}

    def __init__(self,uid, *args, **kwargs):
        super(DraftFormLink, self).__init__(*args, **kwargs)
        self.fields['name_author'].queryset = User.objects.filter(groups__name='Author').exclude(id=uid)
        q_set = User.objects.all()
        name_author = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset = q_set)


class DraftFormTutorial(forms.ModelForm):
    """
    Form describing an editorial type piece
    """
    class Meta:
        model = Draft
        fields = [  'article_name',
                    #'article_type',
                    #'article_external_url',
                    'name_author',
                    'article_description',
                    'article_body_text',
                    #'article_caption_styles',
                    'make_public',
                    ]
        labels = { 'name_author':"Additional Authors"}
        widgets = {'name_author':forms.CheckboxSelectMultiple()}

    def __init__(self,uid, *args, **kwargs):
        super(DraftFormTutorial, self).__init__(*args, **kwargs)
        self.fields['name_author'].queryset = User.objects.filter(groups__name='Author').exclude(id=uid)
        q_set = User.objects.all()
        name_author = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset = q_set)


class DraftFormEditorial(forms.ModelForm):
    """
    Form describing an editorial type piece
    """
    class Meta:
        model = Draft
        fields = [  'article_name',
                    #'article_type',
                    #'article_external_url',
                    'name_author',
                    'article_description',
                    'article_body_text',
                    'article_caption_styles',
                    'make_public',
                    ]
        labels = { 'name_author':"Additional Authors"}
        widgets = {'name_author':forms.CheckboxSelectMultiple()}

    def __init__(self,uid, *args, **kwargs):
        super(DraftFormEditorial, self).__init__(*args, **kwargs)
        self.fields['name_author'].queryset = User.objects.filter(groups__name='Author').exclude(id=uid)
        q_set = User.objects.all()
        name_author = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset = q_set)


class ArticleFormLink(forms.ModelForm):
    """
    Form describing draft creation.
    """
    class Meta:
        model = Article
        fields = [  'article_name',
                    #'article_type',
                    'article_external_url',
                    'name_author',
                    #'article_description',
                    #'article_body_text',
                    #'article_caption_styles',
                    ]
        labels = { 'name_author':"Add Additional Authors"
        }
        widgets = {'name_author':forms.CheckboxSelectMultiple()}

    def __init__(self,uid, *args, **kwargs):
        super(ArticleFormLink, self).__init__(*args, **kwargs)
        self.fields['name_author'].queryset = User.objects.filter(groups__name='Author').exclude(id=uid)
        q_set = User.objects.all()
        name_author = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset = q_set)


class ArticleFormTutorial(forms.ModelForm):
    """
    Form describing an editorial type piece
    """
    class Meta:
        model = Article
        fields = [  'article_name',
                    #'article_type',
                    #'article_external_url',
                    'name_author',
                    'article_description',
                    'article_body_text',
                    #'article_caption_styles',
                    ]
        labels = { 'name_author':"Additional Authors"}
        widgets = {'name_author':forms.CheckboxSelectMultiple()}

    def __init__(self,uid, *args, **kwargs):
        super(ArticleFormTutorial, self).__init__(*args, **kwargs)
        self.fields['name_author'].queryset = User.objects.filter(groups__name='Author').exclude(id=uid)
        q_set = User.objects.all()
        name_author = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset = q_set)


class ArticleFormEditorial(forms.ModelForm):
    """
    Form describing an editorial type piece
    """
    class Meta:
        model = Article
        fields = [  'article_name',
                    #'article_type',
                    #'article_external_url',
                    'name_author',
                    'article_description',
                    'article_body_text',
                    'article_caption_styles',
                    ]
        labels = { 'name_author':"Additional Authors"}
        widgets = {'name_author':forms.CheckboxSelectMultiple()}

    def __init__(self,uid, *args, **kwargs):
        super(ArticleFormEditorial, self).__init__(*args, **kwargs)
        self.fields['name_author'].queryset = User.objects.filter(groups__name='Author').exclude(id=uid)
        q_set = User.objects.all()
        name_author = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset = q_set)
