from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import Depends,HTTPException
from db.database import fetch_user
from email.message import EmailMessage
import smtplib
import boto3
from botocore.exceptions import ClientError
import os

load_dotenv()

#JWT tocken keys
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE=30

# hashpassword methods

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# Hash password
async def Hash_pswrd(password: str):

    return pwd_context.hash(password)


# Verify password
async def validate(plain_password: str, hashed_password: str):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

#jwt authintication

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def create_acces_tocken(data:dict,expiree:timedelta |None=None):
    to_encode=data.copy()
    expire = datetime.now(timezone.utc) + (
    expiree if expiree else timedelta(minutes=15)
)
    to_encode.update({
        "exp": expire.timestamp()
    })
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

async def verify_token(

    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        return email

    except JWTError:

        return None

async def get_current_user(

    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]
        )
        print(payload)
        username = payload.get("sub")
        print(username)

        if username is None:

            raise HTTPException(

                status_code=401,

                detail="Invalid token"
            )

        return username

    except JWTError:

        raise HTTPException(

            status_code=401,

            detail="Token is invalid or expired"
        )





def send_otp_email(to_mail: str, otp: str):

    try:

        # Sender credentials
        from_mail = os.getenv("SENDER_MAIL")
        password = os.getenv("SENDER_PASSWORD")

        # Create SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)

        # Start TLS encryption
        server.starttls()

        # Login
        server.login(from_mail, password)

        # Create Email Message
        msg = EmailMessage()

        msg["Subject"] = "OTP VERIFICATION"
        msg["From"] = from_mail
        msg["To"] = to_mail

        # Email body
        msg.set_content(f"Your OTP is: {otp}")

        # Send email
        server.send_message(msg)

        # Close connection
        server.quit()

        return True

    except Exception as e:

        print("Email Error:", str(e))

        return False
    

# forgot validation

def send_otp_email2(to_mail: str, otp: str):

    try:

        # Sender credentials
        from_mail = os.getenv("SENDER_MAIL")
        password = os.getenv("SENDER_PASSWORD")

        # Create SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)

        # Start TLS encryption
        server.starttls()

        # Login
        server.login(from_mail, password)

        # Create Email Message
        msg = EmailMessage()

        msg["Subject"] = "OTP VERIFICATION"
        msg["From"] = from_mail
        msg["To"] = to_mail

        # Email body
        msg.set_content(f"Your Reset OTP is: {otp}")

        # Send email
        server.send_message(msg)

        # Close connection
        server.quit()

        return True

    except Exception as e:

        print("Email Error:", str(e))

        return False    

# email validation
ALLOWED_DOMAINS = [
    "gmail.com",
    "mitresources.com"
]
def validate_email_domine(email:str):
    domine=email.split("@")[-1]

    if domine  not in ALLOWED_DOMAINS:
        raise ValueError("Only gmail.com and mitresources.com emails are allowed")
    return email        




#================
ses_client = boto3.client(
    "ses",
    region_name="us-east-1"  # Change to your SES region
)

def send_email(to_email: str, subject: str, body: str):
    try:
        response = ses_client.send_email(
            Source="sender@example.com",  # Verified SES email
            Destination={
                "ToAddresses": [to_email]
            },
            Message={
                "Subject": {
                    "Data": subject
                },
                "Body": {
                    "Text": {
                        "Data": body
                    }
                }
            }
        )

        return {
            "message_id": response["MessageId"],
            "status": "success"
        }

    except ClientError as e:
        return {
            "status": "error",
            "message": str(e)
        }

