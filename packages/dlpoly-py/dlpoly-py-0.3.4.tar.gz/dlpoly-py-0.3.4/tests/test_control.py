#!/usr/bin/env python3
import unittest

import dlpoly as dlp
from dlpoly.new_control import NewControl


class ControlTest(unittest.TestCase):

    def setUp(self):
        self.control = ControlTest.control

    @classmethod
    def setUpClass(cls):
        super(ControlTest, cls).setUpClass()
        cls.control = dlp.DLPoly(control="tests/CONTROL").control

    def test_control_steps(self):
        self.assertEqual(self.control.time_run, [20.0, 'steps'],
                         'incorrect number of steps')
        self.assertEqual(self.control.time_equilibration, [10.0, 'steps'],
                         'incorrect number of equilibration steps')
        self.assertEqual(self.control.timestep, [0.001, 'ps'],
                         'incorrect timestep step')
        self.assertEqual(self.control.timestep_variable, True,
                         'incorrect variable step')

    def test_control_tp(self):
        self.assertEqual(self.control.temperature, [300.0, 'K'],
                         'incorrect temperature')
        self.assertEqual(self.control.pressure_hydrostatic[0], 0.001,
                         'incorrect pressure')

    def test_control_ens(self):
        self.assertEqual(self.control.ensemble, 'npt',
                         'incorrect ensemble')
        self.assertEqual(self.control.ensemble_method, 'hoover',
                         'incorrect ensemble type')
        self.assertListEqual(self.control.ensemble_thermostat_coupling, [0.5, 'ps'],
                             'incorrect ensemble')
        self.assertListEqual(self.control.ensemble_barostat_coupling, [1.0, 'ps'],
                             'incorrect ensemble')

    def test_control_prints(self):
        self.assertEqual(self.control.stats_frequency, [5.0, 'steps'],
                         'incorrect stats frequency')
        self.assertEqual(self.control.print_frequency, [5.0, 'steps'],
                         'incorrect print frequency')
        self.assertEqual(self.control.rdf_print, True,
                         'incorrect rdf')
        self.assertEqual(self.control.record_equilibration, True,
                         'incorrect collect setting')

    def test_control_equil(self):
        self.assertEqual(self.control.equilibration_force_cap, [1000.0, 'k_B.temp/ang'],
                         'incorrect cap')
        self.assertEqual(self.control.rescale_frequency, [3, 'steps'],
                         'incorrect scale')
        self.assertEqual(self.control.shake_tolerance, [0.000001, 'ang'],
                         'incorrect shake')

    def test_control_from_dict(self):

        test_dict = {
            'time_run': [20.0, 'steps'],
            'time_equilibration': [10.0, 'steps'],
            'timestep': [0.001, 'ps'],
            'timestep_variable': True,
            'temperature': [300.0, 'K'],
            'pressure_hydrostatic': [0.001, 'katm'],
            'ensemble': 'npt',
            'ensemble_method': 'hoover',
            'ensemble_thermostat_coupling': [0.5, 'ps'],
            'ensemble_barostat_coupling': [1.0, 'ps'],
            'stats_frequency': [5.0, 'steps'],
            'print_frequency': [5.0, 'steps'],
            'rdf_print': True,
            'record_equilibration': True,
            'equilibration_force_cap': [1000.0, 'k_B.temp/ang'],
            'rescale_frequency': [3, 'steps'],
            'shake_tolerance': [0.000001, 'ang']}

        cont = NewControl.from_dict(test_dict)
        for key in test_dict:
            self.assertEqual(cont[key], self.control[key])

        with self.assertRaises(KeyError) as context:
            test_dict = {'tim_run': [20.0, 'steps']}
            cont = NewControl.from_dict(test_dict)

        self.assertTrue('not allowed in' in str(context.exception))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ControlTest('test_control_steps'))
    suite.addTest(ControlTest('test_control_tp'))
    suite.addTest(ControlTest('test_control_ens'))
    suite.addTest(ControlTest('test_control_prints'))
    suite.addTest(ControlTest('test_control_equil'))
    suite.addTest(ControlTest('test_control_from_dict'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
