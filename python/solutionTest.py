import unittest
from preloaded import simulate
from solution import Compiler

class Test(unittest.TestCase):
    def test_basic_functionality(self):
        prog = '[ x y z ] ( 2*3*x + 5*y - 3*z ) / (1 + 3 + 2*2)';
        t1 = {'op':'/','a':{'op':'-','a':{'op':'+','a':{'op':'*','a':{'op':'*','a':{'op':'imm','n':2},'b':{'op':'imm','n':3}},'b':{'op':'arg','n':0}},'b':{'op':'*','a':{'op':'imm','n':5},'b':{'op':'arg','n':1}}},'b':{'op':'*','a':{'op':'imm','n':3},'b':{'op':'arg','n':2}}},'b':{'op':'+','a':{'op':'+','a':{'op':'imm','n':1},'b':{'op':'imm','n':3}},'b':{'op':'*','a':{'op':'imm','n':2},'b':{'op':'imm','n':2}}}};
        t2 = {'op':'/','a':{'op':'-','a':{'op':'+','a':{'op':'*','a':{'op':'imm','n':6},'b':{'op':'arg','n':0}},'b':{'op':'*','a':{'op':'imm','n':5},'b':{'op':'arg','n':1}}},'b':{'op':'*','a':{'op':'imm','n':3},'b':{'op':'arg','n':2}}},'b':{'op':'imm','n':8}};
        c = Compiler()
        self.assertTrue(c, 'Able to construct compiler')
        
        p1 = c.pass1(prog)
        self.assertEqual(p1, t1, 'Pass1')
        
        p2 = c.pass2(p1)
        self.assertEqual(p2, t2, 'Pass2')
        
        p3 = c.pass3(p2)
        print(p3)
        self.assertEqual(simulate(p3, [4,0,0]), 3, 'prog(4,0,0) == 3')
        self.assertEqual(simulate(p3, [4,8,0]), 8, 'prog(4,8,0) == 8')
        self.assertEqual(simulate(p3, [4,8,16]), 2, 'prog(4,8,6) == 2')
