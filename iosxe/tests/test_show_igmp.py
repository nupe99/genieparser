# Python
import unittest
from unittest.mock import Mock

# ATS
from ats.topology import Device

# Metaparset
from metaparser.util.exceptions import SchemaEmptyParserError, \
                                       SchemaMissingKeyError

# Parser
from parser.iosxe.show_igmp import ShowIpIgmpInterface, \
                                   ShowIpIgmpGroupsDetail, \
                                   ShowIpIgmpSsmMapping


# ==================================================
# Unit test for 'show ip igmp interface'
# Unit test for 'show ip igmp vrf <WORD> interface'
# ==================================================
class test_show_ip_igmp_interface(unittest.TestCase):
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output = {
        "vrf": {
            "default": {
                 "interface": {
                      "GigabitEthernet1": {
                           "querier_timeout": 266,
                           "configured_querier_timeout": 266,
                           "max_groups": 10,
                           "multicast": {
                                "designated_router": "10.1.2.1",
                                "ttl_threshold": 0,
                                "routing_enable": True
                           },
                           "group_policy": "test2",
                           "line_protocol": "up",
                           "query_max_response_time": 10,
                           "router_version": 3,
                           "leaves": 3,
                           "interface_adress": "10.1.2.1/24",
                           "joined_group": {
                                "239.3.3.3": {
                                     "number_of_users": 1
                                },
                                "224.0.1.40": {
                                     "number_of_users": 1
                                },
                                "239.1.1.1": {
                                     "number_of_users": 1
                                },
                                "239.4.4.4": {
                                     "number_of_users": 1
                                },
                                "239.2.2.2": {
                                     "number_of_users": 1
                                }
                           },
                           "oper_status": "up",
                           "active_groups": 1,
                           "joins": 13,
                           "last_member_query_count": 2,
                           "query_interval": 133,
                           "enable": True,
                           "querier": "10.1.2.1",
                           "configured_query_interval": 133,
                           "last_member_query_interval": 100,
                           "host_version": 3
                      }
                 },
                 "global_active_groups": 1,
                 "global_max_groups": 20
            }
       }
    }

    golden_output = {'execute.return_value': '''\
        Global IGMP State Limit : 1 active out of 20 max
        GigabitEthernet1 is up, line protocol is up
          Internet address is 10.1.2.1/24
          IGMP is enabled on interface
          Current IGMP host version is 3
          Current IGMP router version is 3
          IGMP query interval is 133 seconds
          IGMP configured query interval is 133 seconds
          IGMP querier timeout is 266 seconds
          IGMP configured querier timeout is 266 seconds
          IGMP max query response time is 10 seconds
          Last member query count is 2
          Last member query response interval is 100 ms
          Inbound IGMP access group is test2
          IGMP activity: 13 joins, 3 leaves
          Interface IGMP State Limit : 1 active out of 10 max
          Multicast routing is enabled on interface
          Multicast TTL threshold is 0
          Multicast designated router (DR) is 10.1.2.1 (this system)
          IGMP querying router is 10.1.2.1 (this system)
          Multicast groups joined by this system (number of users):
              224.0.1.40(1)  239.4.4.4(1)  239.3.3.3(1)
              239.2.2.2(1)  239.1.1.1(1)
    '''}
    
    golden_parsed_output_1 = {
        "vrf": {
            "VRF1": {
                 "interface": {
                      "GigabitEthernet2": {
                           "querier_timeout": 266,
                           "configured_querier_timeout": 266,
                           "max_groups": 10,
                           "multicast": {
                                "designated_router": "20.1.2.1",
                                "ttl_threshold": 0,
                                "routing_enable": True,
                                "routing_table": "VRF1",
                           },
                           "group_policy": "test2",
                           "line_protocol": "up",
                           "query_max_response_time": 10,
                           "router_version": 3,
                           "leaves": 0,
                           "interface_adress": "20.1.2.1/24",
                           "joined_group": {
                                "224.0.1.40": {
                                     "number_of_users": 1
                                },
                                "239.1.1.1": {
                                     "number_of_users": 1
                                },
                                "239.2.2.2": {
                                     "number_of_users": 1
                                },
                                "239.3.3.3": {
                                     "number_of_users": 1
                                },
                                "239.4.4.4": {
                                     "number_of_users": 1
                                }
                           },
                           "oper_status": "up",
                           "active_groups": 0,
                           "joins": 9,
                           "last_member_query_count": 2,
                           "query_interval": 133,
                           "enable": True,
                           "querier": "20.1.2.1",
                           "configured_query_interval": 133,
                           "last_member_query_interval": 100,
                           "host_version": 3
                      }
                 },
                 "global_active_groups": 0,
                 "global_max_groups": 20
            }
       }
    }

    golden_output_1 = {'execute.return_value': '''\
        Global IGMP State Limit : 0 active out of 20 max
        GigabitEthernet2 is up, line protocol is up
          Internet address is 20.1.2.1/24
          IGMP is enabled on interface
          Multicast Routing table VRF1
          Current IGMP host version is 3
          Current IGMP router version is 3
          IGMP query interval is 133 seconds
          IGMP configured query interval is 133 seconds
          IGMP querier timeout is 266 seconds
          IGMP configured querier timeout is 266 seconds
          IGMP max query response time is 10 seconds
          Last member query count is 2
          Last member query response interval is 100 ms
          Inbound IGMP access group is test2
          IGMP activity: 9 joins, 0 leaves
          Interface IGMP State Limit : 0 active out of 10 max
          Multicast routing is enabled on interface
          Multicast TTL threshold is 0
          Multicast designated router (DR) is 20.1.2.1 (this system)
          IGMP querying router is 20.1.2.1 (this system)
          Multicast groups joined by this system (number of users):
              224.0.1.40(1)  239.1.1.1(1)  239.2.2.2(1)
              239.3.3.3(1)  239.4.4.4(1)
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowIpIgmpInterface(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden_default_vrf(self):
        self.device = Mock(**self.golden_output)
        obj = ShowIpIgmpInterface(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output)

    def test_golden_non_default_vrf(self):
        self.device = Mock(**self.golden_output_1)
        obj = ShowIpIgmpInterface(device=self.device)
        parsed_output = obj.parse(vrf='VRF1')
        self.assertEqual(parsed_output,self.golden_parsed_output_1)


# =====================================================
# Unit test for 'show ip igmp groups detail'
# Unit test for 'show ip igmp vrf <WORD> groups detail'
# =====================================================
class test_show_ip_igmp_groups_detail(unittest.TestCase):
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output = {
        "vrf": {
            "default": {
                 "interface": {
                      "GigabitEthernet1": {
                           "group": {
                                "239.1.1.1": {
                                     "group_mode": "include",
                                     "up_time": "00:05:06",
                                     "flags": "L U",
                                     "last_reporter": "10.1.2.1"
                                },
                                "239.5.5.5": {
                                     "group_mode": "include",
                                     "up_time": "00:05:06",
                                     "flags": "SG",
                                     "last_reporter": "0.0.0.0"
                                },
                                "239.4.4.4": {
                                     "group_mode": "include",
                                     "up_time": "00:05:06",
                                     "flags": "L",
                                     "source": {
                                          "1.1.1.2": {
                                               "up_time": "00:05:06",
                                               "flags": "L",
                                               "foward": True,
                                               "csr_exp": "stopped",
                                               "v3_exp": "stopped"
                                          }
                                     },
                                     "last_reporter": "10.1.2.1"
                                },
                                "239.8.8.8": {
                                     "group_mode": "include",
                                     "up_time": "00:05:06",
                                     "flags": "SS",
                                     "source": {
                                          "2.2.2.1": {
                                               "up_time": "00:05:06",
                                               "flags": "S",
                                               "foward": True,
                                               "csr_exp": "stopped",
                                               "v3_exp": "stopped"
                                          },
                                          "2.2.2.2": {
                                               "up_time": "00:05:06",
                                               "flags": "S",
                                               "foward": True,
                                               "csr_exp": "stopped",
                                               "v3_exp": "stopped"
                                          }
                                     },
                                     "last_reporter": "0.0.0.0"
                                },
                                "239.6.6.6": {
                                     "group_mode": "include",
                                     "up_time": "00:05:06",
                                     "flags": "SG",
                                     "last_reporter": "0.0.0.0"
                                },
                                "239.7.7.7": {
                                     "group_mode": "include",
                                     "up_time": "00:05:06",
                                     "flags": "SS",
                                     "source": {
                                          "2.2.2.1": {
                                               "up_time": "00:05:06",
                                               "flags": "S",
                                               "foward": True,
                                               "csr_exp": "stopped",
                                               "v3_exp": "stopped"
                                          }
                                     },
                                     "last_reporter": "0.0.0.0"
                                },
                                "239.9.9.9": {
                                     "group_mode": "exclude",
                                     "up_time": "00:23:15",
                                     "flags": "Ac",
                                     "expire": "00:06:06",
                                     "last_reporter": "10.1.2.2"
                                },
                                "239.2.2.2": {
                                     "group_mode": "include",
                                     "up_time": "00:05:06",
                                     "flags": "L U",
                                     "last_reporter": "10.1.2.1"
                                },
                                "224.0.1.40": {
                                     "group_mode": "include",
                                     "up_time": "00:25:33",
                                     "flags": "L U",
                                     "last_reporter": "10.1.2.1"
                                },
                                "239.3.3.3": {
                                     "group_mode": "include",
                                     "up_time": "00:05:06",
                                     "flags": "L",
                                     "source": {
                                          "1.1.1.1": {
                                               "up_time": "00:05:06",
                                               "flags": "L",
                                               "foward": True,
                                               "csr_exp": "stopped",
                                               "v3_exp": "stopped"
                                          }
                                     },
                                     "last_reporter": "10.1.2.1"
                                }
                           },
                           "static_group": {
                                "239.6.6.6 *": {
                                     "up_time": "00:05:06",
                                     "flags": "SG",
                                     "last_reporter": "0.0.0.0"
                                },
                                "239.5.5.5 *": {
                                     "up_time": "00:05:06",
                                     "flags": "SG",
                                     "last_reporter": "0.0.0.0"
                                }
                           },
                           "join_group": {
                                "239.8.8.8 2.2.2.2": {
                                     "up_time": "00:05:06",
                                     "foward": True,
                                     "csr_exp": "stopped",
                                     "v3_exp": "stopped",
                                     "flags": "SS",
                                     "last_reporter": "0.0.0.0"
                                },
                                "239.8.8.8 2.2.2.1": {
                                     "up_time": "00:05:06",
                                     "foward": True,
                                     "csr_exp": "stopped",
                                     "v3_exp": "stopped",
                                     "flags": "SS",
                                     "last_reporter": "0.0.0.0"
                                },
                                "239.4.4.4 1.1.1.2": {
                                     "up_time": "00:05:06",
                                     "foward": True,
                                     "csr_exp": "stopped",
                                     "v3_exp": "stopped",
                                     "flags": "L",
                                     "last_reporter": "10.1.2.1"
                                },
                                "239.9.9.9 *": {
                                     "expire": "00:06:06",
                                     "up_time": "00:23:15",
                                     "flags": "Ac",
                                     "last_reporter": "10.1.2.2"
                                },
                                "224.0.1.40 *": {
                                     "up_time": "00:25:33",
                                     "flags": "L U",
                                     "last_reporter": "10.1.2.1"
                                },
                                "239.7.7.7 2.2.2.1": {
                                     "up_time": "00:05:06",
                                     "foward": True,
                                     "csr_exp": "stopped",
                                     "v3_exp": "stopped",
                                     "flags": "SS",
                                     "last_reporter": "0.0.0.0"
                                },
                                "239.3.3.3 1.1.1.1": {
                                     "up_time": "00:05:06",
                                     "foward": True,
                                     "csr_exp": "stopped",
                                     "v3_exp": "stopped",
                                     "flags": "L",
                                     "last_reporter": "10.1.2.1"
                                },
                                "239.2.2.2 *": {
                                     "up_time": "00:05:06",
                                     "flags": "L U",
                                     "last_reporter": "10.1.2.1"
                                },
                                "239.1.1.1 *": {
                                     "up_time": "00:05:06",
                                     "flags": "L U",
                                     "last_reporter": "10.1.2.1"
                                }
                           }
                      }
                 }
            }
       }
    }

    golden_output = {'execute.return_value': '''\
        Flags: L - Local, U - User, SG - Static Group, VG - Virtual Group,
               SS - Static Source, VS - Virtual Source,
               Ac - Group accounted towards access control limit

        Interface:        GigabitEthernet1
        Group:                239.1.1.1
        Flags:                L U 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        10.1.2.1
        Source list is empty

        Interface:        GigabitEthernet1
        Group:                239.3.3.3
        Flags:                L 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        10.1.2.1
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          1.1.1.1          00:05:06  stopped   stopped   Yes  L

        Interface:        GigabitEthernet1
        Group:                239.2.2.2
        Flags:                L U 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        10.1.2.1
        Source list is empty

        Interface:        GigabitEthernet1
        Group:                239.5.5.5
        Flags:                SG 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Source list is empty

        Interface:        GigabitEthernet1
        Group:                239.4.4.4
        Flags:                L 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        10.1.2.1
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          1.1.1.2          00:05:06  stopped   stopped   Yes  L

        Interface:        GigabitEthernet1
        Group:                239.7.7.7
        Flags:                SS 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          2.2.2.1          00:05:06  stopped   stopped   Yes  S

        Interface:        GigabitEthernet1
        Group:                239.6.6.6
        Flags:                SG 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Source list is empty

        Interface:        GigabitEthernet1
        Group:                239.9.9.9
        Flags:                Ac 
        Uptime:                00:23:15
        Group mode:        EXCLUDE (Expires: 00:06:06)
        Last reporter:        10.1.2.2
        Source list is empty

        Interface:        GigabitEthernet1
        Group:                239.8.8.8
        Flags:                SS 
        Uptime:                00:05:06
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          2.2.2.1          00:05:06  stopped   stopped   Yes  S
          2.2.2.2          00:05:06  stopped   stopped   Yes  S

        Interface:        GigabitEthernet1
        Group:                224.0.1.40
        Flags:                L U 
        Uptime:                00:25:33
        Group mode:        INCLUDE
        Last reporter:        10.1.2.1
        Source list is empty
    '''}
    
    golden_parsed_output_1 = {
        "vrf": {
            "VRF1": {
                 "interface": {
                      "GigabitEthernet2": {
                           "static_group": {
                                "239.5.5.5 *": {
                                     "last_reporter": "0.0.0.0",
                                     "up_time": "00:06:17",
                                     "flags": "SG"
                                },
                                "239.6.6.6 *": {
                                     "last_reporter": "0.0.0.0",
                                     "up_time": "00:06:14",
                                     "flags": "SG"
                                }
                           },
                           "join_group": {
                                "239.8.8.8 2.2.2.2": {
                                     "last_reporter": "0.0.0.0",
                                     "flags": "SS",
                                     "foward": True,
                                     "csr_exp": "stopped",
                                     "up_time": "00:05:59",
                                     "v3_exp": "stopped"
                                },
                                "239.3.3.3 1.1.1.1": {
                                     "last_reporter": "20.1.2.1",
                                     "flags": "L",
                                     "foward": True,
                                     "csr_exp": "stopped",
                                     "up_time": "00:06:24",
                                     "v3_exp": "stopped"
                                },
                                "239.1.1.1 *": {
                                     "last_reporter": "20.1.2.1",
                                     "up_time": "00:06:24",
                                     "flags": "L U",
                                     "expire": "never"
                                },
                                "239.4.4.4 1.1.1.2": {
                                     "last_reporter": "20.1.2.1",
                                     "flags": "L",
                                     "foward": True,
                                     "csr_exp": "stopped",
                                     "up_time": "00:06:23",
                                     "v3_exp": "stopped"
                                },
                                "239.7.7.7 2.2.2.1": {
                                     "last_reporter": "0.0.0.0",
                                     "flags": "SS",
                                     "foward": True,
                                     "csr_exp": "stopped",
                                     "up_time": "00:06:06",
                                     "v3_exp": "stopped"
                                },
                                "239.2.2.2 *": {
                                     "last_reporter": "20.1.2.1",
                                     "up_time": "00:06:24",
                                     "flags": "L U",
                                     "expire": "never"
                                },
                                "239.8.8.8 2.2.2.1": {
                                     "last_reporter": "0.0.0.0",
                                     "flags": "SS",
                                     "foward": True,
                                     "csr_exp": "stopped",
                                     "up_time": "00:05:59",
                                     "v3_exp": "stopped"
                                },
                                "224.0.1.40 *": {
                                     "last_reporter": "20.1.2.1",
                                     "up_time": "00:25:55",
                                     "flags": "L U"
                                }
                           },
                           "group": {
                                "239.4.4.4": {
                                     "group_mode": "include",
                                     "last_reporter": "20.1.2.1",
                                     "flags": "L",
                                     "source": {
                                          "1.1.1.2": {
                                               "foward": True,
                                               "flags": "L",
                                               "up_time": "00:06:23",
                                               "v3_exp": "stopped",
                                               "csr_exp": "stopped"
                                          }
                                     },
                                     "up_time": "00:06:23"
                                },
                                "239.5.5.5": {
                                     "group_mode": "include",
                                     "last_reporter": "0.0.0.0",
                                     "flags": "SG",
                                     "up_time": "00:06:17"
                                },
                                "239.1.1.1": {
                                     "group_mode": "exclude",
                                     "last_reporter": "20.1.2.1",
                                     "flags": "L U",
                                     "up_time": "00:06:24",
                                     "expire": "never"
                                },
                                "239.3.3.3": {
                                     "group_mode": "include",
                                     "last_reporter": "20.1.2.1",
                                     "flags": "L",
                                     "source": {
                                          "1.1.1.1": {
                                               "foward": True,
                                               "flags": "L",
                                               "up_time": "00:06:24",
                                               "v3_exp": "stopped",
                                               "csr_exp": "stopped"
                                          }
                                     },
                                     "up_time": "00:06:24"
                                },
                                "239.6.6.6": {
                                     "group_mode": "include",
                                     "last_reporter": "0.0.0.0",
                                     "flags": "SG",
                                     "up_time": "00:06:14"
                                },
                                "239.8.8.8": {
                                     "group_mode": "include",
                                     "last_reporter": "0.0.0.0",
                                     "flags": "SS",
                                     "source": {
                                          "2.2.2.1": {
                                               "foward": True,
                                               "flags": "S",
                                               "up_time": "00:03:56",
                                               "v3_exp": "stopped",
                                               "csr_exp": "stopped"
                                          },
                                          "2.2.2.2": {
                                               "foward": True,
                                               "flags": "S",
                                               "up_time": "00:05:57",
                                               "v3_exp": "stopped",
                                               "csr_exp": "stopped"
                                          }
                                     },
                                     "up_time": "00:05:59"
                                },
                                "224.0.1.40": {
                                     "group_mode": "include",
                                     "last_reporter": "20.1.2.1",
                                     "flags": "L U",
                                     "up_time": "00:25:55"
                                },
                                "239.7.7.7": {
                                     "group_mode": "include",
                                     "last_reporter": "0.0.0.0",
                                     "flags": "SS",
                                     "source": {
                                          "2.2.2.1": {
                                               "foward": True,
                                               "flags": "S",
                                               "up_time": "00:06:06",
                                               "v3_exp": "stopped",
                                               "csr_exp": "stopped"
                                          }
                                     },
                                     "up_time": "00:06:06"
                                },
                                "239.2.2.2": {
                                     "group_mode": "exclude",
                                     "last_reporter": "20.1.2.1",
                                     "flags": "L U",
                                     "up_time": "00:06:24",
                                     "expire": "never"
                                }
                           }
                      }
                 }
            }
       }
    }

    golden_output_1 = {'execute.return_value': '''\
        Flags: L - Local, U - User, SG - Static Group, VG - Virtual Group,
               SS - Static Source, VS - Virtual Source,
               Ac - Group accounted towards access control limit

        Interface:        GigabitEthernet2
        Group:                239.1.1.1
        Flags:                L U 
        Uptime:                00:06:24
        Group mode:        EXCLUDE (Expires: never)
        Last reporter:        20.1.2.1
        Source list is empty

        Interface:        GigabitEthernet2
        Group:                239.3.3.3
        Flags:                L 
        Uptime:                00:06:24
        Group mode:        INCLUDE
        Last reporter:        20.1.2.1
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          1.1.1.1          00:06:24  stopped   stopped   Yes  L

        Interface:        GigabitEthernet2
        Group:                239.2.2.2
        Flags:                L U 
        Uptime:                00:06:24
        Group mode:        EXCLUDE (Expires: never)
        Last reporter:        20.1.2.1
        Source list is empty

        Interface:        GigabitEthernet2
        Group:                239.5.5.5
        Flags:                SG 
        Uptime:                00:06:17
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Source list is empty

        Interface:        GigabitEthernet2
        Group:                239.4.4.4
        Flags:                L 
        Uptime:                00:06:23
        Group mode:        INCLUDE
        Last reporter:        20.1.2.1
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          1.1.1.2          00:06:23  stopped   stopped   Yes  L

        Interface:        GigabitEthernet2
        Group:                239.7.7.7
        Flags:                SS 
        Uptime:                00:06:06
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          2.2.2.1          00:06:06  stopped   stopped   Yes  S

        Interface:        GigabitEthernet2
        Group:                239.6.6.6
        Flags:                SG 
        Uptime:                00:06:14
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Source list is empty

        Interface:        GigabitEthernet2
        Group:                239.8.8.8
        Flags:                SS 
        Uptime:                00:05:59
        Group mode:        INCLUDE
        Last reporter:        0.0.0.0
        Group source list: (C - Cisco Src Report, U - URD, R - Remote, S - Static,
                            V - Virtual, M - SSM Mapping, L - Local,
                            Ac - Channel accounted towards access control limit)
          Source Address   Uptime    v3 Exp   CSR Exp   Fwd  Flags
          2.2.2.1          00:03:56  stopped   stopped   Yes  S
          2.2.2.2          00:05:57  stopped   stopped   Yes  S

        Interface:        GigabitEthernet2
        Group:                224.0.1.40
        Flags:                L U 
        Uptime:                00:25:55
        Group mode:        INCLUDE
        Last reporter:        20.1.2.1
        Source list is empty
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowIpIgmpGroupsDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden_default_vrf(self):
        self.device = Mock(**self.golden_output)
        obj = ShowIpIgmpGroupsDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output)

    def test_golden_non_default_vrf(self):
        self.device = Mock(**self.golden_output_1)
        obj = ShowIpIgmpGroupsDetail(device=self.device)
        parsed_output = obj.parse(vrf='VRF1')
        self.assertEqual(parsed_output,self.golden_parsed_output_1)


