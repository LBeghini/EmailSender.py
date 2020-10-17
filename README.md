# :mailbox_with_mail: SMTPClient.py

## About

This project implements the communication between a Client SMTP to a Server SMTP to send an email.

## Technologies

- Python

## Setup

### Requirements
To run and edit this project locally, certify that you have installed the following programs:

- Python 3.8
- A code editor (I use Pycharm IDE)
- A Google account that allows [Less secure apps](myaccount.google.com/lesssecureapps)
> Gmail will complain that you're trying to login from a non-Google app.  
To avoid it, you should turn on Allow Less Secure Apps.  
You can turn it off once you finish testing the SMPTClient

After that, you'll need to clone this repo:

```
git clone https://github.com/LBeghini/TCP-Chat.git
``` 

## Usage

You'll need to edit some variables to send an email.  

### Connection using SSL to the Server

- ```login``` at line 39 should be your login in [base64](https://www.base64encode.org)
- ```password``` at line 47 should be your password in [base64](https://www.base64encode.org)

### The mail

- ```mailfrom``` at line 55 between the <> is your email
- ```rcptto``` at line 64 between the <> is the email you want to send a message to
- at line 80, after ```SUBJECT:```, is the subject of the message
- ```msg``` at line 5 is the message you want to send

Then, run SMPTClient.py through ```cmd``` with:
```
python SMTPClient.py
```
