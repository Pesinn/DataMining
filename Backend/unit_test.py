import unittest2
import content.domain.sentiment.sentiment_analysis_factory_test as t

class TestStringMethods(unittest2.TestCase):

  def test_upper(self):
    self.assertEqual('foo'.upper(), 'FOO')

unittest2.main()

t.test()