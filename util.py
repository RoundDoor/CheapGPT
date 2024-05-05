import aiohttp
import io
import discord


async def url_to_image(url: str, ctx: discord.ApplicationContext):
    # Download the image from the url
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.read()

    file = discord.File(io.BytesIO(data), filename="cheapGPT.png")
    await ctx.send_followup(file=file)
