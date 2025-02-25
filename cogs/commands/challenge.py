import discord 
from discord.ext import commands
from config import GUILDID
from cogs.profile.challengeProfile import challengeProfile
from utils.discord.viewmenu import SelectView

class Challenge(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    challenge = discord.SlashCommandGroup("challenge", "")

    @challenge.command(name="lookup", description="look up a challenge", guild=discord.Object(id=int(GUILDID)))
    @discord.option(
        "code",
        description = "Enter a challenge code",
        required = True
    )
    async def lookup(self, ctx:discord.ApplicationContext, code: str):

        embed = challengeProfile(index=code.upper())
        await ctx.respond(embed=embed)





    @challenge.command(name="daily", description="Get the current daily challenge.", guild=discord.Object(id=int(GUILDID))) #type: ignore
    @discord.option(
            "difficulty",
            description = "Enter the type of daily challenge, default is Advanced.",
            choices = ["Standard", "Advanced", "Co-op"],
            required = False
        )
    async def daily(self, ctx:discord.ApplicationContext, difficulty: str = "Advanced"):

        if difficulty == "Co-op":
            difficulty = "coop"
        
        embed, _= challengeProfile(index=None, difficulty=difficulty.lower()) #type: ignore

        data = {
            "Author": ctx.author.id, 
            "EventName": [None],
            "PreviousEvents": ["placeholder"],
            "Function": challengeProfile,
            "Difficulty": difficulty.lower(),
            "Message": None,
            "Emoji": ["<:Coop:1341515962410598521>"], 
            "Button": [
                    ["Standard", "standard", "success"],
                    ["Advanced", "advanced", "primary"],
                    ["Co-op", "coop", "danger"]
                ]
            }

        view = SelectView(data)
        message = await ctx.respond(embed=embed, view=view)
        view.message = message

def setup(bot):
    bot.add_cog(Challenge(bot))
