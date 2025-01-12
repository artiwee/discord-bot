import discord 
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
from datetime import timedelta

class YouTube(commands.Cog):
   def __init__(self, bot: commands.Bot):
       self.bot = bot

   def add_rounded_corners(self, image, radius=12):
       """Ajoute des coins arrondis précis comme YouTube"""
       circle = Image.new('L', (radius * 2, radius * 2), 0)
       draw = ImageDraw.Draw(circle)
       draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
       alpha = Image.new('L', image.size, 255)
       alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
       alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (image.width - radius, 0))
       alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, image.height - radius))
       alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (image.width - radius, image.height - radius))
       image.putalpha(alpha)
       return image

   def create_circular_avatar(self, size=40):
       """Crée un avatar circulaire"""
       mask = Image.new('L', (size, size), 0)
       draw = ImageDraw.Draw(mask)
       draw.ellipse((0, 0, size, size), fill=255)
       avatar = Image.new('RGB', (size, size), '#303030')  # Gris foncé
       output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
       output.putalpha(mask)
       return output

   def create_youtube_preview(self, thumbnail, title, channel_name, views, time, duration):
       """Crée la preview YouTube complète"""
       width = 400
       height = 330
       padding = 16  

       base = Image.new('RGBA', (width + (padding * 2), height + (padding * 2)), (255, 255, 255, 255))
       content = Image.new('RGBA', (width, height), (255, 255, 255, 255))
       
       thumbnail = thumbnail.resize((width, 225), Image.Resampling.LANCZOS)
       thumbnail = self.add_rounded_corners(thumbnail)

       draw = ImageDraw.Draw(thumbnail)
       timestamp_box = Image.new('RGBA', (65, 25), (0, 0, 0, 180))
       timestamp_box = self.add_rounded_corners(timestamp_box, 4)
       timestamp_x = width - timestamp_box.width - 5
       timestamp_y = 225 - timestamp_box.height - 5
       thumbnail.paste(timestamp_box, (timestamp_x, timestamp_y), timestamp_box)

       font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
       draw.text((timestamp_x + 32, timestamp_y + 12), duration, font=font, fill='white', anchor="mm")

       content.paste(thumbnail, (0, 0), thumbnail)

       avatar = self.create_circular_avatar()
       content.paste(avatar, (12, 240), avatar)

       draw = ImageDraw.Draw(content)
       title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
       info_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)

       title_lines = []
       words = title.split()
       current_line = words[0]
       for word in words[1:]:
           test_line = current_line + " " + word
           if draw.textlength(test_line, font=title_font) < width - 70:
               current_line = test_line
           else:
               title_lines.append(current_line)
               current_line = word
       title_lines.append(current_line)

       for i, line in enumerate(title_lines[:2]):
           draw.text((65, 240 + i*20), line, font=title_font, fill='black')

       draw.text((65, 285), channel_name, font=info_font, fill='#606060')
       draw.text((65, 305), f"{views} views • {time}", font=info_font, fill='#606060')

       draw.text((width - 25, 240), "⋮", font=title_font, fill='#606060')

       base.paste(content, (padding, padding), content)

       return base

   @app_commands.command(
       name="youtube",
       description="Get a preview of your miniature from YouTube",
   )
   async def youtube_thumbnail(
       self,
       interaction: discord.Interaction,
       image: discord.Attachment,
       title: str,
       channel_name: str,
       views: str = "31K",
       time: str = "7 days ago",
       duration: str = "20:49"
   ):
       await interaction.response.defer()

       try:
           if not image.content_type.startswith('image/'):
               return await interaction.followup.send("❌ Format d'image invalide")

           thumbnail_bytes = await image.read()
           thumbnail = Image.open(io.BytesIO(thumbnail_bytes)).convert('RGBA')

           preview = self.create_youtube_preview(
               thumbnail=thumbnail,
               title=title,
               channel_name=channel_name,
               views=views,
               time=time,
               duration=duration
           )

           buffer = io.BytesIO()
           preview.save(buffer, format='PNG')
           buffer.seek(0)

           await interaction.followup.send(
               file=discord.File(buffer, 'youtube.png'),
           )

       except Exception as e:
           await interaction.followup.send(f"❌ Une erreur est survenue : {str(e)}")

async def setup(bot: commands.Bot):
   await bot.add_cog(YouTube(bot))