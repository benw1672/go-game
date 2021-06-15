import unittest

from test.board_unittests import BoardUnitTests
from test.player_unittests import PlayerUnitTests
from test.point_unittests import PointUnitTests
from test.rule_checker_unittests import RuleCheckerUnitTests


def suite():
    suite = unittest.TestSuite()
    suite.addTest(BoardUnitTests('test_board_eq'))
    suite.addTest(PlayerUnitTests('test_player_eq'))
    suite.addTest(PointUnitTests('test_point_eq'))
    suite.addTest(PointUnitTests('test_bounds_checking'))
    suite.addTest(RuleCheckerUnitTests('test_get_scores'))
    suite.addTest(RuleCheckerUnitTests('test_history_len_1'))
    suite.addTest(RuleCheckerUnitTests('test_is_history_legal'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())