import cyrtranslit

class AliasUtil:
    def __init__(self):
        pass

    @staticmethod
    def _NormalizeToTwoWords(name:str):
        '''Normalizes a name to two words, if it is more than two words, it takes the first and the last word,
        if it is one word, it duplicates it.'''
        
        name = name.strip()
        name_parts = name.split()
        return name_parts[0] + " " + name_parts[-1]

    @staticmethod
    def _NormalizeToLatin(name:str):
        '''Transliterates a name to Latin script, if it is not already in Latin script.'''
        return cyrtranslit.to_latin(name, "sr")

    @staticmethod
    def _NormalizeDoubleLetters(name:str):
        mapping = { "Đ": "Dj", "đ": "dj", "Č": "C", "č": "c", "Ć": "C", "ć": "c", "Š": "S", "š": "s", "Ž": "Z", "ž": "z" }
        table = str.maketrans(mapping)
        return name.translate(table)

    @staticmethod
    def NormalizeName(name:str):
        name = AliasUtil._NormalizeToTwoWords(name)
        name = AliasUtil._NormalizeToLatin(name)
        name = AliasUtil._NormalizeDoubleLetters(name)
        return name