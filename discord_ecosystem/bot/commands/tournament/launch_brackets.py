import discord


# Ensure we have a correct number of rounds, no empty matches, and no matches with more than two players
def isRoundConform(baseTour: list):
    return (len(baseTour) % 2 == 0 or len(baseTour) == 1) and len([
        nomatch for nomatch in baseTour if len(nomatch) == 0
    ]) == 0 and len([nomatch for nomatch in baseTour if len(nomatch) > 2]) == 0


def determineWinner(pair: list[discord.Member], winner=discord.Member):
    if len(pair) == 1:
        return pair
    if not winner or winner not in pair:
        raise Exception("FUCK IT")
    return [winner]


def makeNextRound(ronde: list):
    nextRound = []
    for i in range(int(len(ronde) / 2)):
        nextRound.append([*ronde[2 * i], *ronde[2 * i + 1]])
    return nextRound
