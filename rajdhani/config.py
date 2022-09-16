
 # Feature Flags to enable features incrementally
 # Note: Please enable these flags only when the task asks you to do

flag_homepage = True
flag_show_schedule_link = False
flag_ticketclass_in_search = False
flag_search_filters = False

## Database configurations
## Note: Please do not modify these

db_path = "trains.db"
db_uri = f"sqlite:///{db_path}"
db_init_url = "https://rajdhani.pipal.in/static/trains.db"

base_status_page_url = "https://rajdhani.pipal.in"

# SMTP configuration
# This default configuration will work with a locally running
# server. e.g. with `pip install aiosmtpd; aiosmtpd -n`

smtp = {
    "hostname": "localhost",
    "port": "8025",
    "username": None,
    "password": None
}

# Authentication
# Note: Please do not modify this

secret_key_file = "secret_key.txt"
