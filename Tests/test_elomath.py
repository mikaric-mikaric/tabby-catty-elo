import unittest
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ELOMath.elomath import (
    CalculateELOexpectation,
    SpeakerDifferenceFactor,
    CalculateELOchange,
    CalculateNewELO
)


class TestCalculateELOexpectation(unittest.TestCase):
    """Test cases for CalculateELOexpectation function"""
    
    def test_equal_ratings(self):
        """When both players have equal ratings, each should have 50% win probability"""
        expA, expB = CalculateELOexpectation(1600, 1600)
        self.assertAlmostEqual(expA, 0.5, places=5)
        self.assertAlmostEqual(expB, 0.5, places=5)
    
    def test_higher_rated_advantage(self):
        """Higher rated player should have higher win probability"""
        expA, expB = CalculateELOexpectation(1800, 1600)
        self.assertGreater(expA, expB)
        self.assertAlmostEqual(expA + expB, 1.0, places=5)
    
    def test_probabilities_sum_to_one(self):
        """Probabilities should always sum to 1"""
        expA, expB = CalculateELOexpectation(1700, 1500)
        self.assertAlmostEqual(expA + expB, 1.0, places=5)
    
    def test_lower_rated_disadvantage(self):
        """Lower rated player should have lower win probability"""
        expA, expB = CalculateELOexpectation(1400, 1600)
        self.assertLess(expA, expB)
    
    def test_large_rating_difference(self):
        """With large rating difference, higher rated player should have very high probability"""
        expA, expB = CalculateELOexpectation(2000, 1200)
        self.assertGreater(expA, 0.9)
        self.assertLess(expB, 0.1)
    
    def test_return_type(self):
        """Should return tuple of two floats"""
        result = CalculateELOexpectation(1600, 1600)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)


class TestSpeakerDifferenceFactor(unittest.TestCase):
    """Test cases for SpeakerDifferenceFactor function"""
    
    def test_winner_no_difference(self):
        """Winner with 0 speaker difference should have factor of 1.0"""
        factor = SpeakerDifferenceFactor(won=True, spk_diff=0)
        self.assertAlmostEqual(factor, 1.0, places=5)
    
    def test_winner_positive_difference(self):
        """Winner with positive speaker difference should have factor > 1.0"""
        factor = SpeakerDifferenceFactor(won=True, spk_diff=5)
        self.assertGreater(factor, 1.0)
        self.assertLessEqual(factor, 1.9)
    
    def test_loser_no_difference(self):
        """Loser with 0 speaker difference should have factor of 1.0"""
        factor = SpeakerDifferenceFactor(won=False, spk_diff=0)
        self.assertAlmostEqual(factor, 1.0, places=5)
    
    def test_loser_negative_difference(self):
        """Loser with negative speaker difference should have factor < 1.0"""
        factor = SpeakerDifferenceFactor(won=False, spk_diff=5)
        self.assertLess(factor, 1.0)
        self.assertGreaterEqual(factor, 0.1)
    
    def test_maximum_factor_bound(self):
        """Factor should be capped at 1.9 maximum"""
        factor = SpeakerDifferenceFactor(won=True, spk_diff=100)
        self.assertEqual(factor, 1.9)
    
    def test_minimum_factor_bound(self):
        """Factor should be capped at 0.1 minimum"""
        factor = SpeakerDifferenceFactor(won=False, spk_diff=100)
        self.assertEqual(factor, 0.1)
    
    def test_winner_large_difference(self):
        """Winner with large speaker difference should approach 1.9"""
        factor = SpeakerDifferenceFactor(won=True, spk_diff=19)
        self.assertEqual(factor, 1.9)
    
    def test_loser_large_difference(self):
        """Loser with large speaker difference should approach 0.1"""
        factor = SpeakerDifferenceFactor(won=False, spk_diff=19)
        self.assertEqual(factor, 0.1)


