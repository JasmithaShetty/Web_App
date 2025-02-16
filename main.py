import os
from datetime import datetime
import pytz
from db_connect import get_db_connection
from fasthtml.common import *
from dotenv import load_dotenv

load_dotenv()

MAX_NAME_CHAR =20
MAX_ADDRESS_CHAR =255
TIME_STAMP_FORMAT = "%Y-%m-%d %I:%M:%S %p GMT"

app,rt = fast_app()

def get_time():
    gmt_tz = pytz.timezone("GMT")
    return datetime.now(gmt_tz).strftime(TIME_STAMP_FORMAT)

def add_message_to_database(name, message):
    timestamp = get_time()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO table_name (name, message, timestamp) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, message, timestamp))
    
    conn.commit()
    cursor.close()
    conn.close()

def get_messages_from_database():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM list ORDER BY timestamp DESC"
    cursor.execute(query)
    messages = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return messages
    
def render_message(entry):
    return(
        Article(
            Header(f"Name: {entry['name']}"),
            P(entry["message"]),
            Footer(Small(Em(f"Posted :{entry['timestamp']}"))),
            ),
        )

def render_message_list():
    messages = get_messages_from_database()
    return Div(
        *[render_message(entry) for entry in messages],
        id="message-list"
    )
    
def render_content():
    form = Form(
        Fieldset(
            Input(
                type="text",
                name = "name",
                placeholder="Enter your name",
                required =True,
                maxlength = MAX_NAME_CHAR,
                ),
            Input(
                type="text",
                name ="message",
                placeholder="Enter your Address",
                required =True,
                maxlength = MAX_ADDRESS_CHAR,
                ),
            Button("Submit",type="Submit"),
            Role="group"
        ),
        method="post",
        hx_post="/submit-message",
        hx_target="#message-list",
        hx_swap="outerHTML",
        hx_on__after_request="this.reset()",
    )
    return Div(
        P(Em("The Tokyo's hidden Gem!")),
        form,
        P("Website is here⤵️!!...."),
        Div(
            "This is created with 🫶❤️ for 🎌 by Jasmitha🦋🤍 ",
            A("Tokyo🏯",href="https://www.japan.travel/en/destinations/kanto/tokyo/",target="blank"),
        ),
        Hr(),
        render_message_list(),
        P("Loved to see you here!!!"),
        P("ありがとうございました🙇‍♀️🎀🎎"),
    )
    
@rt('/')
def get():
    return Titled("The Insight🎌🏯",render_content())

@rt('/submit-message', methods=("POST",))
def post(name: str, message: str):
    add_message_to_database(name, message)
    return render_message_list()

serve()