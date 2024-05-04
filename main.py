import discord
from discord.ext import commands
import logging
import util
from openai import OpenAI
from dotenv import dotenv_values

# Load the API key and Discord token from the .env file
keys = dotenv_values(".env")
api_key = keys['OPENAI_API_KEY']
discord_token = keys['DISCORD_TOKEN']

# Initialize the OpenAI client
aiClient = OpenAI(api_key=api_key)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up the Discord client
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='$', intents=intents)


# Event handler for when the bot is ready
@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user.name}')


# Command to test if the bot is working
@client.command()
async def ping(ctx):
    await ctx.send('pong')


# Command to generate an image from text
@client.command()
async def draw(ctx, content):
    # Send a message to the user that the bot is generating the image
    bends = await ctx.send("Generating image...")
    # Generate the image
    try:
        response = aiClient.images.generate(
            model="dall-e-3",
            prompt=content,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        await util.url_to_image(response.data[0].url, ctx.message)
        await bends.delete()
    # Handle exceptions
    except Exception as e:
        logging.error(e)
        await bends.delete()
        await ctx.send("An error occurred while generating the image.")

# Start the bot
client.run(discord_token)
