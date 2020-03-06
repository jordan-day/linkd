from riotwatcher import LolWatcher, ApiError

class StatsGrabber():
    """This class can be used to retrieve and parse stats using the LoL API

    """

    _RANKED_QUEUE_IDS = {'Ranked Solo': 420, 'Ranked Flex': 440}
    _UNRANKED_QUEUE_IDS = {'Unranked Draft': 400, 'Unranked Bind': 430}


    def __init__(self, api_key):
        """Constructor
        
        Arguments:
            api_key {str} -- Unique API key to initialize the StatsGrabber class
        """
        self.__api_key = api_key
        try:
            self.watcher = LolWatcher(api_key)
        except ApiError as e:
            print(f'Raised ApiError. Perhaps API Key is wrong? {e}')
    
    def _get_summoner_data(self, name, region):
        return self.watcher.summoner.by_name(region, name)
    
    def _get_matchlist(self, name, region):
        summoner = self._get_summoner_data(name, region)
        match_references = self.watcher.match.matchlist_by_account(region, summoner['accountId'])['matches']
        match_data = []
        # TODO: Remove 10 game limit when dev api is increased
        match_references=match_references[:10]

        for match in match_references:
            match_data.append(self.watcher.match.by_id(region, match['gameId']))
        return match_data

    def _filter_ranked_matches(self, matches):
        return [match for match in matches if match['queueId'] in self._RANKED_QUEUE_IDS.values()]

    def _filter_unranked_matches(self, matches):
        return [match for match in matches if match['queueId'] in self._UNRANKED_QUEUE_IDS.values()]

    def _add_wins_to_matchlist(self, matchlist, name):
        for match in matchlist:
            for participant in match['participantIdentities']:
                if participant['player']['summonerName'] == name:
                    team_id = next(player for player in match['participants'] if player['participantId'] == participant['participantId'])['teamId']
                    break
            match['Win'] = next(x for x in match['teams'] if x['teamId'] == team_id)['win']

    def get_ranked_games(self, name, region='na1'):
        """Returns a list containing all ranked games played by summoner name

        Note: Each entry contains the record of if the game was won or lost
        
        Arguments:
            name {str} -- summoner name
        
        Keyword Arguments:
            region {str} -- region code for summoner (default: {'na1'})
        
        Returns:
            list -- list containing all ranked games played
        """
        raw_matchlist = self._get_matchlist(name, region)
        ranked_matchlist = self._filter_ranked_matches(raw_matchlist)
        self._add_wins_to_matchlist(ranked_matchlist, name)
        return ranked_matchlist

    def get_unranked_games(self, name, region='na1'):
        """Returns a list containing all unranked games played by summoner name

        Note: Each entry contains the record of if the game was won or lost
        
        Arguments:
            name {str} -- summoner name
        
        Keyword Arguments:
            region {str} -- region code for summoner (default: {'na1'})
        
        Returns:
            list -- list containing all unranked games played
        """
        raw_matchlist = self._get_matchlist(name, region)
        unranked_matchlist = self._filter_unranked_matches(raw_matchlist)
        self._add_wins_to_matchlist(unranked_matchlist, name)
        return unranked_matchlist
