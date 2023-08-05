import platform
import requests
import json
from . import LowLevelErrors
from . import GameCostants


class RiotAPI:
    __api_token: str

    def __init__(self, api_token: str) -> None:
        self.__api_token = api_token

    def __make_request(self, url: str):
        header_data = {
            'X-Riot-Token': self.__api_token
        }
        response = requests.get(url=url, headers=header_data)
        match(int(response.status_code)):
            case 400:
                raise LowLevelErrors.BadRequest
            case 401:
                raise LowLevelErrors.Unauthorized
            case 403:
                raise LowLevelErrors.Forbidden
            case 404:
                raise LowLevelErrors.NotFound
            case 415:
                raise LowLevelErrors.UnsupportedMediaType
            case 429:
                raise LowLevelErrors.RateLimiExceeded
            case 500:
                raise LowLevelErrors.InternalServerError
            case 503:
                raise LowLevelErrors.ServiceUnavailable
            case 200:
                return json.dumps(response.json())
            case _:
                raise LowLevelErrors.UnknowError

    def get_matches_by_puuid(self, continent: GameCostants.ServerContinent, puuid: str, start_time: int, end_time: int, game_type: GameCostants.GameType, start: int = 0, count: int = 20):
        url = f'https://{continent.value}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={start_time}&endTime={end_time}&type={game_type.value}&start={start}&count={count}'
        return self.__make_request(url=url)

    def get_match_by_match_id(self, continent: GameCostants.ServerContinent, match_id: str):
        url = f'https://{continent.value}.api.riotgames.com/lol/match/v5/matches/{match_id}'
        return self.__make_request(url=url)

    def get_match_timeline_by_match_id(self, continent: GameCostants.ServerContinent, match_id: str):
        url = f'https://{continent.value}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline'
        return self.__make_request(url=url)

    def get_champion_mastery_by_summoner_id(self, summoner_id: str, region: GameCostants.ServerRegion):
        url = f'https://{region.value}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}'
        return self.__make_request(url=url)

    def get_champion_mastery_by_summoner_id_and_champion_id(self, summoner_id: str, champion_id: int, region: GameCostants.ServerRegion):
        url = f'https://{region.value}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}/by-champion/{champion_id}'
        return self.__make_request(url=url)

    def get_summoner_mastery_score(self, summoner_id: str, region: GameCostants.ServerRegion):
        url = f'https://{region.value}.api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/{summoner_id}'
        return self.__make_request(url=url)

    def get_champion_rotation(self, region: GameCostants.ServerRegion):
        url = f'https://{region.value}.api.riotgames.com/lol/platform/v3/champion-rotations'
        return self.__make_request(url=url)

    def get_challenger_league(self, queque: GameCostants.Queue, region: GameCostants.ServerRegion):
        url = f'https://{region.value}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{queque.value}'
        return self.__make_request(url=url)

    def get_grandmaster_league(self, queque: GameCostants.Queue, region: GameCostants.ServerRegion):
        url = f'https://{region.value}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{queque.value}'
        return self.__make_request(url=url)

    def get_master_league(self, queque: GameCostants.Queue, region: GameCostants.ServerRegion):
        url = f'https://{region.value}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{queque.value}'
        return self.__make_request(url=url)

    def get_all_ranked_stats_by_summoner_id(self, summoner_id: str, region: GameCostants.ServerRegion):
        url = f'https://{region.value}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}'
        return self.__make_request(url=url)

    def get_all_summoners_by_division_tier_queque(self, region: GameCostants.ServerRegion, division: GameCostants.Division, tier: GameCostants.Tier, queque: GameCostants.Queue, page: int = 1):
        url = f'https://{region.value}.api.riotgames.com/lol/league/v4/entries/{queque.value}/{tier.value}/{division.value}?page={page}'
        return self.__make_request(url=url)

    def get_server_status(self, region: GameCostants.ServerRegion):
        url = f'https://{region.value}.api.riotgames.com/lol/status/v4/platform-data'
        return self.__make_request(url=url)

    def get_in_game_info_by_summoner_id(self, summoner_id: str, region: GameCostants.ServerRegion):
        url = f'https://{region.value}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}'
        return self.__make_request(url=url)

    def get_summoner_by_summoner_id(self, summoner_id: str, region: GameCostants.ServerRegion):
        url = f'https://{region.value}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}'
        return self.__make_request(url=url)

    def get_summoner_by_name(self, name: str, region: GameCostants.ServerRegion):
        url = f'https://{region.value}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}'
        return self.__make_request(url=url)

    def get_summoner_by_puuid(self, puuid: str, region: GameCostants.ServerRegion):
        url = f'https://{region.value}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}'
        return self.__make_request(url=url)

    def get_summoner_by_account_id(self, account_id: str, region: GameCostants.ServerRegion):
        url = f'https://{region.value}.api.riotgames.com/lol/summoner/v4/summoners/by-account/{account_id}'
        return self.__make_request(url=url)


class MMR_API:
    user_agent_string = f'{platform.system()}:rakan_python_package:0.0.10'

    def __init__(self) -> None:
        pass

    def get_summoner_mmr_info(self, summoner_name: str,  region: GameCostants.MMR_REGION):
        url = f'https://{region.value}.whatismymmr.com/api/v1/summoner?name={summoner_name}'
        response = requests.get(url)
        match(response.status_code):
            case 0:
                raise LowLevelErrors.InternalServerError
            case 1:
                raise LowLevelErrors.InternalServerError
            case 100:
                raise LowLevelErrors.BadRequest
            case 101:
                raise LowLevelErrors.NoMMRData
            case 200:
                return json.dumps(response.json())
            case 9001:
                raise LowLevelErrors.RateLimiExceeded
            case _:
                raise LowLevelErrors.UnknowError
