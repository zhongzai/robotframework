import unittest
import os
from os.path import abspath, dirname, join, normpath

from robot.utils.asserts import assert_equals
from robot.testdoc import JsonConverter, TestSuiteFactory

DATADIR = join(dirname(abspath(__file__)), '..', '..', 'atest', 'testdata', 'misc')


def test_convert(item, **expected):
    for name in expected:
        assert_equals(item[name], expected[name])


class TestJsonConverter(unittest.TestCase):
    suite = None

    def setUp(self):
        if not self.suite:
            suite = TestSuiteFactory(DATADIR, doc='My doc', metadata=['abc:123'])
            output = join(DATADIR, '..', 'output.html')
            self.__class__.suite = JsonConverter(output).convert(suite)

    def test_suite(self):
        test_convert(self.suite,
                     source=normpath(DATADIR),
                     relativeSource='misc',
                     id='s1',
                     name='Misc',
                     fullName='Misc',
                     doc='My doc',
                     metadata={'abc': '123'},
                     numberOfTests=162,
                     tests=[],
                     keywords=[])
        test_convert(self.suite['suites'][1],
                     source=join(normpath(DATADIR), 'dummy_lib_test.html'),
                     relativeSource=join('misc', 'dummy_lib_test.html'),
                     id='s1-s2',
                     name='Dummy Lib Test',
                     fullName='Misc.Dummy Lib Test',
                     doc='',
                     metadata={},
                     numberOfTests=1,
                     suites=[],
                     keywords=[])
        test_convert(self.suite['suites'][4]['suites'][1]['suites'][-1],
                     source=join(normpath(DATADIR), 'multiple_suites',
                                 '02__sub.suite.1', 'second__.Sui.te.2..html'),
                     relativeSource=join('misc', 'multiple_suites',
                                         '02__sub.suite.1', 'second__.Sui.te.2..html'),
                     id='s1-s5-s2-s2',
                     name='.Sui.te.2.',
                     fullName='Misc.Multiple Suites.Sub.Suite.1..Sui.te.2.',
                     doc='',
                     metadata={},
                     numberOfTests=12,
                     suites=[],
                     keywords=[])

    def test_multi_suite(self):
        data = TestSuiteFactory([join(DATADIR, 'normal.html'),
                                 join(DATADIR, 'pass_and_fail.html')])
        suite = JsonConverter().convert(data)
        test_convert(suite,
                     source='',
                     relativeSource='',
                     id='s1',
                     name='Normal & Pass And Fail',
                     fullName='Normal & Pass And Fail',
                     doc='',
                     metadata={},
                     numberOfTests=4,
                     keywords=[],
                     tests=[])
        test_convert(suite['suites'][0],
                     source=normpath(join(DATADIR, 'normal.html')),
                     relativeSource='',
                     id='s1-s1',
                     name='Normal',
                     fullName='Normal & Pass And Fail.Normal',
                     doc='Normal test cases',
                     metadata={'Something': 'My Value'},
                     numberOfTests=2)
        test_convert(suite['suites'][1],
                     source=normpath(join(DATADIR, 'pass_and_fail.html')),
                     relativeSource='',
                     id='s1-s2',
                     name='Pass And Fail',
                     fullName='Normal & Pass And Fail.Pass And Fail',
                     doc='Some tests here',
                     metadata={},
                     numberOfTests=2)

    def test_test(self):
        test_convert(self.suite['suites'][1]['tests'][0],
                     id='s1-s2-t1',
                     name='Dummy Test',
                     fullName='Misc.Dummy Lib Test.Dummy Test',
                     doc='',
                     tags=[],
                     timeout='')
        test_convert(self.suite['suites'][3]['tests'][-1],
                     id='s1-s4-t5',
                     name='Fifth',
                     fullName='Misc.Many Tests.Fifth',
                     doc='',
                     tags=['d1', 'd2', 'f1'],
                     timeout='')
        test_convert(self.suite['suites'][-3]['tests'][0],
                     id='s1-s10-t1',
                     name='Default Test Timeout',
                     fullName='Misc.Timeouts.Default Test Timeout',
                     doc='I have a timeout',
                     tags=[],
                     timeout='1 minute 42 seconds')

    def test_timeout(self):
        test_convert(self.suite['suites'][-3]['tests'][0],
                     name='Default Test Timeout',
                     timeout='1 minute 42 seconds')
        test_convert(self.suite['suites'][-3]['tests'][1],
                     name='Test Timeout With Message',
                     timeout='1 day 2 hours :: The message')
        test_convert(self.suite['suites'][-3]['tests'][2],
                     name='Test Timeout With Variable',
                     timeout='${100}')

    def test_keyword(self):
        test_convert(self.suite['suites'][1]['tests'][0]['keywords'][0],
                     name='dummykw',
                     arguments='',
                     type='KEYWORD')
        test_convert(self.suite['suites'][3]['tests'][-1]['keywords'][0],
                     name='Log',
                     arguments='Test 5',
                     type='KEYWORD')

    def test_suite_setup_and_teardown(self):
        test_convert(self.suite['suites'][3]['keywords'][0],
                     name='Log',
                     arguments='Setup',
                     type='SETUP')
        test_convert(self.suite['suites'][3]['keywords'][1],
                     name='Noop',
                     arguments='',
                     type='TEARDOWN')

    def test_test_setup_and_teardown(self):
        test_convert(self.suite['suites'][7]['tests'][0]['keywords'][0],
                     name='Test Setup',
                     arguments='',
                     type='SETUP')
        test_convert(self.suite['suites'][7]['tests'][0]['keywords'][2],
                     name='Test Teardown',
                     arguments='',
                     type='TEARDOWN')

    def test_for_loops(self):
        test_convert(self.suite['suites'][2]['tests'][0]['keywords'][0],
                     name='${pet} IN [ cat | dog | horse ]',
                     arguments='',
                     type='FOR')
        test_convert(self.suite['suites'][2]['tests'][1]['keywords'][0],
                     name='${i} IN RANGE [ 10 ]',
                     arguments='',
                     type='FOR')

    def test_assign(self):
        test_convert(self.suite['suites'][-2]['tests'][0]['keywords'][1],
                     name='${msg} = Evaluate',
                     arguments="u'Fran\\\\xe7ais'",
                     type='KEYWORD')


if __name__ == '__main__':
    unittest.main()