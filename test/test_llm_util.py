import unittest
from unittest.mock import patch, MagicMock
from util.llm_util import is_llm_accessible, send_query

class TestLLMUtil(unittest.TestCase):

    @patch('util.llm_util.openai.Engine.list')
    def test_is_llm_accessible_success(self, mock_list):
        """测试 LLM 可访问性 - 成功"""
        mock_list.return_value = MagicMock()
        self.assertTrue(is_llm_accessible())


    @patch('util.llm_util.openai.ChatCompletion.create')
    def test_send_query_success(self, mock_create):
        """测试发送查询消息 - 成功"""
        mock_response = {
            'choices': [{'message': {'content': 'Hello, user!'}}]
        }
        mock_create.return_value = mock_response

        chatHistory = []
        response = send_query("Hello, LLM!", chatHistory)
        
        self.assertEqual(response, 'Hello, user!')
        self.assertEqual(len(chatHistory), 2)
        self.assertEqual(chatHistory[0]['content'], "Hello, LLM!")
        self.assertEqual(chatHistory[1]['content'], "Hello, user!")

    @patch('util.llm_util.openai.ChatCompletion.create')
    def test_send_query_failure(self, mock_create):
        """测试发送查询消息 - 失败"""
        mock_create.side_effect = Exception("API Error")

        chatHistory = []
        response = send_query("Hello, LLM!", chatHistory)
        
        self.assertIsNone(response)
        self.assertEqual(len(chatHistory), 1)
        self.assertEqual(chatHistory[0]['content'], "Hello, LLM!")

if __name__ == '__main__':
    unittest.main()



####
##   python -m unittest discover -s test -p "test_*.py"
###