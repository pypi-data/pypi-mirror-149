"""Test HSI."""
import unittest
from . import util
from coloraide_extras import Color, NaN
import pytest


class TestHSI(util.ColorAssertsPyTest):
    """Test HSI."""

    COLORS = [
        ('red', 'color(--hsi 0 1 0.33333)'),
        ('orange', 'color(--hsi 38.824 1 0.54902)'),
        ('yellow', 'color(--hsi 60 1 0.66667)'),
        ('green', 'color(--hsi 120 1 0.16732)'),
        ('blue', 'color(--hsi 240 1 0.33333)'),
        ('indigo', 'color(--hsi 274.62 1 0.26797)'),
        ('violet', 'color(--hsi 300 0.35644 0.79216)'),
        ('white', 'color(--hsi 0 0 1)'),
        ('gray', 'color(--hsi 0 0 0.50196)'),
        ('black', 'color(--hsi 0 0 0)')
    ]

    @pytest.mark.parametrize('color1,color2', COLORS)
    def test_hsi_colors(self, color1, color2):
        """Test colors."""

        self.assertColorEqual(Color(color1).convert('hsi'), Color(color2))


class TestHSIPoperties(util.ColorAsserts, unittest.TestCase):
    """Test HSI."""

    def test_h(self):
        """Test `h`."""

        c = Color('color(--hsi 60 1 0.66667)')
        self.assertEqual(c['h'], 60)
        c['h'] = 0.2
        self.assertEqual(c['h'], 0.2)

    def test_s(self):
        """Test `s`."""

        c = Color('color(--hsi 60 1 0.66667)')
        self.assertEqual(c['s'], 1)
        c['s'] = 0.1
        self.assertEqual(c['s'], 0.1)

    def test_i(self):
        """Test `i`."""

        c = Color('color(--hsi 60 1 0.66667)')
        self.assertEqual(c['i'], 0.66667)
        c['i'] = 0.1
        self.assertEqual(c['i'], 0.1)

    def test_alpha(self):
        """Test `alpha`."""

        c = Color('color(--hsi 60 1 0.66667)')
        self.assertEqual(c['alpha'], 1)
        c['alpha'] = 0.5
        self.assertEqual(c['alpha'], 0.5)


class TestNull(util.ColorAsserts, unittest.TestCase):
    """Test Null cases."""

    def test_null_input(self):
        """Test null input."""

        c = Color('hsi', [NaN, 0.5, 1], 1)
        self.assertTrue(c.is_nan('hue'))

    def test_none_input(self):
        """Test `none` null."""

        c = Color('color(--hsi none 0% 75% / 1)')
        self.assertTrue(c.is_nan('hue'))

    def test_null_normalization_min_sat(self):
        """Test minimum saturation."""

        c = Color('color(--hsi 270 0% 75% / 1)').normalize()
        self.assertTrue(c.is_nan('hue'))

    def test_null_normalization_min_intensity(self):
        """Test minimum intensity."""

        c = Color('color(--hsi 270 20% 0% / 1)').normalize()
        self.assertTrue(c.is_nan('hue'))

    def test_corner_case_null(self):
        """Test corner case that produces null."""

        c = Color('color(srgb -2 0 2)').convert('hsl')
        self.assertTrue(c.is_nan('hue'))
