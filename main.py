import IO.api as apis
import IO.io as io
import ELOMath.elomath as emat
def main():
    
    myio = io.IO("elo_list_test.csv")
    elo=myio.ReturnCurrentELOList()
    myio.WriteNewELOList(elo)
    '''
    api = apis.FetchFromTabbyAPI()
    testURL = input("Enter the link to the Tabbycat site containing tournaments you want to scrape... ")
    num_of_rounds = 5a
    ballot=1
    list_of_tournaments = api.get_list_of_tournaments_from_tabbycat(testURL)
    for tournament in list_of_tournaments:
        skip = input(f'Found the tournament {tournament}, should it be processed? [Y/N] ')
        if skip == "Y":
            tournament_data = api.get_custom_request(tournament)
            rounds_base = tournament_data['_links']['rounds']

            for round_num in range(1,num_of_rounds+1):
                debate_ids = api.get_list_of_debate_data_from_round(tournament,round_num)
                for debate_id in debate_ids:
                    print(api.get_ballot_of_debate(tournament,round_num,debate_id=debate_id))
                    print(f'Got ballot No: {ballot}')
                    
                    ballot+=1
        else: print(f'Skipping tournament {tournament}!')
'''

if __name__ == "__main__":
    main()