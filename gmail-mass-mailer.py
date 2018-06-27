from tkinter import *
import smtplib
from threading import Thread
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


root = Tk()
root.title("Gmail Mass Mailer")
root.resizable(False, False)
text = Text(root)
text.config(width=50, height=10, state=DISABLED)
text.grid(column=1, columnspan=2, row=4)
email_list = []
successfully_sent = 0


def text_print(msg):
    text.config(state=NORMAL)
    text.insert('1.0', msg + "\n")
    text.config(state=DISABLED)


def send_mail(email, password):
    global successfully_sent
    message = MIMEMultipart()
    message['From'] = email
    message['To'] = victims_email.get()
    message['Subject'] = email_subject.get()
    body = email_message.get()
    body = MIMEText(body)
    message.attach(body)
    try:
        server = smtplib.SMTP()
        server.connect("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, victims_email.get(), message.as_string())
        server.quit()
        successfully_sent += 1
        text_print("Successfully sent email from: \n" + email)
    except:
        text_print("An error occurred while \ntrying to send email from: \n" + email)


def add_email(*args):
    global email_list
    if email_address.get() != "" and email_password.get() != "" and ":" not in email_address.get() and ":" not in email_password.get():
        email = email_address.get() + ":" + email_password.get()
        email_list.append(email)
        text_print(email)
        email_password.set("")
        email_address.set("")


def clear_list():
    global email_list
    email_list = []
    text.config(state=NORMAL)
    text.delete("1.0", END)
    text.config(state=DISABLED)


def send_emails():
    if victims_email != "" and num_of_emails != "" and email_subject != "" and email_message != "":
        try:
            int(num_of_emails.get())
        except:
            num_of_emails.set("Wrong Input!")
            return None
        text.config(state=NORMAL)
        text.delete("1.0", END)
        text.config(state=DISABLED)
        for i in range(int(num_of_emails.get())):
            for x in email_list:
                x = x.split(":")
                Thread(target=send_mail, args=(x[0], x[1])).start()
                sleep(0.5)
        clear_list()


email_address = StringVar()
email_password = StringVar()
victims_email = StringVar()
mails_send = StringVar()
num_of_emails = StringVar()
email_subject = StringVar()
email_message = StringVar()

Label(root, text="Your Email Address: ").grid(column=1, row=1)
Entry(root, textvariable=email_address).grid(column=2, row=1)
Label(root, text="Your Email Password: ").grid(column=1, row=2)
Entry(root, textvariable=email_password).grid(column=2, row=2)
Button(root, text="Add To Email List", width=18, command=add_email).grid(column=2, row=3)
Button(root, text="Clear Email List", width=18, command=clear_list).grid(column=1, row=3)
Label(root, text="Victims Email Address: ").grid(column=1, row=5)
Entry(root, textvariable=victims_email).grid(column=2, row=5)
Label(root, text="Email Subject: ").grid(column=1, row=6)
Entry(root, textvariable=email_subject).grid(column=2, row=6)
Label(root, text="Email Message: ").grid(column=1, row=7)
Entry(root, textvariable=email_message).grid(column=2, row=7)
Label(root, text="Number of Emails to send: ").grid(column=1, row=8)
Label(root, text="(From every account)").grid(column=1, row=9)
Entry(root, textvariable=num_of_emails).grid(column=2, row=8, sticky=N)
Button(root, text="Send Emails", command=send_emails, width=14).grid(column=2, row=9)

for child in root.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.bind("<Return>", add_email)
root.mainloop()
