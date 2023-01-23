import os

secret_key = os.getenv("SECRET_KEY", "helloworld")

 # Feature Flags to enable features incrementally
 # Note: Please enable these flags only when the task asks you to do

flag_homepage = True
flag_show_schedule_link = False
flag_ticketclass_in_search = True
flag_search_filters = False
flag_login = False
flag_bookings = False

## Database configurations
## Note: Please do not modify these

db_path = "trains.db"
db_uri = f"sqlite:///{db_path}"
db_init_url = "https://rajdhani.pipal.in/static/trains.db"

base_status_page_url = "https://rajdhani.pipal.in"

# SMTP configuration
# This default configuration will work with a locally running
# server. e.g. with `pip install aiosmtpd; aiosmtpd -n`

smtp_hostname = os.getenv("SMTP_HOSTNAME", "localhost"),
smtp_port = os.getenv("SMTP_PORT", "8025"),
smtp_username = os.getenv("SMTP_USERNAME", None),
smtp_password = os.getenv("SMTP_PASSWORD", None)
