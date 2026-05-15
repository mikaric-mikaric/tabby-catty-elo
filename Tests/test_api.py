import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, call
import requests

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from IO.api import FetchFromTabbyAPI


class TestFetchFromTabbyAPIInit(unittest.TestCase):
    """Test cases for FetchFromTabbyAPI class initialization"""
    
    def test_init_default_timeout(self):
        """Test initialization with default timeout"""
        api = FetchFromTabbyAPI()
        self.assertEqual(api.timeout, 10)
        self.assertIsNotNone(api.session)
    
    def test_init_custom_timeout(self):
        """Test initialization with custom timeout"""
        api = FetchFromTabbyAPI(timeout=20)
        self.assertEqual(api.timeout, 20)
    
    def test_session_is_requests_session(self):
        """Test that session is a requests.Session instance"""
        api = FetchFromTabbyAPI()
        self.assertIsInstance(api.session, requests.Session)


class TestGetCustomRequest(unittest.TestCase):
    """Test cases for get_custom_request method"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.api = FetchFromTabbyAPI()
    
    @patch.object(FetchFromTabbyAPI, 'session')
    def test_get_custom_request_success(self, mock_session):
        """Test successful GET request"""
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'test'}
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response
        
        api = FetchFromTabbyAPI()
        api.session = mock_session
        result = api.get_custom_request("http://example.com/api")
        
        self.assertEqual(result, {'data': 'test'})
        mock_session.get.assert_called_once()
    
    @patch.object(FetchFromTabbyAPI, 'session')
    def test_get_custom_request_uses_timeout(self, mock_session):
        """Test that get_custom_request uses the configured timeout"""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_session.get.return_value = mock_response
        
        api = FetchFromTabbyAPI(timeout=15)
        api.session = mock_session
        api.get_custom_request("http://example.com")
        
        mock_session.get.assert_called_once_with("http://example.com", timeout=15)
    
    @patch.object(FetchFromTabbyAPI, 'session')
    def test_get_custom_request_handles_error(self, mock_session):
        """Test that get_custom_request handles HTTP errors gracefully"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_session.get.return_value = mock_response
        
        # Should not raise exception, but print error
        result = self.api.get_custom_request("http://example.com/invalid")
        self.assertIsNone(result)
    
    @patch.object(FetchFromTabbyAPI, 'session')
    def test_get_custom_request_timeout_error(self, mock_session):
        """Test that get_custom_request handles timeout errors"""
        mock_session.get.side_effect = requests.exceptions.Timeout("Request timeout")
        
        result = self.api.get_custom_request("http://example.com")
        self.assertIsNone(result)


