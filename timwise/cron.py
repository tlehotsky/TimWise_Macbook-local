# filepath: timwise/cron.py
from django_cron import CronJobBase, Schedule
import os, sys, random
import psycopg2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 10  # every 10 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'  # a unique code

    def do(self):
        # Your code here



        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(
                host = '134.209.220.170',
                dbname = 'django',
                user = 'django',
                password = '95b59de430f28cb03f211a5ac5c32218',
                port = 5432,
                sslmode='require'
            )
            print ("SUCCESS connecting to the database")

        except Exception as e:
            print("failed to connect to postgres database with the followiing error:\n",e)
            sys.exit()


        try:
            # Create a cursor
            cur = conn.cursor()

            # Fetch all user_ids from auth_user table
            print("Fetching all user_ids from auth_user table...")
            cur.execute('SELECT id FROM auth_user')
            user_ids = [row[0] for row in cur.fetchall()]
            print("User IDs:", user_ids)

            # Close the communication with the PostgreSQL
            cur.close()
            # conn.close()

        except Exception as e:
            print("Failed to fetch user_ids with the following error:\n", e)
            if cur:
                cur.close()
            if conn:
                conn.close()

        x=1
        for ID in user_ids:
            try:
                # Create a cursor
                cur = conn.cursor()

                # Fetch the email for the current user ID
                cur.execute('SELECT email FROM auth_user WHERE id = %s', (ID,))
                email = cur.fetchone()[0]

                print("User number", x, "has user ID:", ID)
                print("The user's email address is", email)

                # Fetch a random text and book_id from the Timwise_highlight table for the current user ID
                cur.execute('SELECT text, book_id FROM Timwise_highlight WHERE user_id = %s', (ID,))
                highlights = cur.fetchall()

                if highlights:
                    random_highlight = random.choice(highlights)
                    random_text = random_highlight[0]
                    book_id = random_highlight[1]
                    cur.execute('SELECT name FROM Timwise_book WHERE "ID" = %s', (book_id,))
                    book_name = cur.fetchone()[0]
                    print("A random highlight from the book:", book_name, "for this user ID", ID," is:", random_text)
                    # print("The book ID for this highlight is:", book_id)

                    message = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
    <div style="max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;">
      <h1 style="color: #007BFF; text-align: center;">Hello, TimWise here...</h1>
      <hr style="border: none; height: 1px; background-color: #ddd;">
      <p style="font-size: 18px;">Sending you today's highlight:</p>
      <div style="margin: 20px 0; padding: 15px; border-left: 4px solid #007BFF; background-color: #eef5ff;">
        <p style="margin: 0;"><strong>Book Name:</strong> {book_name}</p>
      </div>
      <p style="font-size: 16px; margin-top: 20px; text-align: justify;">{random_text}</p>
      <hr style="border: none; height: 1px; background-color: #ddd; margin: 30px 0;">
      <footer style="text-align: center; font-size: 14px; color: #555;">
        <p>&copy; 2025 TimWise Highlights</p>
      </footer>
    </div>
  </body>
</html>
"""


                    # send_email("Test Subject", "<p>Test Body</p>", email)
                    send_email("Today's Highlight", message, [email])


                else:
                    print("No highlights found for this user.")

                # Close the cursor
                cur.close()

            except Exception as e:
                print("Failed to fetch data for user ID", ID, "with the following error:\n", e)
                if cur:
                    cur.close()

            x += 1

        # Close the connection
        conn.close()











    def send_email(subject, body, to):
        gmail_user = "timwise.app@gmail.com"
        gmail_password = "bmhg xbzq lqve mpxt"  # Replace with the App Password from Google

        sent_from = gmail_user
        # to = ["tim.lehotsky@wsp.com"]

        msg = MIMEMultipart('alternative')
        msg['From'] = sent_from
        msg['To'] = ", ".join(to)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            # server.set_debuglevel(1)  # Enable debug output
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, msg.as_string())
            server.close()
            print("Email sent!")
        except Exception as e:
            print(f"Something went wrong: {e}")


