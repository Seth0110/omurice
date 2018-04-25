# ATR2 Test functions
import unittest
import ATR2

class TestMaxShown(unittest.TestCase):

    def test_max_shown(self):
        a = ATR2.max_shown()

        self.assertEqual(a, 6)

class TestMnemonic(unittest.TestCase):

    def test_mnemonic(self):
        a = ATR2.mnemonic(44, 0)

        self.assertEqual(a, "SAR")

class TestOperand(unittest.TestCase):

    @unittest.skip("Can't find True condition")
    def test_Operand(self):
        a = ATR2.operand(9, 9)

        self.assertEqual(a, "@")

# log_error

# integer

class TestGraphCheck(unittest.TestCase):

    def test_graph_check(self):
        a = ATR2.graph_check(0)

        self.assertFalse(a)

# robot_graph

class TestUpdateArmor(unittest.TestCase):

    @unittest.skip("VOID function")
    def test_update_armor(self):
        a = ATR2.update_armor(0)

        self.assertFalse(a)

class TestUpdateHeat(unittest.TestCase):

    @unittest.skip("VOID function")
    def test_update_heat(self):
        a = ATR2.update_heat(0)

        self.assertFalse(a)

# robot error

# update lives

# 

if __name__ == "__main__":
    unittest.main()
