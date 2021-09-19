import jwt
from fastapi import (BackgroundTasks, UploadFile, File, Form, Depends, HTTPException, status)
from pydantic import BaseModel, EmailStr
from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import dotenv_values

from models import User


config_credentials = dotenv_values(".env")


conf = ConnectionConfig(
    MAIL_USERNAME = config_credentials["MAIL_USERNAME"],
    MAIL_PASSWORD = config_credentials["MAIL_PASSWORD"],
    MAIL_FROM = config_credentials["MAIL_FROM"],
    MAIL_PORT = 587,
    MAIL_SERVER = config_credentials["MAIL_SERVER"],
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)



async def send_mail(email: List, instance: User):
    token_data = {
        "id": instance.id,
        "username": instance.username,
    }

    token = jwt.encode(token_data, config_credentials["SECRET_KEY"], algorithm='HS256')

    template = f"""
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
            <div style=" display: flex; align-items: center; justify-content: center; flex-direction: column;">
                <h3> Account Verification </h3>
                <br>
                <p>Thanks for choosing EasyShopas, please 
                click on the link below to verify your account</p> 
                <a style="margin-top:1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #0275d8; color: white;"
                 href="http://127.0.0.1:8000/verification/?token={token}">
                    Verify your email
                <a>
                <p style="margin-top:1rem;">If you did not register for EasyShopas, 
                please kindly ignore this email. Thanks<p>
            </div>
        </body>
        </html>
    """
    message = MessageSchema(
        subject = "EasyShops Account Verification Email",
        recipients = email, # List of recipients
        body = template,
        subtype = "html"
    )

    fm = FastMail(conf)
    await fm.send_message(message=message)
