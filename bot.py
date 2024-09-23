import telebot

import os
from pymongo import MongoClient

# Initialize your bot using the bot token from BotFather
bot_token = '7554329147:AAGSxkAcbQyMSpYjgw4RDgIfnsYuUEHhLVs'
bot = telebot.TeleBot(bot_token)

# MongoDB setup using an SRV connection string from the environment variable
DATABASE_URI = os.environ.get('DATABASE_URI', "mongodb+srv://Madhan:N0password@cluster0.y0vtta6.mongodb.net/telegram_bot?retryWrites=true&w=majority")
client = MongoClient(DATABASE_URI)
db = client['telegram_bot']  # Database name
collection = db['users']  # Collection name

# Function to add user information (ID and name) to the database
def add_user_to_db(user_id, first_name):
    user_data = {"user_id": user_id, "first_name": first_name}
    collection.insert_one(user_data)  # Insert user data into the collection
    return f"User {first_name} with ID {user_id} added to the database."

# This function handles any incoming message to the bot
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Check if the message contains a colon
        if ":" not in message.text:
            bot.reply_to(message, "Error: Please use the format 'ID: Name'.")
            return
        
        # Split the message and check if it has exactly two parts
        user_input = message.text.split(":")
        if len(user_input) != 2:
            bot.reply_to(message, "Error: Please use the format 'ID: Name'.")
            return
        
        user_id = user_input[0].strip()  # Get the ID
        first_name = user_input[1].strip()  # Get the Name
        
        # Call the function to add user info to the database
        response = add_user_to_db(user_id, first_name)
        
        # Reply to the message with a confirmation response
        bot.reply_to(message, response)
        
    except Exception as e:
        # Log any unexpected errors
        bot.reply_to(message, "Error: Could not add user to the database.")
        print(f"Error: {e}")  # Log the error to the console

# Start polling to keep the bot running and listen for messages
if __name__ == '__main__':
    bot.polling(none_stop=True)
    app.run(host='0.0.0.0', port=8080)
