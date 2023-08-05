from requests import get
from unittest import TestCase, main
try:
    from .find_primes import *

except ImportError:
    from find_primes import *

def get_answer(string):
    try:
        t = get(f'https://oeis.org/{string}').text
    
    except Exception:
        try:
            t = get(f'https://oeis.org/{string}').text
        
        except Exception:
            return
    
    located_1 = t.find('<tt>')
    located_2 = t.find('</tt>')
    answer_str = t[located_1:located_2][4:]
    return [int(x) for x in answer_str.split(', ')]

class TestAnswer(TestCase):
    def test_all_prime(self):
        result = all_primes(275, 'list')
        answer = get_answer('A000040')
        self.assertEqual(result, answer)

    def test_twin_prime(self):
        result = find_twins(1610)
        answer1 = get_answer('A001359')
        answer2 = get_answer('A006512')
        self.assertEqual(list(result.keys()), answer1)
        self.assertEqual(list(result.values()), answer2)
    
    def test_palindome_prime(self):
        result = find_palindromes(18190)
        answer = get_answer('A002385')
        self.assertEqual(result, answer)

if __name__ == '__main__':
    main()