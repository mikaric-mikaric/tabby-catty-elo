import requests


class FetchFromTabbyAPI:

    timeout = 10
    session = None

    def __init__(self,timeout:int=10):
        self.timeout = timeout
        self.session = requests.Session()
        
    def get_custom_request(self,myURL:str):
        '''Sends a GET request, raises alert if status is an error,
        then returns a response object, either in default form or in json.'''

        response = self.session.get(myURL,timeout=self.timeout)
        try:
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'Exception while trying to get custom request, exception:\n{e}')

    def get_list_of_tournaments_from_tabbycat(self,myURL:str):
        '''Returns a list of tournaments hosted a tabbycat site located on provided URL,
        either in default format or JSON'''
        
        myURL = myURL.rstrip("/") #Strip trailing /
        if myURL.endswith('tournaments'): pass # Section to parse correct URL
        elif myURL.endswith('v1'): myURL+='/tournaments'
        elif myURL.endswith('api'): myURL+='/v1/tournaments'
        else: myURL +='/api/v1/tournaments'

        list_tournamnets_json = self.get_custom_request(myURL)
        list_tournament_urls = []
        for tournament in list_tournamnets_json:
            list_tournament_urls.append(tournament['url'])
        return list_tournament_urls

    def get_link_to_pairing_page_of_round(self,tournamentURL:str,round_number:int):
        '''Returns the link to pairing page provided with tournament URL and round number'''
        
        response_with_round_link = self.get_custom_request(tournamentURL)['_links']['rounds']
        link = response_with_round_link + f'/{str(round_number)}'
        response_with_pairing_link = self.get_custom_request(link)['_links']['pairing']
        return response_with_pairing_link

    def get_ballot_of_debate(self,tournamentURL:str,round_number:int,debate_id:int):
        '''Returns the OBJECT of the ballot of the debate, based on tournament URL, round number and debateid'''
        
        debate_link = self.get_custom_request(f'{tournamentURL}/rounds/{round_number}/pairings/{debate_id}')
        ballot_link = debate_link['_links']['ballots']
        ballot_data = self.get_custom_request(ballot_link)

        return ballot_data

        
    def get_list_of_debate_data_from_round(self,tournamentURL:str,round_number:int):
        '''Returns a list of debate IDs, and a list of team IDs that faced each other
        Input:
        tournamentURL: A URL of the tournament
        round_number: the number of the round for which data is to be returned
        inJson: whether data should be in JSON or not
        
        Output:
        debate_ids, list of ints who are ids of debates that happened that round'''

        pairing_link = self.get_link_to_pairing_page_of_round(tournamentURL=tournamentURL,round_number=round_number)
        response_with_list_of_data = self.get_custom_request(pairing_link)
        debate_ids = []
        for debate in response_with_list_of_data:
            debate_ids.append(debate['id'])
        return debate_ids
    
    def get_speaker_name_from_speaker_link(self,speaker_link:str):
        '''Returns the name of the speaker based on the link to the speaker'''
        response = self.get_custom_request(speaker_link)
        return response['name']