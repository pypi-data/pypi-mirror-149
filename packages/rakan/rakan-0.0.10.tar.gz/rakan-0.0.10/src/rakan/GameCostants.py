from enum import Enum


class ServerRegion(Enum):
    """Enumation of all the server regions."""
    BR = 'br1'
    """Brazil server"""
    EUNE = 'eun1'
    """Nordic and Eastern European server."""
    EUW = 'euw1'
    """Western European server."""
    LAN = 'la1'
    """Latin America North."""
    LAS = 'la2'
    """Latin America South."""
    NA = 'na1'
    """North American server."""
    OCE = 'oc1'
    """Oceania."""
    RU = 'ru1'
    """Russian server."""
    TUR = 'tr1'
    """Turkey."""
    JAP = 'jp1'
    """Japanese server."""
    KR = 'kr'
    """Korean server."""


class ServerContinent(Enum):
    """Enumation of all the continental regions of League of Legends.
    This are groups of standard regions.
    """
    AMERICAS = 'americas'
    ASIA = 'asia'
    EUROPE = 'europe'


class Seasons(Enum):
    """Enumation of all the seasons in League of Legends."""
    PRESEASON_3 = 0
    SEASON_3 = 1
    PRESEASON_4 = 2
    SEASON_4 = 3
    PRESEASON_5 = 4
    SEASON_5 = 5
    PRESEASON_6 = 6
    SEASON_6 = 7
    PRESEASON_7 = 8
    SEASON_7 = 9
    PRESEASON_8 = 10
    SEASON_8 = 11
    PRESEASON_9 = 12
    SEASON_9 = 13


class Tier(Enum):
    """Enumation of all the tiers in League of Legends."""
    IRON = 'IRON'
    BRONZE = 'BRONZE'
    SILVER = 'SILVER'
    GOLD = 'GOLD'
    PLATINUM = 'PLATINUM'
    DIAMON = 'DIAMOND'
    MASTER = 'MASTER'
    GANDMASTER = 'GRANDMASTER'
    CHALLENGER = 'CHALLENGER'


class Division(Enum):
    """Enumation of all the ranks in League of Legends."""
    ONE = 'I'
    """1"""
    TWO = 'II'
    """2"""
    THREE = 'III'
    """3"""
    FOUR = 'IV'
    """4"""


class Queue(Enum):
    """Enumaton of all the queques."""
    RANKED_SOLO = 'RANKED_SOLO_5x5'
    RANKED_FLEX_SR = 'RANKED_FLEX_SR'
    RANKED_FLEX_TT = 'RANKED_FLEX_TT'


class GameType(Enum):
    """Enumation of all the game types."""
    RANKED = 'ranked'
    NORMAL = 'normal'
    TOURNEY = 'tourney'
    TUTORIAL = 'tutorial'


class MMR_REGION(Enum):
    EUW = 'euw'
    EUNE = 'eune'
    KR = 'kr'
    NA = 'na'


class MMR_QUEUE(Enum):
    RANKED_SOLO = 'ranked'
    NORMAL = 'normal'
    ARAM = 'ARAM'


riot_region_to_mmr_region = {
    ServerRegion.EUW: MMR_REGION.EUW,
    ServerRegion.EUNE: MMR_REGION.EUNE,
    ServerRegion.KR: MMR_REGION.KR,
    ServerRegion.NA: MMR_REGION.NA
}

mmr_queue_to_riot_queue = {
    MMR_QUEUE.RANKED_SOLO: Queue.RANKED_SOLO
}
