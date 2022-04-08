import discord

# This is here for typing to avoid cyclic import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cogs.blackjack.game import Game


class BlackjackView(discord.ui.View):
    def __init__(self, game: 'Game'):
        super().__init__(
            HitButton(game),
            StandButton(game),
            timeout=300
        )

    async def on_timeout(self):
        pass


class StandButton(discord.ui.Button):
    def __init__(self, game: 'Game'):
        super().__init__(label="STAND")
        self.game = game

        if self.game.isfinished:
            self.disabled = True

    async def callback(self, interaction: discord.Interaction):

        player = self.game.find_player_by_id(interaction.user.id)

        player.playable = False  # disable player from playing

        # Finish the game
        if self.game.all_locked_in():
            self.game.play_dealer()
            self.game.determine_winner()

        await interaction.response.edit_message(embed=self.game.embed, view=self.game.view)


class HitButton(discord.ui.Button):
    def __init__(self, game: 'Game'):
        super().__init__(label="HIT")
        self.game = game

        if self.game.isfinished:
            self.disabled = True

    async def callback(self, interaction: discord.Interaction):

        player = self.game.find_player_by_id(interaction.user.id)

        if not player or not player.playable:
            return

        self.game.deal_cards(player, amount=1)

        if player.total > 21:
            print(f"{player.name} busted")
            player.playable = False

        # Finish the game
        if self.game.all_locked_in():
            self.game.play_dealer()
            self.game.determine_winner()

        await interaction.response.edit_message(embed=self.game.embed, view=self.game.view)
