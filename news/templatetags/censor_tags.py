from django import template
import re

register = template.Library()

BAD_WORDS = ['плохое', 'запрещённое', 'нецензурное','НХЛ', 'Предприятие']

def censor_word(match):
    word = match.group()
    return word[0] + '*' * (len(word) - 1)

@register.filter()
def censor(value):
    if not isinstance(value, str):
        return value
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, BAD_WORDS)) + r')\b', flags=re.IGNORECASE)
    return pattern.sub(censor_word, value)