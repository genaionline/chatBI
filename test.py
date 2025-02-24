import os
import configparser
from util.llm_util import send_query, handle_history




if __name__ == "__main__":
    question = 'Hi, give me five common English names.'
    print(send_query(question, []))
