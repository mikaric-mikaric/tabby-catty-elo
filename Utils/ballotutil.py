''' Example ballot data structure:
    {
'id': 750795, 
'result': {'sheets': [{'teams': [{'side': 'og', 'points': 2, 'win': False, 'score': 144.0, 'team': 'https://open-communication-2026.calicotab.com/api/v1/tournaments/monopol2026/teams/358478', 'speeches': [{'ghost': False, 'score': 71.0, 'speaker': 'https://open-communication-2026.calicotab.com/api/v1/tournaments/monopol2026/speakers/1236261'}, {'ghost': False, 'score': 73.0, 'speaker': 'https://open-communication-2026.calicotab.com/api/v1/tournaments/monopol2026/speakers/1236260'}]}, {'side': 'oo', 'points': 0, 'win': False, 'score': 138.0, 'team': 'https://open-communication-2026.calicotab.com/api/v1/tournaments/monopol2026/teams/358489', 'speeches': [{'ghost': False, 'score': 70.0, 'speaker': 'https://open-communication-2026.calicotab.com/api/v1/tournaments/monopol2026/speakers/1236284'}, {'ghost': False, 'score': 68.0, 'speaker': 'https://open-communication-2026.calicotab.com/api/v1/tournaments/monopol2026/speakers/1236283'}]}, {'side': 'cg', 'points': 1, 'win': False, 'score': 142.0, 'team': 'https://open-communication-2026.calicotab.com/api/v1/tournaments/monopol2026/teams/358487', 'speeches': [{'ghost': False, 'score': 71.0, 'speaker': 'https://open-communication-2026.calicotab.com/api/v1/tournaments/monopol2026/speakers/1236279'}, {'ghost': False, 'score': 71.0, 'speaker': 'https://open-communication-2026.calicotab.com/api/v1/tournaments/monopol2026/speakers/1236280'}]}, {'side': 'co', 'points': 3, 'win': False, 'score': 148.0, 'team': 'https://open-communication-2026.calicotab.com/api/v1/tournaments/monopol2026/teams/358503', 'speeches': [{'ghost': False, 'score': 75.0, 'speaker': 'https://open-communication-2026.calicotab.com/api/v1/tournaments/monopol2026/speakers/1236311'}, {'ghost': False, 'score': 73.0, 'speaker': 'https://open-communication-2026.calicotab.com/api/v1/tournaments/monopol2026/speakers/1236312'}]}], 'adjudicator': None}]}, 'motion': 'https://open-communication-2026.calicotab.com/api/v1/tournaments/monopol2026/motions/76522', 'url': 'https://open-communication-2026.calicotab.com/api/v1/tournaments/monopol2026/rounds/5/pairings/600599/ballots/750795', 'participant_submitter': None, 'vetos': [], 'timestamp': '2026-04-05T13:16:31.617026+02:00', 'version': 1, 'submitter_type': 'T', 'confirmed': True, 'private_url': False, 'confirm_timestamp': '2026-04-05T13:16:31.754291+02:00', 'discarded': False, 'single_adj': False, 'forfeit': False, 'submitter': 38648, 'confirmer': 38648}]
'''
def basic_ballot_unravel(ballot):
    '''The ballot object from Tabbycat is a list containig a dict and so on, this unravels it to a more usable form, which is a list of dicts, each dict containing the data for one team'''
    first_array_unravaled = ballot[0]
    first_dict_unravaled = first_array_unravaled['result']['sheets'][0]['teams']       
    return first_dict_unravaled

def ballot_from_team_unravel(ballot):
    '''Unravel the ballot data from the team section of the ballot, returns a list of 4 lists, 
    each containing tuples of (speaker, score) for each speech, in order of OG, OO, CG, CO'''
    data = [[] for _ in range(4)]
    #print(ballot)
    for team in ballot:
        index = None
        if team['points'] == '0' or team['points']==0: index = 0
        elif team['points'] == '1' or team['points']==1: index = 1
        elif team['points'] == '2' or team['points']==2: index = 2
        elif team['points'] == '3' or team['points']==3: index = 3
        else: print(f'Error while trying to unravel ballot, team side is not recognized, team data:\n{team}')
        speeches = team['speeches']
        for speech in speeches:
            data[index].extend([speech['speaker'], speech['score']])
        data[index].append(team['points'])
    print(data)
    return data

def generate_speaker_pairs_based_on_ballot(ballot):
    '''Generates pairs of speakers based on the ballot data, returns a list of tuples, each tuple containing the names of two speakers that faced each other'''
    pairs = []
    for i in range(4):
        for j in range(i+1,4):
            pairs.append([ballot[i][0], ballot[j][0], ballot[i][-1], ballot[j][-1]])
            pairs.append([ballot[i][2], ballot[j][2], -ballot[i][-1], -ballot[j][-1]])
            pairs.append([ballot[i][0], ballot[j][2], ballot[i][-1], -ballot[j][-1]])
            pairs.append([ballot[i][2], ballot[j][0], -ballot[i][-1], ballot[j][-1]])
    print(pairs)
    input()
    return pairs