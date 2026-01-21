import os
from dotenv import load_dotenv

load_dotenv()

class MailConfig:

    MAIL_DEBUG = False
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 465))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "false").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "true").lower() == "true"
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")


    # MAIL_DEBUG = False
    # MAIL_SERVER = "smtp.gmail.com"
    # MAIL_PORT = 465
    # MAIL_USERNAME = "mtm.linnaunghtet@gmail.com"
    # MAIL_PASSWORD = "yfqg uhmj hezo ptdx"
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    # MAIL_DEFAULT_SENDER = "mtm.linnaunghtet@gmail.com"