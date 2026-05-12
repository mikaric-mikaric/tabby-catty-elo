import requests
import string
import logging
import exception

BASE_URL = "https://open-communication-2026.calicotab.com/api"

session = requests.Session()

def get_custom_request(myURL:str,mytimeout:int=10):
    '''Sends a GET requests, raises alert if status is an error,
    then returns response object, either in default form or in json.'''

    response = session.get(myURL, timeout=mytimeout)
    try:
        response.raise_for_status()
    except Exception as e:
        print(f'Exception while trying to get custom request, exception:/n{e}')
    return response.json()

def get_list_of_tournaments_from_tabbycat(myURL:str,mytimeout:int=10):
    '''Returns a list of tournaments hosted a tabbycat site located on provided URL,
     either in default format or JSON'''
    
    myURL = myURL.rstrip("/") #Strip trailing /
    if myURL.endswith('tournaments'): pass # Section to parse correct URL
    elif myURL.endswith('v1'): myURL+='/tournaments'
    elif myURL.endswith('api'): myURL+='/v1/tournaments'
    else: myURL +='/api/v1/tournaments'

    list_tournamnets_json = get_custom_request(myURL,mytimeout=mytimeout)
    list_tournament_urls = []
    for tournament in list_tournamnets_json:
        list_tournament_urls.append(tournament['url'])
    return list_tournament_urls

def get_link_to_pairing_page_of_round(tournamentURL:str,round_number:int,mytimeout:int=10):
    '''Returns the link to pairing page provided with tournament URL and round number'''
    response_with_round_link = get_custom_request(tournamentURL,mytimeout=mytimeout)['_links']['rounds']
    link = response_with_round_link + f'/{str(round_number)}'
    response_with_pairing_link = get_custom_request(link,mytimeout=mytimeout)['_links']['pairing']
    return response_with_pairing_link

def get_ballot_of_debate(tournamentURL:str,round_number:int,debate_id:int,mytimeout:int=10,efficent:bool=True):
    '''Returns the OBJECT of the ballot of the debate, based on tournament URL, round number and debateid'''
    
    debate_link = get_custom_request(f'{tournamentURL}/rounds/{round_number}/pairings/{debate_id}')
    ballot_link = debate_link['_links']['ballots']
    return get_custom_request(ballot_link,mytimeout=mytimeout)
    
def get_list_of_debate_data_from_round(tournamentURL:str,round_number:int,mytimeout:int=10):
    '''Returns a list of debate IDs, and a list of team IDs that faced each other
    Input:
    tournamentURL: A URL of the tournament
    round_number: the number of the round for which data is to be returned
    inJson: whether data should be in JSON or not
    mytimeout: timeout for the API request
    
    Output:
    debate_ids, list of ints who are ids of debates that happened that round'''

    pairing_link = get_link_to_pairing_page_of_round(tournamentURL=tournamentURL,round_number=round_number,mytimeout=mytimeout)
    response_with_list_of_data = get_custom_request(pairing_link,mytimeout=mytimeout)
    debate_ids = []
    for debate in response_with_list_of_data:
        debate_ids.append(debate['id'])
    return debate_ids



def main():
    '''r = custom_get_request(BASE_URL)
    print("Root:", r)

    v1 = requests.get(f"{BASE_URL}/v1", timeout=10).json()
    print("V1 links:", v1["_links"])

    tournaments = requests.get(v1["_links"]["tournaments"], timeout=10).json()
    print(f"Tournaments found: {len(tournaments)}")

    print('/n')
    print(v1["_links"]["tournaments"])'''

    testURL = input()
    num_of_rounds = 5
    ballot=1
    list_of_tournaments = get_list_of_tournaments_from_tabbycat(testURL)
    for tournament in list_of_tournaments:
        tournament_data = get_custom_request(tournament)
        rounds_base = tournament_data['_links']['rounds']

        for round_num in range(1,num_of_rounds+1):
            debate_ids = (get_list_of_debate_data_from_round(tournament,round_num))
            for debate_id in debate_ids:
                print(get_ballot_of_debate(tournament,round_num,debate_id=debate_id,mytimeout=10))
                print(f'Got ballot No: {ballot}')
                
                ballot+=1



if __name__ == "__main__":
    main()