def CalculateELOexpectation(ratingA:float,ratingB:float):
    '''Calculated the expectation that the player A or B should win depending on their ratings.
    Returns result in the format of two floats, the first being player A's probability of winning, the second player B's'''

    ExpectationA = 1 / (1+pow(10,(ratingB-ratingA)/400))
    return ExpectationA,1-ExpectationA # This can be done because Expectation A + Expectation B = 1 always

def SpeakerDifferenceFactor(won:bool,spk_diff:int):
    '''Returns speaker difference factor adjustment for ELO between 0.1 and 1.9,
    based on whether the debater won and the amount they outspoke their partner by.'''
    return max(min(1.9,1+spk_diff/10),0.1) if won else min(max(0.1,1-spk_diff/10),1.9) 

def CalculateELOchange(ratingA:float,ratingB:float,kA:int,kB:int,spk_diffA:int,spk_diffB:int):
    '''Calculate the change of elo' for player's A and B, where player A beat plater B.
    
    Input:
    rating A, rating B: Player's/Debaters ELO ratings before the debate;
    kA, kB: K-factors for the players A and B, determines how much ratings are adjusted per debate.
    spk_diffA, spkdiffB: how much debaters A and B OUTSPOKE their partners by
    
    Output:
    RatingDifferenceA,RatingDifferenceB'''
    ExpectationA, ExpectationB = CalculateELOexpectation(ratingA,ratingB)
    spk_diff_factorA, spk_diff_factorB = SpeakerDifferenceFactor(True,spk_diffA),SpeakerDifferenceFactor(False,spk_diffB)
    return spk_diff_factorA*kA*(1-ExpectationA), spk_diff_factorB*kB*(0-ExpectationB)

def CalculateNewELO(ratingA:float,ratingB:float,kA:int,kB:int,spk_diffA:int,spk_diffB:int):
    '''Calculate the new elo' for player's A and B, where player A beat plater B.
    
    Input:
    rating A, rating B: Player's/Debaters ELO ratings before the debate;
    kA, kB: K-factors for the players A and B, determines how much ratings are adjusted per debate.
    spk_diffA, spkdiffB: how much debaters A and B OUTSPOKE their partners by
    
    Output:
    NewRatingA,NewRatingB'''
    changeA, changeB = CalculateELOchange(ratingA,ratingB,kA,kB,spk_diffA,spk_diffB)
    return ratingA + changeA , ratingB + changeB