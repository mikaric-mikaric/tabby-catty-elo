import IO.api as apis
import IO.io as io
import ELOMath.elomath as emat
import Utils.aliasutil as aliasutil
import Utils.ballotutil as ballotutil
import copy

DEFAULT_ELO_VALUE = 1000

def get_speaker_elo_from_speaker_name(speaker_name:str,elo_list:list[list]):
    '''Returns the ELO of a speaker based on their name, if the speaker is not found in the ELO list, returns None'''
    for speaker in elo_list:
        if speaker[0] == speaker_name:
            return speaker[1]
    return False

def get_speaker_debateNo_from_speaker_name(speaker_name:str,elo_list:list[list]):
    '''Returns the ELO of a speaker based on their name, if the speaker is not found in the ELO list, returns None'''
    for speaker in elo_list:
        if speaker[0] == speaker_name:
            return speaker[2]
    return False

def resolveKvalue(k_schedule,debateNo):
    '''Returns the K-value for a given debate number based on the K-schedule'''
    for schedule in k_schedule:
        if int(debateNo) <= int(schedule[1]):
            return int(schedule[0])

def main():
    
    myio = io.IO()
    elo_list=myio.ReturnCurrentELOList()
    alias_list=myio.ReturnCurrentAliasList()
    k_schedule=myio.ReturnCurrentKSchedule()
    print(elo_list)
    input()
    name_util = aliasutil.AliasUtil()

    api = apis.FetchFromTabbyAPI()

    testURL = input("Enter the link to the Tabbycat site containing tournaments you want to scrape... ")
    num_of_rounds = 5
    ballotno=1

    list_of_tournaments = api.get_list_of_tournaments_from_tabbycat(testURL)
    for tournament in list_of_tournaments:
        skip = input(f'Found the tournament {tournament}, should it be processed? [Y/N] ')
        if skip == "Y":
            tournament_data = api.get_custom_request(tournament)
            rounds_base = tournament_data['_links']['rounds']

            for round_num in range(1,num_of_rounds+1):
                print(f'Processing round {round_num} of tournament {tournament}...')
                debate_ids = api.get_list_of_debate_data_from_round(tournament,round_num)
                for debate_id in debate_ids:
                    new_elo_list = copy.deepcopy(elo_list)
                    ballot = api.get_ballot_of_debate(tournament,round_num,debate_id=debate_id)
                    print(f'Got ballot No: {ballotno}')
                    ballot_data = ballotutil.ballot_from_team_unravel(ballotutil.basic_ballot_unravel(ballot))
                    speaker1_oldelo = 0
                    speaker2_oldelo = 0
                    for i in range(4):
                        print(f'Processing ballot No: {ballotno}, team No: {i+1}')
                        team = ballot_data[i]
                        speaker1_name = api.get_speaker_name_from_speaker_link(team[0])
                        speaker1_name = name_util.NormalizeName(speaker1_name)
                        speaker1_oldelo = get_speaker_elo_from_speaker_name(speaker1_name, elo_list)
                        if speaker1_oldelo == False:
                            speaker1_oldelo = DEFAULT_ELO_VALUE
                            elo_list.append([speaker1_name, speaker1_oldelo,1])
                        ballot_data[i][0]= speaker1_name

                        speaker2_name = api.get_speaker_name_from_speaker_link(team[2])
                        speaker2_name = name_util.NormalizeName(speaker2_name)
                        speaker2_oldelo = get_speaker_elo_from_speaker_name(speaker2_name, elo_list)
                        if speaker2_oldelo == False:
                            speaker2_oldelo = DEFAULT_ELO_VALUE
                            elo_list.append([speaker2_name, speaker2_oldelo,1])
                        ballot_data[i][2] = speaker2_name
                        ballot_data[i].append(int(team[1])-int(team[3]))

                    pairs = ballotutil.generate_speaker_pairs_based_on_ballot(ballot_data)
                    for pair in pairs:
                        spk1_oldelo = get_speaker_elo_from_speaker_name(pair[0], elo_list)
                        spk2_oldelo = get_speaker_elo_from_speaker_name(pair[1], elo_list)
                        k_value1 = resolveKvalue(k_schedule, get_speaker_debateNo_from_speaker_name(pair[0], elo_list))
                        k_value2 = resolveKvalue(k_schedule, get_speaker_debateNo_from_speaker_name(pair[1], elo_list))
                        spk1c,spk2c=emat.CalculateELOchange(spk1_oldelo, spk2_oldelo, k_value1, k_value2, pair[-2], pair[-1])
                        emat.UpdateEloList(new_elo_list, pair[0], spk1_oldelo+spk1c)
                        emat.UpdateEloList(new_elo_list, pair[1], spk2_oldelo+spk2c)

                elo_list = copy.deepcopy(new_elo_list)
            print(elo_list)
        else: print(f'Skipping tournament {tournament}!')

if __name__ == "__main__":
    main()