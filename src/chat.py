from prompt_template import PROMPT_TEMPLATE

import json
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from search import search_vector

from dotenv import load_dotenv

load_dotenv()

@tool("search_vector_tool")
def search_vector_tool(question: str) -> str:
    """Retorna uma lista com texto, score e metadados dos documentos encontrados."""
    return json.dumps(search_vector(question))

def main():

    llm = ChatOpenAI(model="gpt-5-mini", disable_streaming=True)
    tools = [search_vector_tool]

    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

    agent_chain = create_react_agent(llm, tools, prompt, stop_sequence=False)

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent_chain, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors="Invalid format. Either provide an Action with Action Input, or a Final Answer only.",
        max_iterations=3
        )

    print("Chat com IA iniciado! Digite 'sair' para encerrar.")    

    while True:
        usuario_msg = input("\nVocê: ")
        
        if usuario_msg.lower() == "sair":
            break
            
        # Envia a mensagem para o modelo e obtém a resposta mantendo o contexto
        resposta = agent_executor.invoke({"input": str(usuario_msg)})

        print(f"AI Agent: {str(resposta)}")

if __name__ == "__main__":
    main()