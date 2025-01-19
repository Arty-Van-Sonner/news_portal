from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives as MSG

def send_mail(emails, subject, template, context, text_content, **kwargs):
    style = ''
    with open('static/css/styles.css', 'r') as file:
        style += file.read() + '\n'
    with open('static/css/additional_styles.css', 'r') as file:
        style += file.read() + '\n'
    context['style'] = style

    html = render_to_string(
            template_name = template,
            context = context,
        )
    for email in emails:
            msg = MSG(subject, text_content, None, [email])
            msg.attach_alternative(html, "text/html")
            msg.send()