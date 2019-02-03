# Copyright (c) 2018, Yung-Yu Chen <yyc@solvcon.net>
# BSD 3-Clause License, see COPYING

import unittest

import numpy as np

import libst


class SolutionTC(unittest.TestCase):

    def setUp(self):

        self.grid10 = libst.Grid(0, 10, 10)
        self.sol10 = libst.Solution(grid=self.grid10, nvar=1,
                                    time_increment=0.2)
        self.sol10.so0.fill(-1)
        self.sol10.so1.fill(-2)

    def test_str(self):

        self.assertEqual("Solution(grid=Grid(xmin=0, xmax=10, ncelm=10))",
                         str(self.sol10))

    def test_grid(self):

        self.assertEqual(self.grid10, self.sol10.grid)

    def test_nvar(self):

        self.assertEqual(1, self.sol10.nvar)

    def test_time_increment(self):

        self.assertEqual(0.2, self.sol10.time_increment)
        self.sol10.time_increment = 42
        self.assertEqual(42, self.sol10.time_increment)

    def test_so0_so1(self):

        # shape
        self.assertEqual((23,1), self.sol10.so0.shape)
        self.assertEqual((23,1), self.sol10.so1.shape)
        # type
        self.assertEqual(np.float64, self.sol10.so0.dtype)
        self.assertEqual(np.float64, self.sol10.so1.dtype)
        # content
        self.sol10.so0.fill(0)
        self.assertEqual([0.0]*23, self.sol10.so0.flatten().tolist())
        self.sol10.so1.fill(1)
        self.assertEqual([1.0]*23, self.sol10.so1.flatten().tolist())

    def test_celm(self):

        with self.assertRaises(TypeError):
            self.sol10.celm(-1)

        self.assertEqual(
            "Celm(even, index=0, x=0.5, xneg=0, xpos=1)",
            str(self.sol10.celm(0)),
        )

        self.assertEqual(
            "Celm(odd, index=0, x=1, xneg=0.5, xpos=1.5)",
            str(self.sol10.celm(ielm=0, odd_plane=True)),
        )

        self.assertEqual(
            "Celm(even, index=9, x=9.5, xneg=9, xpos=10)",
            str(self.sol10.celm(9, odd_plane=False)),
        )

        with self.assertRaisesRegex(
            IndexError,
            "Field::celm_at\(ielm=9, odd_plane=1\): xindex = 21 "
            "outside the interval \[2, 21\)",
        ):
            self.sol10.celm(9, odd_plane=True)

        with self.assertRaisesRegex(
            IndexError,
            "Field::celm_at\(ielm=10, odd_plane=0\): xindex = 22 "
            "outside the interval \[2, 21\)",
        ):
            self.sol10.celm(10)

    def test_selm(self):

        with self.assertRaises(TypeError):
            self.sol10.selm(-1)

        self.assertEqual(
            "Selm(even, index=0, x=0, xneg=-0.5, xpos=0.5)",
            str(self.sol10.selm(0)),
        )

        self.assertEqual(
            "Selm(odd, index=0, x=0.5, xneg=0, xpos=1)",
            str(self.sol10.selm(0, odd_plane=True)),
        )

        self.assertEqual(
            "Selm(even, index=10, x=10, xneg=9.5, xpos=10.5)",
            str(self.sol10.selm(10, odd_plane=False)),
        )

        with self.assertRaisesRegex(
            IndexError,
            "Field::selm_at\(ielm=10, odd_plane=1\): xindex = 22 "
            "outside the interval \[1, 22\)",
        ):
            self.sol10.selm(10, odd_plane=True)

        with self.assertRaisesRegex(
            IndexError,
            "Field::selm_at\(ielm=11, odd_plane=0\): xindex = 23 "
            "outside the interval \[1, 22\)",
        ):
            self.sol10.selm(11)

    def test_celms(self):

        sol = self.sol10

        self.assertEqual(list(sol.celms()), list(sol.celms(odd_plane=False)))

        gold = [sol.celm(it, odd_plane=False) for it in range(sol.grid.ncelm)]
        self.assertEqual(gold, list(sol.celms(odd_plane=False)))

        gold = [sol.celm(it, odd_plane=True) for it in range(sol.grid.ncelm-1)]
        self.assertEqual(gold, list(sol.celms(odd_plane=True)))

    def test_selms(self):

        sol = self.sol10

        self.assertEqual(list(sol.selms()), list(sol.selms(odd_plane=False)))

        gold = [sol.selm(it, odd_plane=False) for it in range(sol.grid.nselm)]
        self.assertEqual(gold, list(sol.selms(odd_plane=False)))

        gold = [sol.selm(it, odd_plane=True) for it in range(sol.grid.nselm-1)]
        self.assertEqual(gold, list(sol.selms(odd_plane=True)))

# vim: set et sw=4 ts=4: