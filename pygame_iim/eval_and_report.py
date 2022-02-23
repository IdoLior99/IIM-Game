# import smtplib, ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
import yagmail


def send_mail(subject, msg, who):
    my_password = "ToTResMail00"
    mail_add = "eldarnirpersonal@gmail.com"
    rec_mail = f"eldarnirpersonal+{who}@gmail.com"
    yagmail.register(mail_add, my_password)
    yag = yagmail.SMTP(mail_add)
    yag.send(
        to=rec_mail,
        subject=subject,
        contents=msg,
    )

def send_mail_csv(subject, msg, results_csv, who):
    my_password = None  # TODO: find out the password
    mail_add = "eldarnirpersonal@gmail.com"
    rec_mail = f"eldarnirpersonal+{who}@gmail.com"
    yagmail.register(mail_add, my_password)
    yag = yagmail.SMTP(mail_add)
    yag.send(
        to=rec_mail,
        subject=subject,
        contents=msg,
        attachments=results_csv,
    )
# def send_mail(subject, msg, who):
#     sender_email = "eldarnirpersonal@gmail.com"
#     receiver_email = f"eldarnirpersonal+{who}@gmail.com"
#     password = None  # TODO: find out the password
#     PORT = 456  # TODO: find out what port needs to be
#
#     message = MIMEMultipart("alternative")
#     message["Subject"] = subject
#     message["From"] = sender_email
#     message["To"] = receiver_email
#
#     part1 = MIMEText(msg, "plain")
#     message.attach(part1)
#
#     # Create secure connection with server and send email
#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message.as_string())


def accuracy(lst):
    return sum(lst) / len(lst)


def avg_time(lst):
    return sum(lst) / len(lst)


def report_performance_mail(acc, time, eng, tut, ans, NPC_type, player_id):
    msg = f"Who: {player_id} \
            NPC: {NPC_type} \
            Answers: {ans} \
            Accuracy: {acc} \
            Time: {time} \
            Tutorial stats: {tut} \
            NPC engagement: {eng} \
            "
    # TODO: try adding empty csv to exe and sending the data in the csv through mail.
    subject = f"{player_id}'s Statistics"
    send_mail(subject, msg, player_id)