class TestCalculateELOchange(unittest.TestCase):
    """Test cases for CalculateELOchange function"""
    
    def test_winner_gains_points(self):
        """Winner (player A) should gain ELO points"""
        changeA, changeB = CalculateELOchange(
            ratingA=1600,
            ratingB=1600,
            kA=32,
            kB=32,
            spk_diffA=0,
            spk_diffB=0
        )
        self.assertGreater(changeA, 0)
    
    def test_loser_loses_points(self):
        """Loser (player B) should lose ELO points"""
        changeA, changeB = CalculateELOchange(
            ratingA=1600,
            ratingB=1600,
            kA=32,
            kB=32,
            spk_diffA=0,
            spk_diffB=0
        )
        self.assertLess(changeB, 0)
    
    def test_changes_roughly_sum_to_zero(self):
        """With equal K-factors, changes should roughly sum to zero (zero-sum game)"""
        changeA, changeB = CalculateELOchange(
            ratingA=1600,
            ratingB=1600,
            kA=32,
            kB=32,
            spk_diffA=0,
            spk_diffB=0
        )
        self.assertAlmostEqual(changeA + changeB, 0, places=1)
    
    def test_favorite_wins_small_gain(self):
        """Favorite winning should gain less ELO than underdog"""
        # Favorite wins
        changeA_fav, _ = CalculateELOchange(
            ratingA=1800,
            ratingB=1600,
            kA=32,
            kB=32,
            spk_diffA=0,
            spk_diffB=0
        )
        # Underdog wins
        changeA_under, _ = CalculateELOchange(
            ratingA=1400,
            ratingB=1600,
            kA=32,
            kB=32,
            spk_diffA=0,
            spk_diffB=0
        )
        self.assertLess(changeA_fav, changeA_under)
    
    def test_speaker_difference_affects_gain(self):
        """Higher speaker difference should result in higher gain for winner"""
        change_no_diff, _ = CalculateELOchange(
            ratingA=1600,
            ratingB=1600,
            kA=32,
            kB=32,
            spk_diffA=0,
            spk_diffB=0
        )
        change_with_diff, _ = CalculateELOchange(
            ratingA=1600,
            ratingB=1600,
            kA=32,
            kB=32,
            spk_diffA=5,
            spk_diffB=0
        )
        self.assertGreater(change_with_diff, change_no_diff)


class TestCalculateNewELO(unittest.TestCase):
    """Test cases for CalculateNewELO function"""
    
    def test_winner_rating_increases(self):
        """Winner's new rating should be higher than original"""
        newA, newB = CalculateNewELO(
            ratingA=1600,
            ratingB=1600,
            kA=32,
            kB=32,
            spk_diffA=0,
            spk_diffB=0
        )
        self.assertGreater(newA, 1600)
    
    def test_loser_rating_decreases(self):
        """Loser's new rating should be lower than original"""
        newA, newB = CalculateNewELO(
            ratingA=1600,
            ratingB=1600,
            kA=32,
            kB=32,
            spk_diffA=0,
            spk_diffB=0
        )
        self.assertLess(newB, 1600)
    
    def test_return_type(self):
        """Should return tuple of two floats"""
        result = CalculateNewELO(
            ratingA=1600,
            ratingB=1600,
            kA=32,
            kB=32,
            spk_diffA=0,
            spk_diffB=0
        )
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
    
    def test_higher_k_factor_larger_change(self):
        """Higher K-factor should result in larger rating change"""
        newA_k16, newB_k16 = CalculateNewELO(
            ratingA=1600,
            ratingB=1600,
            kA=16,
            kB=16,
            spk_diffA=0,
            spk_diffB=0
        )
        newA_k32, newB_k32 = CalculateNewELO(
            ratingA=1600,
            ratingB=1600,
            kA=32,
            kB=32,
            spk_diffA=0,
            spk_diffB=0
        )
        self.assertGreater(newA_k32 - 1600, newA_k16 - 1600)
    
    def test_realistic_scenario(self):
        """Test with realistic scenario"""
        # Strong player beats weak player with same speaker points
        newA, newB = CalculateNewELO(
            ratingA=1800,  # Strong player
            ratingB=1400,  # Weak player
            kA=32,
            kB=32,
            spk_diffA=0,
            spk_diffB=0
        )
        # Strong player should still gain points
        self.assertGreater(newA, 1800)
        # Weak player should lose points
        self.assertLess(newB, 1400)


if __name__ == '__main__':
    unittest.main()
