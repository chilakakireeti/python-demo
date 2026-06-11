from fastapi import APIRouter,HTTPException,Depends
from models.models import signup,otp_validation,forgot_password,reset_validation,TokenResponse
from db.database import fetch_user,add_user,update_user,login_collection
from email.message import EmailMessage
from app.utils import Hash_pswrd,validate,create_acces_tocken,get_current_user,oauth2_scheme,send_otp_email,send_otp_email2,send_email
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
import os
import smtplib
import random

load_dotenv()
 router=APIRouter()
otp={}
otp_2={}

@router.post('/signup')
async def signup(data:signup):
    try:
            if data.password != data.confirm_password:
                raise HTTPException(status_code=400,detail="Passwords do not match")
            
            validate= await fetch_user({'email':data.email})
            if validate:
                raise HTTPException(status_code=409,detail='data alredy exist')
            
           #generating otp
        
            Otp=str(random.randint(100000,999999))

            #store temperorryly
            otp[data.email] = {'otp': Otp,'name': data.username,'email': data.email, 'password': data.password,'Role':    data.role}

            #sending email  
                  
            emailsend=send_otp_email(data.email,Otp)
            if not emailsend:
                raise HTTPException(status_code=500,detail="failes to send email") 
            return {
                "message":"OTP Send Sussfully"
            }
    except  Exception as e:
        return print(e)
    
@router.post('/signup_validation')   
async def otp_verification(data:otp_validation):
    try:
        checking=otp.get(data.email)
        if not checking:
            raise HTTPException(status_code=404,detail='otp not found')
        if checking['otp'] != data.otp:
            raise HTTPException(status_code=400,detail='invalid otp')
      
        #hash password

        hash_password=await Hash_pswrd(checking['password'])

        #storing data 
        signup_data = {'name': checking['name'],'email': checking['email'],'password': hash_password,'role': checking['Role']}
        await add_user(signup_data)

        #del otp data
        del otp[data.email]
            
        return {'message':'Signup Successful'}
    except Exception as e:
     raise HTTPException(
         status_code=500,
         detail=str(e)
     )    
    
@router.post('/login')
async def login(data: OAuth2PasswordRequestForm = Depends()):

    # Check whether user exists
    user =await fetch_user({
        "email": data.username
    })

    if not user:
        raise HTTPException(status_code=404,detail="User not found")

    # Verify password
    verified =await validate(data.password, user["password"])
    if not verified:
        raise HTTPException(status_code=401,detail="Invalid password")
    hashed_pasword=await Hash_pswrd(data.password)
    login_users={"email": data.username,"password":hashed_pasword}
    login_collection.insert_one(login_users)
# JWT payload

    token_data = {"sub": user["email"]}
    
    # Generate JWT token
    access_token =await create_acces_tocken(token_data)

    

    
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }

# jwt tocken
    
@router.get("/dashboard")
async def dashboard(token: str = Depends(oauth2_scheme)):
    return {
        "message": "Welcome to dashboard",
        "token": token
    }
@router.get("/user/me")
async def dashboard2(current_user: str = Depends(get_current_user)):

   return {
        "message": "Welcome to dashboard",
        "user_email": current_user
    }
# forgot password
@router.post('/forgot_password')
async def reset_password(data:forgot_password):
    try:     
         search=await fetch_user({'email':data.email})                      
         if not search:
            raise HTTPException(status_code=404,detail='invalid email')
       
         #genereting otp

         Otp2=str(random.randint(100000,999999))
         otp_2[data.email] = {'otp': Otp2,'email': data.email,'password': data.reset_password}
         send_email=send_otp_email2(data.email,otp_2)
         if not send_email:
              raise HTTPException(status_code=500,detail="failes to send email") 

         return {"message": "RESET OTP SENT SUCESSFULLY"}
            
    except Exception as e:
         return{
              "error":str(e)
         }
    
#reset validation

@router.post('/reset_validation')

async def reset_otp(data: reset_validation):
    try:
        checking = None
 
        # find matching otp
        for value in otp_2.values():
            if value['otp'] == data.otp:
                checking = value
                break
        
        # otp not found
        if not checking:

            raise HTTPException(status_code=404,detail='otp not found')

        # hash password
        hash_password = await Hash_pswrd(checking['password'])
       
        # update password
        await update_user({'email': checking['email']},{'password': hash_password})

        # delete temp otp data
        del otp_2[checking['email']]

        return { 'message': 'Password updated successfully'}

    except Exception as e:

        raise HTTPException(status_code=500,detail=str(e))
    
@router.post("/send-email")
def send_test_email():
    return send_email(
        to_email="recipient@example.com",
        subject="Test Email",
        body="Hello from AWS SES"
    )    