from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, secrets, difflib
import random, time

sender_email = "shaxrux243@gmail.com"
sender_password = "hzsa yxaq ygcy kwnc"  # Используйте пароль приложения, а не обычный!


def send_code_to_email(receiver_email):
    print(receiver_email)
    key = random.randint(10000, 99999)
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Регистрация!"
    body = f"Code: {key}"
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return {"status": True, "code": key}
    except Exception as e:
        return {"status": False, "error": str(e)}

