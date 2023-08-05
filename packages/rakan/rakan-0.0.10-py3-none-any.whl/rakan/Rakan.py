from . import Xayah
from . import GameCostants
from . import Globals
import json


def set_riot_api_key(riot_api_key: str):
    Globals.riot_api_key = riot_api_key


class Summoner:
    __summoner_boring_info = {
        'name': str,
        'account_id': str,
        'summoner_id': str,
        'puuid': str,
        'region': GameCostants.ServerRegion
    }

    def __init__(self, name: str, region: GameCostants.ServerRegion):
        riot_api = Xayah.RiotAPI(Globals.riot_api_key)
        boring_data = json.loads(riot_api.get_summoner_by_name(name, region))
        self.__summoner_boring_info['name'] = boring_data['name']
        self.__summoner_boring_info['account_id'] = boring_data['accountId']
        self.__summoner_boring_info['summoner_id'] = boring_data['id']
        self.__summoner_boring_info['puuid'] = boring_data['puuid']
        self.__summoner_boring_info['region'] = region

    def get_ranked_info(self):
        riot_api = Xayah.RiotAPI(Globals.riot_api_key)
        raw_riot_data = json.loads(riot_api.get_all_ranked_stats_by_summoner_id(
            summoner_id=self.__summoner_boring_info['summoner_id'],
            region=self.__summoner_boring_info['region'],
        ))

        mmr_api = Xayah.MMR_API()

        raw_mmr_data = json.loads(mmr_api.get_summoner_mmr_info(
            summoner_name=self.__summoner_boring_info['name'],
            region=GameCostants.riot_region_to_mmr_region[self.__summoner_boring_info['region']],
        ))

        final_data = dict()

        for queue in raw_riot_data:
            final_data[GameCostants.Queue(queue['queueType'])] = {
                'tier': GameCostants.Tier(queue['tier']),
                'rank': GameCostants.Division(queue['rank']),
                'points': queue['leaguePoints'],
                'wins': queue['wins'],
                'losses': queue['losses'],
                'winrate': queue['wins'] * 100 / (queue['wins'] + queue['losses']),
                'hot_streak': queue['hotStreak'],
                'inactive': queue['inactive'],
                'veteran': queue['veteran'],
                'fresh_blood': queue['freshBlood'],
            }

        if GameCostants.MMR_QUEUE.RANKED_SOLO.value in raw_mmr_data.keys() and GameCostants.Queue.RANKED_SOLO in final_data.keys():
            final_data[GameCostants.Queue.RANKED_SOLO]['mmr'] = raw_mmr_data[GameCostants.MMR_QUEUE.RANKED_SOLO.value]['avg']
            final_data[GameCostants.Queue.RANKED_SOLO]['percentile'] = raw_mmr_data[GameCostants.MMR_QUEUE.RANKED_SOLO.value]['percentile']
            final_data[GameCostants.Queue.RANKED_SOLO]['error'] = raw_mmr_data[GameCostants.MMR_QUEUE.RANKED_SOLO.value]['err']
            final_data[GameCostants.Queue.RANKED_SOLO]['expected_tier'],
            final_data[GameCostants.Queue.RANKED_SOLO]['expected_rank'] = raw_mmr_data[GameCostants.MMR_QUEUE.RANKED_SOLO.value]['closestRank'].split(
                ' ')
            final_data[GameCostants.Queue.RANKED_SOLO]['expected_tier'] = GameCostants.Tier(final_data[GameCostants.Queue.RANKED_SOLO]['expected_tier'].upper())
            final_data[GameCostants.Queue.RANKED_SOLO]['expected_rank'] = GameCostants.Division(final_data[GameCostants.Queue.RANKED_SOLO]['expected_rank'])
        return final_data
