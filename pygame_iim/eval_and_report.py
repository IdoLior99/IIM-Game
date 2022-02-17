import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(subject, msg, who):
    sender_email = "eldarnirpersonal@gmail.com"
    receiver_email = f"eldarnirpersonal+{who}@gmail.com"
    password = None  # TODO: find out the password
    PORT = None  # TODO: find out what port needs to be

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    part1 = MIMEText(msg, "plain")
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def accuracy(lst):
    return sum(lst == True) / len(lst)


def avg_time(lst):
    return sum(lst) / len(lst)


def report_performance_mail(acc, time, NPC_type, player_id):
    msg = f"Who: {player_id} \
            Accuracy: {acc} \
            Time: {time} \
            NPC: {NPC_type}"
    subject = f"{player_id}'s Statistics"
    send_mail(subject, msg, player_id)
