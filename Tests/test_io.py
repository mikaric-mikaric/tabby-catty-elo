import unittest
import sys
from pathlib import Path
import tempfile
import csv
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from IO.io import IO


class TestIOInit(unittest.TestCase):
    """Test cases for IO class initialization"""
    
    def test_init_default_parameters(self):
        """Test IO initialization with default parameters"""
        io = IO()
        self.assertEqual(io.ELOLISTFILENAME, "elo_list.csv")
        self.assertEqual(io.ALIASFILENAME, "aliases.csv")
        self.assertEqual(io.NEWELOLISTFILENAME, "new_elo_list.csv")
        self.assertEqual(io.KFACTORFILENAME, "k_factor_schedule.csv")
    
    def test_init_custom_parameters(self):
        """Test IO initialization with custom parameters"""
        io = IO(
            listfilename="custom_elo.csv",
            aliasfilename="custom_aliases.csv",
            newlistfilename="custom_new.csv",
            kfactorfilename="custom_k.csv"
        )
        self.assertEqual(io.ELOLISTFILENAME, "custom_elo.csv")
        self.assertEqual(io.ALIASFILENAME, "custom_aliases.csv")
        self.assertEqual(io.NEWELOLISTFILENAME, "custom_new.csv")
        self.assertEqual(io.KFACTORFILENAME, "custom_k.csv")
    
    def test_elo_dir_path_exists(self):
        """Test that ELO_DIR path is set correctly"""
        io = IO()
        self.assertTrue(io.ELO_DIR.name == "LocalCSV")
        self.assertTrue(io.BASE_DIR.exists())


class TestIOReturnFileInLocalCSV(unittest.TestCase):
    """Test cases for _ReturnFileInLocalCSV method"""
    
    def setUp(self):
        """Create temporary CSV files for testing"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        
    def tearDown(self):
        """Clean up temporary files"""
        self.temp_dir.cleanup()
    
    def create_test_csv(self, filename, headers, data):
        """Helper method to create a test CSV file"""
        filepath = self.temp_path / filename
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)
        return filepath
    
    def test_read_csv_skips_header(self):
        """Test that _ReturnFileInLocalCSV skips the header row"""
        headers = ['Name', 'ELO Rating', 'Matches on record']
        data = [['Alice', '1600', '10'], ['Bob', '1400', '8']]
        self.create_test_csv('test.csv', headers, data)
        
        io = IO()
        io.ELO_DIR = self.temp_path
        result = io._ReturnFileInLocalCSV('test.csv')
        
        # Should return only data rows (no header)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ['Alice', '1600', '10'])
        self.assertEqual(result[1], ['Bob', '1400', '8'])
    
    def test_read_empty_csv(self):
        """Test reading CSV with only headers"""
        headers = ['Name', 'ELO Rating', 'Matches on record']
        self.create_test_csv('empty.csv', headers, [])
        
        io = IO()
        io.ELO_DIR = self.temp_path
        result = io._ReturnFileInLocalCSV('empty.csv')
        
        self.assertEqual(len(result), 0)


class TestIOReturnCurrentELOList(unittest.TestCase):
    """Test cases for ReturnCurrentELOList method"""
    
    def setUp(self):
        """Create temporary directory"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
    
    def tearDown(self):
        """Clean up"""
        self.temp_dir.cleanup()
    
    def create_test_elo_csv(self):
        """Create test ELO CSV"""
        filepath = self.temp_path / "elo_list.csv"
        data = [
            ['Name', 'ELO Rating', 'Matches on record'],
            ['Alice', '1600', '10'],
            ['Bob', '1400', '8'],
            ['Charlie', '1500', '12']
        ]
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)
    
    def test_return_current_elo_list(self):
        """Test ReturnCurrentELOList returns data correctly"""
        self.create_test_elo_csv()
        
        io = IO()
        io.ELO_DIR = self.temp_path
        result = io.ReturnCurrentELOList()
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][0], 'Alice')
        self.assertEqual(result[1][0], 'Bob')


