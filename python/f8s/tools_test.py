import unittest

import f8s.tools
# ------------------------------------------------------------------------------


class ToolsTests(unittest.TestCase):
    def test_error_to_response(self):
        error = TypeError('foo')
        result = f8s.tools.error_to_response(error)
        self.assertEqual(result.mimetype, 'application/json')
        self.assertEqual(result.json['error'], 'TypeError')
        self.assertEqual(result.json['args'], ['foo'])
        self.assertEqual(result.json['message'], 'TypeError(\n    foo\n)')
        self.assertEqual(result.json['code'], 500)

    def test_error_to_response_dict(self):
        arg = {
            'bars': {
                f'bar-{i:02d}': {
                    f'bar-{i:02d}': 'banana'
                } for i in range(3)
            },
            'foos': [['pizza'] * 3] * 3,
        }
        error = TypeError(arg, arg, 'arg2')
        result = f8s.tools.error_to_response(error)

        expected = r'''
TypeError(
    {'bars': "{'bar-00': {'bar-00': 'banana'},\n"
         " 'bar-01': {'bar-01': 'banana'},\n"
         " 'bar-02': {'bar-02': 'banana'}}"}
    {'foos': "[['pizza', 'pizza', 'pizza'],\n"
         " ['pizza', 'pizza', 'pizza'],\n"
         " ['pizza', 'pizza', 'pizza']]"}
    {'bars': "{'bar-00': {'bar-00': 'banana'},\n"
         " 'bar-01': {'bar-01': 'banana'},\n"
         " 'bar-02': {'bar-02': 'banana'}}"}
    {'foos': "[['pizza', 'pizza', 'pizza'],\n"
         " ['pizza', 'pizza', 'pizza'],\n"
         " ['pizza', 'pizza', 'pizza']]"}
    arg2
)'''[1:]

        self.assertEqual(result.mimetype, 'application/json')
        self.assertEqual(result.json['error'], 'TypeError')
        self.assertEqual(result.json['args'][0], str(arg))
        self.assertEqual(result.json['args'][1], str(arg))
        self.assertEqual(result.json['args'][2], 'arg2')
        self.assertEqual(result.json['message'], expected)
        self.assertEqual(result.json['code'], 500)
