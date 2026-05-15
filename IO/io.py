import csv
from pathlib import Path

class IO:

    ELO_CSV_HEADER = ['Name','ELO Rating','Matches on record']
    ALIAS_CSV_HEADER = ['Original Name in ELO list','Alias']

    def __init__(self,listfilename:str="elo_list.csv",aliasfilename:str='aliases.csv',newlistfilename:str='new_elo_list.csv',kfactorfilename:str='k_factor_schedule.csv'):
        self.BASE_DIR = Path(__file__).resolve().parents[1]
        self.ELOLISTFILENAME = listfilename
        self.ALIASFILENAME = aliasfilename
        self.NEWELOLISTFILENAME = newlistfilename
        self.KFACTORFILENAME = kfactorfilename
        self.ELO_DIR = self.BASE_DIR / "LocalData" / "LocalCSV"

    def _ReturnFileInLocalCSV(self,filename:str):
        '''Returns the contents of the specified CSV file in an array form, always skipping the first (header) row'''
        
        elo_file = self.ELO_DIR / filename
        with open(elo_file,newline='',encoding='utf-8-sig') as csvfile:
            elo_reader = csv.reader(csvfile, dialect="excel")
            next(elo_reader,None) #Skip row
            return list(elo_reader)
    
    def ReturnCurrentELOList(self):
        '''Returns current ELO list in array of arrays form, where each sub-array has the structure specified in original .CSV file'''
        return self._ReturnFileInLocalCSV(self.ELOLISTFILENAME)

    def ReturnCurrentAliasList(self):
        '''Returns the name alias list in the form of array, based on the original .CSV file'''
        return self._ReturnFileInLocalCSV(self.ALIASFILENAME)
    
    def ReturnCurrentKSchedule(self):
        '''Returns the K-factor schedule based on the number of debates'''
        return self._ReturnFileInLocalCSV(self.KFACTORFILENAME)

    def _WriteNewFile(self,rows:list[list[str]],csvfilename:str):
        '''Writes arbitrary rows in the specified CSV'''
        file = self.ELO_DIR / csvfilename
        with open(file, 'w',newline='') as csvfile:
            writer = csv.writer(csvfile, dialect="excel")
            writer.writerows(rows)

    def WriteNewELOList(self,rows:list[list[str]]):
        '''Writes new ELO list as a .CSV file, adding appropriate header at the top'''
        rows.insert(0,self.ELO_CSV_HEADER)
        self._WriteNewFile(rows,self.NEWELOLISTFILENAME)

    def WriteNewAliases(self,rows:list[list[str]]):
        '''Writes new Alias list to a .CSV file, adding appropriate header at the top'''
        rows.insert(0,self.ALIAS_CSV_HEADER)
        self._WriteNewFile(rows,self.ALIAS_FILENAME)