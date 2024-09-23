import telebot
from pymongo import MongoClient

# Initialize your bot using the bot token from BotFather
bot_token = '7554329147:AAGSxkAcbQyMSpYjgw4RDgIfnsYuUEHhLVs'
bot = telebot.TeleBot(bot_token)

# MongoDB setup to connect to the database
# Replace the URI with your actual MongoDB connection string
client = MongoClient("mongodb+srv://Madhan:N0password@cluster0.y0vtta6.mongodb.net/?retryWrites=true&w=majority")
db = client['telegram_bot']  # Database name
collection = db['users']  # Collection name

# Function to add user information (ID and name) to the database
def add_user_to_db(user_id, first_name):
    # Creating a dictionary to store user info
    user_data = {"user_id": user_id, "first_name": first_name}
    
    # Insert the user data into the MongoDB collection
    collection.insert_one(user_data)
    
    # Return a confirmation message
    return f"User {first_name} with ID {user_id} added to the database."

# This function handles any incoming message to the bot
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Extract user ID and name from the message sender
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        
        # Call the function to add user info to the database
        response = add_user_to_db(user_id, first_name)
        
        # Reply to the message with a confirmation response
        bot.reply_to(message, response)
        
    except Exception as e:
        # In case of any error, send this message back to the user
        bot.reply_to(message, "Error: Could not add user to the database.")

# Start polling to keep the bot running and listen for messages
bot.polling()