# ===========================================================
# Unit test for 'show ip igmp ssm-mapping <WROD>'
# Unit test for 'show ip igmp vrf <WORD> ssm-mapping <WORD>'
# ============================================================
class test_show_ip_igmp_ssm_mapping(unittest.TestCase):
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output = {
        'vrf': {
            'default': {
                'ssm_map': {
                    '1.1.1.1': {
                        'source_addr': '1.1.1.1',
                        'group_address': '239.1.1.1',
                        'database': 'static',
                    },
                    '2.2.2.2': {
                        'source_addr': '2.2.2.2',
                        'group_address': '239.1.1.1',
                        'database': 'static',
                    },
                }
            }
        }
    }

    golden_output = {'execute.return_value': '''\
        Group address: 239.1.1.1
        Database     : Static
        Source list  : 1.1.1.1
                       2.2.2.2
    '''}
    
    golden_parsed_output_1 = {
        'vrf': {
            'VRF1': {
                'ssm_map': {
                    '1.1.1.1': {
                        'source_addr': '1.1.1.1',
                        'group_address': '239.1.1.1',
                        'database': 'static',
                    },
                    '2.2.2.2': {
                        'source_addr': '2.2.2.2',
                        'group_address': '239.1.1.1',
                        'database': 'static',
                    },
                }
            }
        }
    }

    golden_output_1 = {'execute.return_value': '''\
        Group address: 239.1.1.1
        Database     : Static
        Source list  : 1.1.1.1
                       2.2.2.2
    '''}

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowIpIgmpSsmMapping(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse(group='239.1.1.1')

    def test_golden_default_vrf(self):
        self.device = Mock(**self.golden_output)
        obj = ShowIpIgmpSsmMapping(device=self.device)
        parsed_output = obj.parse(group='239.1.1.1')
        self.assertEqual(parsed_output,self.golden_parsed_output)

    def test_golden_non_default_vrf(self):
        self.device = Mock(**self.golden_output_1)
        obj = ShowIpIgmpSsmMapping(device=self.device)
        parsed_output = obj.parse(vrf='VRF1', group='239.1.1.1')
        self.assertEqual(parsed_output,self.golden_parsed_output_1)

if __name__ == '__main__':
    unittest.main()