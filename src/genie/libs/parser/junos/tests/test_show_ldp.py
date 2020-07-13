# Python
import unittest
from unittest.mock import Mock

# ATS
from pyats.topology import Device

# Metaparser
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.parser.junos.show_ldp import (
    ShowLDPSession, ShowLdpNeighbor)


# =================================
# Unit test for 'show ldp session'
# =================================
class TestShowLDPSession(unittest.TestCase):
    '''unit test for "show ldp session'''
    device = Device(name='aDevice')
    maxDiff = None

    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'ldp-session-information': {
            'ldp-session': [{
                'ldp-neighbor-address': '59.128.2.250',
                'ldp-session-state': 'Operational',
                'ldp-connection-state': 'Open',
                'ldp-remaining-time': '26',
                'ldp-session-adv-mode': 'DU'
            }]
        }
    }

    golden_output = {
        'execute.return_value':
        '''
          Address                           State       Connection  Hold time  Adv. Mode
        59.128.2.250                        Operational Open          26         DU
        '''
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowLDPSession(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowLDPSession(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)



























# =================================
# Unit test for 'show ldp neighbor'
# =================================
class TestShowLDPSession(unittest.TestCase):
    '''unit test for "show ldp session'''
    device = Device(name='aDevice')
    maxDiff = None

    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
            'ldp-neighbor-information': 
                {'ldp-neighbor': [
                    {'interface-name': 'ge-0/0/0.0',
                     'ldp-label-space-id': '59.128.2.250:0',
                     'ldp-neighbor-address': '106.187.14.158',
                     'ldp-remaining-time': '14'
                     }
                ]
            }
    }

    golden_output = {
        'execute.return_value':
        '''
          show ldp neighbor
        Address                             Interface       Label space ID     Hold time
        106.187.14.158                      ge-0/0/0.0      59.128.2.250:0       14
        '''
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowLdpNeighbor(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowLdpNeighbor(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


if __name__ == '__main__':
    unittest.main()
