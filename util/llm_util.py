import os
import sys
import openai
import configparser
import requests
# 读取配置文件
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), '../config/llm_config.ini')
config.read(config_path)

# 获取配置信息
openai_config = {
    "api_key": os.getenv("OPENAI_API_KEY", config['openai']['api_key']),
    "model_name": config['openai']['model_name'],
    "api_base": config['openai']['api_base'],
    "timeout": int(config['openai']['timeout']),
    "max_retries": int(config['openai']['max_retries'])
}

# 设置 OpenAI API 密钥和基础 URL
openai.api_key = openai_config['api_key']
openai.api_base = openai_config['api_base']

def is_llm_accessible():
    """检查 LLM 是否可访问"""
    try:
        if 'localhost' in openai.api_base:
            response = requests.get(openai_config['api_base'], timeout=5)
            print('Got response from localhost:', response.status_code)
        else:
            # 尝试调用 OpenAI API 的一个简单请求
            openai.Engine.list()
        return True
    except Exception as e:
        print(f"Error accessing LLM: {e}")
        return False

def send_query(message, chatHistory):
    """发送查询消息并获取 LLM 响应"""
    # 更新聊天记录
    chatHistory.append({"role": "user", "content": message})

    # 将聊天记录转换为字符串
    history_as_text = "\n".join([f"{entry['role']}: {entry['content']}" for entry in chatHistory])

    try:
        response = openai.Completion.create(
            model=openai_config['model_name'],
            prompt=history_as_text,  # 使用完整的聊天记录作为 prompt
            timeout=openai_config['timeout'],
            max_tokens=4096,  # 根据需要调整
            temperature=0.6  # 根据需要调整
        )
        
        # 获取 LLM 的响应内容
        llm_response = response['choices'][0]['text'].strip()
        
        # 更新聊天记录
        chatHistory.append({"role": "assistant", "content": llm_response})
        
        return llm_response
    except openai.error.OpenAIError as e:
        print(f"Error sending query: {e}")
        return None

def handle_history(messages):
    """处理历史消息"""
    # 这里可以根据需要实现历史消息的存储和管理
    # 例如，可以将消息保存到文件或数据库中
    return messages  # 返回处理后的消息 