class TestGetListOfTournamentsFromTabbycat(unittest.TestCase):
    """Test cases for get_list_of_tournaments_from_tabbycat method"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.api = FetchFromTabbyAPI()
    
    @patch.object(FetchFromTabbyAPI, 'get_custom_request')
    def test_url_normalization_removes_trailing_slash(self, mock_request):
        """Test that trailing slash is removed from URL"""
        mock_request.return_value = []
        
        self.api.get_list_of_tournaments_from_tabbycat("http://example.com/")
        
        # Check that the URL passed was normalized
        call_args = mock_request.call_args_list
        self.assertTrue(any('http://example.com/api/v1/tournaments' in str(arg) 
                          for arg in call_args))
    
    @patch.object(FetchFromTabbyAPI, 'get_custom_request')
    def test_url_ends_with_tournaments(self, mock_request):
        """Test URL that already ends with 'tournaments'"""
        mock_request.return_value = []
        
        self.api.get_list_of_tournaments_from_tabbycat("http://example.com/tournaments")
        
        # Should not add more to URL
        call_args = mock_request.call_args_list
        # The URL should still be correct even if it already ends with tournaments
        self.assertTrue(len(call_args) > 0)
    
    @patch.object(FetchFromTabbyAPI, 'get_custom_request')
    def test_url_ends_with_v1(self, mock_request):
        """Test URL that ends with 'v1'"""
        mock_request.return_value = []
        
        self.api.get_list_of_tournaments_from_tabbycat("http://example.com/v1")
        
        # Should append /tournaments
        call_args = str(mock_request.call_args_list)
        self.assertIn('/tournaments', call_args)
    
    @patch.object(FetchFromTabbyAPI, 'get_custom_request')
    def test_url_ends_with_api(self, mock_request):
        """Test URL that ends with 'api'"""
        mock_request.return_value = []
        
        self.api.get_list_of_tournaments_from_tabbycat("http://example.com/api")
        
        # Should append /v1/tournaments
        call_args = str(mock_request.call_args_list)
        self.assertIn('api/v1/tournaments', call_args)
    
    @patch.object(FetchFromTabbyAPI, 'get_custom_request')
    def test_returns_list_of_tournament_urls(self, mock_request):
        """Test that method returns list of tournament URLs"""
        mock_tournaments = [
            {'url': 'http://example.com/api/v1/tournaments/1'},
            {'url': 'http://example.com/api/v1/tournaments/2'},
            {'url': 'http://example.com/api/v1/tournaments/3'}
        ]
        mock_request.return_value = mock_tournaments
        
        result = self.api.get_list_of_tournaments_from_tabbycat("http://example.com")
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], 'http://example.com/api/v1/tournaments/1')
        self.assertEqual(result[1], 'http://example.com/api/v1/tournaments/2')


class TestGetLinkToPairingPageOfRound(unittest.TestCase):
    """Test cases for get_link_to_pairing_page_of_round method"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.api = FetchFromTabbyAPI()
    
    @patch.object(FetchFromTabbyAPI, 'get_custom_request')
    def test_get_link_to_pairing_page(self, mock_request):
        """Test getting link to pairing page"""
        # First call returns tournament with rounds link
        # Second call returns round with pairing link
        mock_request.side_effect = [
            {'_links': {'rounds': 'http://example.com/api/v1/tournaments/1/rounds'}},
            {'_links': {'pairing': 'http://example.com/api/v1/tournaments/1/rounds/1/pairings'}}
        ]
        
        result = self.api.get_link_to_pairing_page_of_round(
            "http://example.com/api/v1/tournaments/1", 
            round_number=1
        )
        
        self.assertEqual(result, 'http://example.com/api/v1/tournaments/1/rounds/1/pairings')
        self.assertEqual(mock_request.call_count, 2)
    
    @patch.object(FetchFromTabbyAPI, 'get_custom_request')
    def test_get_link_correct_round_number_construction(self, mock_request):
        """Test that round number is correctly added to URL"""
        mock_request.side_effect = [
            {'_links': {'rounds': 'http://example.com/api/v1/tournaments/1/rounds'}},
            {'_links': {'pairing': 'http://example.com/api/v1/tournaments/1/rounds/3/pairings'}}
        ]
        
        self.api.get_link_to_pairing_page_of_round(
            "http://example.com/api/v1/tournaments/1",
            round_number=3
        )
        
        # Check that second call includes round 3
        calls = mock_request.call_args_list
        self.assertIn('3', str(calls[1]))


