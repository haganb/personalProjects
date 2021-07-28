import telegram
from telegram.inline.inlinequeryresultdocument import InlineQueryResultDocument
from telegram.ext import Updater, CommandHandler
import praw
import random
import logging
import os
import json

# Global vars and api stuff
# Not in repo for obvious reasons, replace with your own API tokens/secrets to test
with open("vars.json") as f:
    info = json.load(f)
TOKEN = info["TOKEN"]
REDDIT_SECRET = info["REDDIT_SECRET"]
REDDIT_ID = info["REDDIT_ID"]

reddit = praw.Reddit(
        client_id=REDDIT_ID,
        client_secret=REDDIT_SECRET,
        user_agent="testscript by u/patchworky"
    )
    
# Commands
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a cat bot, ask me about cats")

def get_random_cat(update, context):
    #context.bot.send_message(chat_id=update.effective_chat.id, text="Getting a random cat...")
    
    # Build array of random cats
    src = reddit.subreddit("cats+blackcats+catpictures+supermodelcats").hot(limit=25) # poll cats subreddit for top 10 hot posts
    candidates = []
    accepted_types = [".png", ".jpg", ".jpeg"] # filter out videos and self posts
    for post in src:
        if any(x in post.url for x in accepted_types):
            candidates.append(post.url)
    img_url = candidates[random.randint(0, len(candidates)-1)] # select random URL from candidates
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=img_url, caption="Source: {}".format(img_url))

def get_cat_fact(update, context):
    with open('catfacts.txt') as f:
        facts = f.readlines()
    fact = facts[random.randint(0, len(facts)-1)].rstrip()
    context.bot.send_message(chat_id=update.effective_chat.id, text=fact)

# Main
if __name__ == "__main__":
    # Setup and object instantiation
    bot = telegram.Bot(token=TOKEN)
    #print(bot.get_me())

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Add commands
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('random', get_random_cat))
    dispatcher.add_handler(CommandHandler('fact', get_cat_fact))
    
    # Bot starter
    updater.start_polling()
    #updater.idle()