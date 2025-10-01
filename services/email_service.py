import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os
from dotenv import load_dotenv

class EmailService:
    def __init__(self):
        #!SMTP server configuration

        #!Still need to fix this and set the .env file properly because I'm lowkey not working properly.

        load_dotenv()
        password = os.environ.get("APP_PASSWORD")
        
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "sanjeetrashad@gmail.com"
        self.sender_password = password
    
    def send_confirmation_email(self, recipient_email: str, reservation_details: dict) -> bool:
        try:
            #!Making the email
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient_email
            message["Subject"] = "Movie Reservation Confirmation"
            
            #!Body of the email
            body = f"""
            Dear {reservation_details['customer_name']},
            
            Your movie reservation has been confirmed!
            
            Reservation Details:
            - Movie: {reservation_details['movie_title']}
            - Showtime: {reservation_details['showtime']}
            - Screen: {reservation_details['screen']}
            - Seats: {reservation_details['seat_numbers']}
            - Total Price: ${reservation_details['total_price']:.2f}
            
            Please arrive 15 minutes before showtime.
            
            Thank you for choosing our theater!
            
            Best regards,
            Movie Theater Management
            """
            
            message.attach(MIMEText(body, "plain"))
            
            #!Information
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(message)
            server.quit()
            
            print(f"Email sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
