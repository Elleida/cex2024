import streamlit as st
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import YouTubeSearchTool
from googlesearchtool import GoogleSearchTool
from langchain_openai import ChatOpenAI


st.set_page_config(page_title="Agent", page_icon='📃',layout='wide')
st.title("Agente000 :sunglasses:")
st.subheader("Tools: wikipediasearch,youtubevideo,ddg-search", divider="red", anchor=False)

api_wrapper = WikipediaAPIWrapper(top_k_results=10, doc_content_chars_max=512)
wikipediasearch = WikipediaQueryRun(api_wrapper=api_wrapper)
youtubevideo = YouTubeSearchTool()
if "messages" not in st.session_state:
    st.session_state.messages = []
llm=ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, streaming=True)
tools = load_tools(["ddg-search"])
tools.append(wikipediasearch)
tools.append(youtubevideo)
prompt = hub.pull("hwchase17/openai-functions-agent")

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5,return_intermediate_steps=True,handle_parsing_errors=True)
if st.button("Clean agente000"):
    st.session_state.messages = []
if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    messages=[
            {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke(
            {"input": messages}, {"callbacks": [st_callback]}
        )
        st.write(response["output"])