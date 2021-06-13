import unittest, sys, os
sys.path.append(os.path.abspath('..'))
from players.simple_player import SimplePlayer
from players.order_proxy_player import OrderProxyPlayer
from players.history_check_proxy_player import HistoryCheckProxyPlayer

class PlayerUnitTests(unittest.TestCase):
    def test_player_eq(self):
        unwrapped = SimplePlayer()
        unwrapped.register()
        wrapped = OrderProxyPlayer(unwrapped)
        double_wrapped = HistoryCheckProxyPlayer(wrapped)
        other = SimplePlayer()
        other.register()
        self.assertEqual(unwrapped, wrapped)
        self.assertEqual(unwrapped, double_wrapped)
        self.assertEqual(wrapped, double_wrapped)
        self.assertNotEqual(unwrapped, other)
        self.assertNotEqual(wrapped, other)
        self.assertNotEqual(other, double_wrapped)
        self.assertNotEqual(double_wrapped, other)


if __name__ == "__main__":
    unittest.main()
