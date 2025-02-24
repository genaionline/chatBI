## Run it by:    streamlit run app.py


import streamlit as st
from util.llm_util import send_query, handle_history

# 初始化聊天记录
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 左侧边栏
st.sidebar.title("ChatBI")
model_name = st.sidebar.selectbox("Model", ["deepseek-r1-14b"])
system_message = st.sidebar.text_input("System Message", "You are a helpful assistant.")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.6)
top_p = st.sidebar.slider("Top-p", 0.0, 1.0, 0.9)
max_tokens = st.sidebar.selectbox("Max Tokens", ["1024", "2048", "4096"])

# 中间聊天窗口
st.title("Chat Window")
chat_input = st.text_input("Your Message", "")

if st.button("Send"):
    if chat_input:
        # 发送消息并获取响应
        response = send_query(chat_input, st.session_state['chat_history'])
        if response:
            st.session_state['chat_history'] = handle_history(st.session_state['chat_history'])

# 显示聊天记录
for message in st.session_state['chat_history']:
    if message['role'] == 'user':
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Assistant:** {message['content']}")

# 右侧可视化和文本信息
st.sidebar.title("Visualization & Info")
st.sidebar.subheader("Visualization")
# 这里可以添加可视化图表的代码
st.sidebar.subheader("Information")
# 这里可以添加文本信息的代码
st.sidebar.text("Some text information here.")
