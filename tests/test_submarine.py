import unittest

from submarine import (Submarine, SubmarineError, NotSubmergedError,
                     PropellerDamagedError, NotEnoughEnergyError)
from pilot import Pilot


class TestSubmarine(unittest.TestCase):
    def test_TC_01(self):
        """TC-01."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2)
        self.assertEqual((r.name, r.propeller_diameter_m, r.energy, r.depth_m, r.distance_km, r.propeller_intact), ("Жемчужина", 2, 100, 0, 0, True))

    def test_TC_02(self):
        """TC-02."""
        # Arrange / Act / Assert
        for name in ("", "   "):
            with self.subTest(name=name), self.assertRaises(ValueError):
                Submarine(name, 2)

    def test_TC_03(self):
        """TC-03."""
        # Arrange / Act / Assert
        for name, tail in ((12, 2), ("Жемчужина", True)):
            with self.subTest(name=name, tail=tail), self.assertRaises(TypeError):
                Submarine(name, tail)

    def test_TC_04(self):
        """TC-04."""
        # Arrange / Act / Assert
        for tail in (0, -1):
            with self.subTest(tail=tail), self.assertRaises(ValueError):
                Submarine("Жемчужина", tail)

    def test_TC_05(self):
        """TC-05."""
        # Arrange / Act / Assert
        for e in (-1, 101):
            with self.subTest(energy=e), self.assertRaises(ValueError):
                Submarine("Жемчужина", 2, e)
        self.assertEqual(Submarine("Жемчужина", 2, 0).energy, 0)
        self.assertEqual(Submarine("Жемчужина", 2, 100).energy, 100)

    def test_TC_06(self):
        """TC-06."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2)
        before = r.get_status()
        with self.assertRaises(ValueError):
            r.swim(0)
        self.assertEqual(r.get_status(), before)

    def test_TC_07(self):
        """TC-07."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2)
        r.dive(10)
        result = r.swim(10)
        self.assertAlmostEqual(result, 1)
        self.assertEqual((r.energy, r.distance_km, r.depth_m), (80, 10, 10))

    def test_TC_08(self):
        """TC-08."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2, 10)
        r.dive(1)
        result = r.swim(5)
        self.assertAlmostEqual(result, 0.5)
        self.assertEqual((r.energy, r.distance_km), (0, 5))

    def test_TC_09(self):
        """TC-09."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2)
        self.assertIsNone(r.dive(50))
        self.assertEqual(r.depth_m, 50)
        self.assertIsNone(r.dive(0))
        self.assertEqual(r.depth_m, 0)

    def test_TC_10(self):
        """TC-10."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2)
        before = r.get_status()
        for d in (-1, 51):
            with self.subTest(depth=d), self.assertRaises(ValueError):
                r.dive(d)
            self.assertEqual(r.get_status(), before)

    def test_TC_11(self):
        """TC-11."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2)
        with self.assertRaises(TypeError):
            r.dive("10")

    def test_TC_12(self):
        """TC-12."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2, 90)
        before = r.get_status()
        result = r.recharge(30)
        self.assertIsNone(result)
        before["energy"] = 100
        self.assertEqual(r.get_status(), before)

    def test_TC_13(self):
        """TC-13."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2)
        for amount in (0, -1):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                r.recharge(amount)

    def test_TC_14(self):
        """TC-14."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2)
        before = r.get_status()
        with self.assertRaises(NotSubmergedError):
            r.swim(1)
        self.assertEqual(r.get_status(), before)

    def test_TC_15(self):
        """TC-15."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2)
        r.dive(1)
        r.damage_propeller()
        before = r.get_status()
        with self.assertRaises(PropellerDamagedError):
            r.swim(1)
        self.assertEqual(r.get_status(), before)

    def test_TC_16(self):
        """TC-16."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2, 1)
        r.dive(1)
        before = r.get_status()
        with self.assertRaises(NotEnoughEnergyError):
            r.swim(1)
        self.assertEqual(r.get_status(), before)

    def test_TC_17(self):
        """TC-17."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2)
        self.assertIsNone(r.damage_propeller())
        self.assertIsNone(r.damage_propeller())
        self.assertFalse(r.propeller_intact)
        r.dive(5)
        self.assertIsNone(r.repair_propeller())
        self.assertIsNone(r.repair_propeller())
        self.assertTrue(r.propeller_intact)

    def test_TC_18(self):
        """TC-18."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2, 50)
        result = r.get_status()
        self.assertEqual(result, {"name": "Жемчужина", "propeller_diameter_m": 2, "energy": 50, "depth_m": 0, "distance_km": 0, "propeller_intact": True})
        result["energy"] = 0
        self.assertEqual(r.energy, 50)

    def test_TC_19(self):
        """TC-19."""
        # Arrange / Act / Assert
        r = Submarine("Жемчужина", 2)
        with self.assertRaises(TypeError):
            r.swim("1")
        with self.assertRaises(TypeError):
            r.recharge(True)

    def test_TC_20(self):
        """TC-20."""
        # Arrange / Act / Assert
        for x in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=x):
                with self.assertRaises(ValueError):
                    Submarine("Жемчужина", 2, x)
                with self.assertRaises(ValueError):
                    Submarine("Жемчужина", 2).swim(x)

    def test_TC_21(self):
        """TC-21."""
        # Given / When / Then
        p = Pilot(Submarine("Жемчужина", 2))
        p.dive(20)
        elapsed = p.swim(10)
        p.dive(0)
        self.assertAlmostEqual(elapsed, 1)
        self.assertEqual((p.submarine.distance_km, p.submarine.energy, p.submarine.depth_m), (10, 80, 0))

    def test_TC_22(self):
        """TC-22."""
        # Given / When / Then
        p = Pilot(Submarine("Жемчужина", 2))
        p.dive(10)
        p.damage_propeller()
        before = p.submarine.get_status()
        with self.assertRaises(PropellerDamagedError):
            p.swim(1)
        self.assertEqual(p.submarine.get_status(), before)
        p.repair_propeller()
        self.assertAlmostEqual(p.swim(1), 0.1)
        self.assertEqual((p.submarine.distance_km, p.submarine.energy), (1, 98))

    def test_TC_23(self):
        """TC-23."""
        # Given / When / Then
        p = Pilot(Submarine("Жемчужина", 2, 10))
        p.dive(5)
        p.swim(5)
        self.assertEqual(p.submarine.energy, 0)
        p.recharge(20)
        p.swim(3)
        self.assertEqual((p.submarine.energy, p.submarine.distance_km, p.submarine.depth_m), (14, 8, 5))

    def test_TC_24(self):
        """TC-24."""
        # Given / When / Then
        p = Pilot(Submarine("Жемчужина", 2, 5))
        p.dive(50)
        before = p.submarine.get_status()
        with self.assertRaises(NotEnoughEnergyError):
            p.swim(3)
        self.assertEqual(p.submarine.get_status(), before)
        p.dive(0)
        self.assertEqual((p.submarine.depth_m, p.submarine.energy, p.submarine.distance_km), (0, 5, 0))