class TestGetBallotOfDebate(unittest.TestCase):
    """Test cases for get_ballot_of_debate method"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.api = FetchFromTabbyAPI()
    
    @patch.object(FetchFromTabbyAPI, 'get_custom_request')
    def test_get_ballot_of_debate(self, mock_request):
        """Test getting ballot of a debate"""
        # First call returns debate with ballots link
        # Second call returns ballot data
        ballot_data = {
            'id': 1,
            'result': 'Winner A',
            'scores': [74, 73]
        }
        mock_request.side_effect = [
            {'_links': {'ballots': 'http://example.com/api/v1/tournaments/1/rounds/1/pairings/1/ballots'}},
            ballot_data
        ]
        
        result = self.api.get_ballot_of_debate(
            "http://example.com/api/v1/tournaments/1",
            round_number=1,
            debate_id=1
        )
        
        self.assertEqual(result, ballot_data)
        self.assertEqual(mock_request.call_count, 2)
    
    @patch.object(FetchFromTabbyAPI, 'get_custom_request')
    def test_get_ballot_correct_url_construction(self, mock_request):
        """Test that ballot URL is correctly constructed"""
        mock_request.side_effect = [
            {'_links': {'ballots': 'http://example.com/api/v1/tournaments/1/rounds/2/pairings/5/ballots'}},
            {'ballot': 'data'}
        ]
        
        self.api.get_ballot_of_debate(
            "http://example.com/api/v1/tournaments/1",
            round_number=2,
            debate_id=5
        )
        
        # Check first call
        calls = mock_request.call_args_list
        first_call = str(calls[0])
        self.assertIn('tournaments/1', first_call)
        self.assertIn('rounds/2', first_call)
        self.assertIn('pairings/5', first_call)


class TestGetListOfDebateDataFromRound(unittest.TestCase):
    """Test cases for get_list_of_debate_data_from_round method"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.api = FetchFromTabbyAPI()
    
    @patch.object(FetchFromTabbyAPI, 'get_link_to_pairing_page_of_round')
    @patch.object(FetchFromTabbyAPI, 'get_custom_request')
    def test_get_list_of_debate_data_from_round(self, mock_request, mock_get_link):
        """Test getting list of debates from a round"""
        mock_get_link.return_value = 'http://example.com/api/v1/tournaments/1/rounds/1/pairings'
        mock_debates = [
            {'id': 1, 'teams': ['A', 'B']},
            {'id': 2, 'teams': ['C', 'D']},
            {'id': 3, 'teams': ['E', 'F']}
        ]
        mock_request.return_value = mock_debates
        
        result = self.api.get_list_of_debate_data_from_round(
            "http://example.com/api/v1/tournaments/1",
            round_number=1
        )
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result, [1, 2, 3])
    
    @patch.object(FetchFromTabbyAPI, 'get_link_to_pairing_page_of_round')
    @patch.object(FetchFromTabbyAPI, 'get_custom_request')
    def test_get_list_of_debate_data_returns_ids_only(self, mock_request, mock_get_link):
        """Test that only debate IDs are returned"""
        mock_get_link.return_value = 'http://example.com/pairings'
        mock_debates = [
            {'id': 10, 'other': 'data'},
            {'id': 20, 'other': 'data'}
        ]
        mock_request.return_value = mock_debates
        
        result = self.api.get_list_of_debate_data_from_round(
            "http://example.com/api/v1/tournaments/1",
            round_number=1
        )
        
        self.assertEqual(result, [10, 20])
    
    @patch.object(FetchFromTabbyAPI, 'get_link_to_pairing_page_of_round')
    @patch.object(FetchFromTabbyAPI, 'get_custom_request')
    def test_get_list_of_debate_data_empty_round(self, mock_request, mock_get_link):
        """Test getting debates from a round with no debates"""
        mock_get_link.return_value = 'http://example.com/pairings'
        mock_request.return_value = []
        
        result = self.api.get_list_of_debate_data_from_round(
            "http://example.com/api/v1/tournaments/1",
            round_number=1
        )
        
        self.assertEqual(result, [])


class TestAPIIntegration(unittest.TestCase):
    """Integration tests for API class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.api = FetchFromTabbyAPI(timeout=10)
    
    @patch.object(FetchFromTabbyAPI, 'get_custom_request')
    def test_full_workflow_simulation(self, mock_request):
        """Test a simulated full workflow of API calls"""
        # Simulate getting tournaments
        tournaments_response = [
            {'url': 'http://example.com/tournaments/1'},
            {'url': 'http://example.com/tournaments/2'}
        ]
        
        mock_request.return_value = tournaments_response
        
        result = self.api.get_list_of_tournaments_from_tabbycat("http://example.com/api")
        
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(t, str) for t in result))


if __name__ == '__main__':
    unittest.main()
