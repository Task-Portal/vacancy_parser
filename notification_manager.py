import os
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from dotenv import load_dotenv

load_dotenv()


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def send_email(self, vacancies, emails):

        letter = f"""\
            <html>

              <body>
                <p >Привет<br>
                   Новые вакансии...<br>
                   {self.create_letter(vacancies)}
                </p>
              </body>
            </html>
            """


        for i in emails:

            email_from = os.getenv('EMAIL_FROM')
            password = os.getenv('EMAIL_PASSWORD')

            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()

                connection.login(user=email_from, password=password)

                msg = EmailMessage()
                asparagus_cid = make_msgid()

                msg.add_alternative(letter.format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')

                msg['To'] = i
                msg['From'] = email_from
                msg['Subject'] = "Вакансии"
                connection.send_message(msg)
                print("Email sent successfully.")

    def create_letter(self, jobs: dict):
        data = ""

        for i in jobs:

            data += f"<div style='font-size:14px;'><a href='{i['href']}'>{i['job_title']}</a>  {i['company']}, {i['period']} \n\n</div> "

        return data
