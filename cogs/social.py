import io

import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps


class SocialPreviews(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def add_rounded_corners(self, image, radius=12):
        """Ajoute des coins arrondis"""
        circle = Image.new("L", (radius * 2, radius * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
        alpha = Image.new("L", image.size, 255)
        alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
        alpha.paste(
            circle.crop((radius, 0, radius * 2, radius)), (image.width - radius, 0)
        )
        alpha.paste(
            circle.crop((0, radius, radius, radius * 2)), (0, image.height - radius)
        )
        alpha.paste(
            circle.crop((radius, radius, radius * 2, radius * 2)),
            (image.width - radius, image.height - radius),
        )
        image.putalpha(alpha)
        return image

    def create_circular_avatar(self, size=40):
        """Crée un avatar circulaire"""
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        avatar = Image.new("RGB", (size, size), "#303030")
        output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        return output

    def create_tiktok_preview(
        self, thumbnail, username, description, likes, comments, shares
    ):
        """Crée la preview TikTok"""
        width = 300
        height = 520
        padding = 16

        base = Image.new(
            "RGBA", (width + (padding * 2), height + (padding * 2)), (0, 0, 0, 255)
        )
        content = Image.new("RGBA", (width, height), (0, 0, 0, 255))

        thumbnail = thumbnail.resize(
            (width, int(width * 16 / 9)), Image.Resampling.LANCZOS
        )
        content.paste(thumbnail, (0, 0))

        draw = ImageDraw.Draw(content)

        username_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        info_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)

        draw.text((16, height - 150), f"@{username}", font=username_font, fill="white")

        description_lines = []
        words = description.split()
        current_line = words[0]
        for word in words[1:]:
            test_line = current_line + " " + word
            if draw.textlength(test_line, font=info_font) < width - 32:
                current_line = test_line
            else:
                description_lines.append(current_line)
                current_line = word
        description_lines.append(current_line)

        for i, line in enumerate(description_lines[:3]):
            draw.text((16, height - 120 + i * 20), line, font=info_font, fill="white")

        icons_y = height - 50
        draw.text((20, icons_y), "♥", font=info_font, fill="white")
        draw.text((45, icons_y), likes, font=info_font, fill="white")

        draw.text((100, icons_y), "💬", font=info_font, fill="white")
        draw.text((125, icons_y), comments, font=info_font, fill="white")

        draw.text((180, icons_y), "➤", font=info_font, fill="white")
        draw.text((205, icons_y), shares, font=info_font, fill="white")

        base.paste(content, (padding, padding), content)
        return base

    def create_instagram_preview(
        self, thumbnail, username, caption, likes, comments, time
    ):
        """Crée la preview Instagram"""
        width = 400
        height = 480
        padding = 16

        base = Image.new(
            "RGBA",
            (width + (padding * 2), height + (padding * 2)),
            (255, 255, 255, 255),
        )
        content = Image.new("RGBA", (width, height), (255, 255, 255, 255))

        avatar = self.create_circular_avatar(32)
        content.paste(avatar, (12, 12), avatar)

        draw = ImageDraw.Draw(content)
        username_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        info_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)

        draw.text((52, 20), username, font=username_font, fill="black")
        draw.text((width - 30, 20), "⋮", font=username_font, fill="black")

        thumbnail = thumbnail.resize((width, width), Image.Resampling.LANCZOS)
        content.paste(thumbnail, (0, 50))

        actions_y = width + 60
        draw.text((16, actions_y), "♥", font=info_font, fill="black")
        draw.text((56, actions_y), "💬", font=info_font, fill="black")
        draw.text((96, actions_y), "➤", font=info_font, fill="black")
        draw.text((width - 30, actions_y), "🔖", font=info_font, fill="black")

        draw.text(
            (16, actions_y + 30), f"{likes} likes", font=username_font, fill="black"
        )

        caption_start = actions_y + 55
        draw.text((16, caption_start), username, font=username_font, fill="black")

        caption_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        words = caption.split()
        lines = []
        current_line = ""
        x_offset = draw.textlength(username + " ", font=username_font)

        for word in words:
            test_line = current_line + " " + word if current_line else word
            if draw.textlength(test_line, font=caption_font) < width - 32 - (
                x_offset if not lines else 0
            ):
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
                x_offset = 0
        lines.append(current_line)

        for i, line in enumerate(lines):
            x = 16 + (x_offset if i == 0 else 0)
            y = caption_start + (i * 20)
            draw.text((x, y), line, font=caption_font, fill="black")

        draw.text(
            (16, caption_start + len(lines) * 20 + 10),
            time,
            font=info_font,
            fill="#999999",
        )

        base.paste(content, (padding, padding), content)
        return base

    @app_commands.command(
        name="tiktok", description="Get a preview of your TikTok post"
    )
    async def tiktok_preview(
        self,
        interaction: discord.Interaction,
        image: discord.Attachment,
        username: str,
        description: str,
        likes: str = "1.2M",
        comments: str = "10.5K",
        shares: str = "5.2K",
    ):
        await interaction.response.defer()

        try:
            if not image.content_type.startswith("image/"):
                return await interaction.followup.send("❌ Format d'image invalide")

            thumbnail_bytes = await image.read()
            thumbnail = Image.open(io.BytesIO(thumbnail_bytes)).convert("RGBA")

            preview = self.create_tiktok_preview(
                thumbnail=thumbnail,
                username=username,
                description=description,
                likes=likes,
                comments=comments,
                shares=shares,
            )

            buffer = io.BytesIO()
            preview.save(buffer, format="PNG")
            buffer.seek(0)

            await interaction.followup.send(file=discord.File(buffer, "tiktok.png"))

        except Exception as e:
            await interaction.followup.send(f"❌ Une erreur est survenue : {str(e)}")

    @app_commands.command(
        name="instagram", description="Get a preview of your Instagram post"
    )
    async def instagram_preview(
        self,
        interaction: discord.Interaction,
        image: discord.Attachment,
        username: str,
        caption: str,
        likes: str = "1,234",
        comments: str = "99",
        time: str = "2 HOURS AGO",
    ):
        await interaction.response.defer()

        try:
            if not image.content_type.startswith("image/"):
                return await interaction.followup.send("❌ Format d'image invalide")

            thumbnail_bytes = await image.read()
            thumbnail = Image.open(io.BytesIO(thumbnail_bytes)).convert("RGBA")

            preview = self.create_instagram_preview(
                thumbnail=thumbnail,
                username=username,
                caption=caption,
                likes=likes,
                comments=comments,
                time=time,
            )

            buffer = io.BytesIO()
            preview.save(buffer, format="PNG")
            buffer.seek(0)

            await interaction.followup.send(file=discord.File(buffer, "instagram.png"))

        except Exception as e:
            await interaction.followup.send(f"❌ Une erreur est survenue : {str(e)}")


async def setup(bot: commands.Bot):
    await bot.add_cog(SocialPreviews(bot))