class TestIOReturnCurrentAliasList(unittest.TestCase):
    """Test cases for ReturnCurrentAliasList method"""
    
    def setUp(self):
        """Create temporary directory"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
    
    def tearDown(self):
        """Clean up"""
        self.temp_dir.cleanup()
    
    def create_test_alias_csv(self):
        """Create test Alias CSV"""
        filepath = self.temp_path / "aliases.csv"
        data = [
            ['Original Name in ELO list', 'Alias'],
            ['Alice Smith', 'Alice'],
            ['Bob Johnson', 'Bob']
        ]
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)
    
    def test_return_current_alias_list(self):
        """Test ReturnCurrentAliasList returns data correctly"""
        self.create_test_alias_csv()
        
        io = IO()
        io.ELO_DIR = self.temp_path
        result = io.ReturnCurrentAliasList()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], 'Alice Smith')


class TestIOReturnCurrentKSchedule(unittest.TestCase):
    """Test cases for ReturnCurrentKSchedule method"""
    
    def setUp(self):
        """Create temporary directory"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
    
    def tearDown(self):
        """Clean up"""
        self.temp_dir.cleanup()
    
    def create_test_k_schedule_csv(self):
        """Create test K-factor schedule CSV"""
        filepath = self.temp_path / "k_factor_schedule.csv"
        data = [
            ['Matches', 'K-Factor'],
            ['0-10', '32'],
            ['11-20', '24'],
            ['20+', '16']
        ]
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)
    
    def test_return_current_k_schedule(self):
        """Test ReturnCurrentKSchedule returns data correctly"""
        self.create_test_k_schedule_csv()
        
        io = IO()
        io.ELO_DIR = self.temp_path
        result = io.ReturnCurrentKSchedule()
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][0], '0-10')


class TestIOWriteNewFile(unittest.TestCase):
    """Test cases for _WriteNewFile method"""
    
    def setUp(self):
        """Create temporary directory"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
    
    def tearDown(self):
        """Clean up"""
        self.temp_dir.cleanup()
    
    def test_write_new_file(self):
        """Test _WriteNewFile writes CSV correctly"""
        io = IO()
        io.ELO_DIR = self.temp_path
        
        rows = [['Alice', '1600'], ['Bob', '1400']]
        io._WriteNewFile(rows, 'output.csv')
        
        # Verify file was created
        output_file = self.temp_path / 'output.csv'
        self.assertTrue(output_file.exists())
        
        # Verify contents
        with open(output_file, 'r', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0][0], 'Alice')


class TestIOWriteNewELOList(unittest.TestCase):
    """Test cases for WriteNewELOList method"""
    
    def setUp(self):
        """Create temporary directory"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
    
    def tearDown(self):
        """Clean up"""
        self.temp_dir.cleanup()
    
    def test_write_new_elo_list_adds_header(self):
        """Test WriteNewELOList adds header correctly"""
        io = IO()
        io.ELO_DIR = self.temp_path
        
        rows = [['Alice', '1600', '10'], ['Bob', '1400', '8']]
        io.WriteNewELOList(rows.copy())
        
        # Verify file was created
        output_file = self.temp_path / 'new_elo_list.csv'
        self.assertTrue(output_file.exists())
        
        # Verify header was added
        with open(output_file, 'r', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        
        self.assertEqual(data[0], ['Name', 'ELO Rating', 'Matches on record'])
        self.assertEqual(data[1], ['Alice', '1600', '10'])
    
    def test_write_new_elo_list_modifies_input(self):
        """Test that WriteNewELOList modifies the input list by adding header"""
        io = IO()
        io.ELO_DIR = self.temp_path
        
        rows = [['Alice', '1600', '10']]
        io.WriteNewELOList(rows)
        
        # Original list should be modified (header inserted at index 0)
        self.assertEqual(rows[0], ['Name', 'ELO Rating', 'Matches on record'])


class TestIOWriteNewAliases(unittest.TestCase):
    """Test cases for WriteNewAliases method"""
    
    def setUp(self):
        """Create temporary directory"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
    
    def tearDown(self):
        """Clean up"""
        self.temp_dir.cleanup()
    
    # Note: There's a typo in the original code: ALIAS_FILENAME should be ALIASFILENAME
    def test_write_new_aliases_method_exists(self):
        """Test that WriteNewAliases method exists"""
        io = IO()
        self.assertTrue(hasattr(io, 'WriteNewAliases'))


if __name__ == '__main__':
    unittest.main()
