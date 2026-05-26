""" Component which holds any number of buttons with each a link to a url

"""
import discord


class LinksButtonView(discord.ui.View):
    """class LinksButtonView

        a generic class which transform a pair of label / url into buttons for a view

    Args:
        links: a list of tuples where first item is the label, second is the url
        link : ("un lien super", "https://sefairepirater.ch")
    """

    def __init__(self, links: list[tuple[str, str]]):
        super().__init__()
        for link in links:
            self.add_item(discord.ui.Button(label=link[0], url=link[1]))
