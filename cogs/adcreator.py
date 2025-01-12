import re

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, Modal, TextInput, View


class AdModal(Modal, title="Create your advertisement"):
    def __init__(self):
        super().__init__()

        self.title_input = TextInput(
            label="Title",
            placeholder="Enter your ad title...",
            required=True,
            max_length=256,
        )
        self.add_item(self.title_input)

        self.description = TextInput(
            label="Description",
            placeholder="Enter your ad description...",
            required=True,
            style=discord.TextStyle.paragraph,
            max_length=1024,
        )
        self.add_item(self.description)

        self.cta = TextInput(
            label="Call to Action",
            placeholder="Ex: Learn More, Shop Now, Register...",
            required=True,
            max_length=32,
        )
        self.add_item(self.cta)

        self.url = TextInput(
            label="URL", placeholder="https://your-landing-page.com", required=True
        )
        self.add_item(self.url)

        self.image_url = TextInput(
            label="Image URL (optional)",
            placeholder="https://your-image.com/image.png",
            required=False,
        )
        self.add_item(self.image_url)

    async def on_submit(self, interaction: discord.Interaction):
        url_pattern = re.compile(
            r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
        )

        if not url_pattern.match(self.url.value):
            await interaction.response.send_message(
                "❌ Invalid URL format. Please provide a valid URL.", ephemeral=True
            )
            return

        embed = discord.Embed(
            title=self.title_input.value,
            description=f"{self.description.value}\n\n→ **{self.cta.value}**",
            color=0x2F3136,
        )

        if self.image_url.value and url_pattern.match(self.image_url.value):
            embed.set_image(url=self.image_url.value)

        class AdView(View):
            def __init__(self, url: str, cta: str):
                super().__init__(timeout=None)
                self.add_item(
                    Button(label=cta, url=url, style=discord.ButtonStyle.link)
                )

        view = AdView(self.url.value, self.cta.value)

        await interaction.response.send_message(embed=embed, view=view)


class AdCreator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="create_ad",
        description="Create an advertisement with a custom embed and CTA button",
    )
    async def create_ad(self, interaction: discord.Interaction):
        """Ouvre un modal pour créer une publicité personnalisée"""
        modal = AdModal()
        await interaction.response.send_modal(modal)


async def setup(bot: commands.Bot):
    await bot.add_cog(AdCreator(bot))
