from django.core import validators
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class GithubIdValidator(validators.RegexValidator):
    regex = r'^[\w-]+\Z'
    message = ["GitHub IDに不正な文字が含まれています。",
               "半角英数字と-（ハイフン）のみ使用できます。"]
    flags = 0

def check_github_id_prefix(text):
    if text and text[0]=="-":
        raise ValidationError('頭文字には-（ハイフン）を使用できません。')