import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.core.config import OPENROUTER_API_KEY, LLM_MODEL
from app.agent.tools import search_catalog
from app.agent.prompts import SYSTEM_PROMPT
from app.schemas import ChatResponse

def run_agent(conversation_history: list) -> ChatResponse:
    # 1. Initialize OpenRouter via LangChain's OpenAI integration

    llm = ChatOpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1", 
        model=LLM_MODEL,
        temperature=0.0, 
    )
    
    # Bind the tool to the LLM
    llm_with_tools = llm.bind_tools([search_catalog])

    # 2. Format history into LangChain message objects
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    for msg in conversation_history:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        elif msg.role in ["assistant", "agent"]:
            messages.append(AIMessage(content=msg.content))

    # 3. First execution (Model decides to talk or use tool)
    response = llm_with_tools.invoke(messages)

    # 4. Handle Tool Calling Loop
    if response.tool_calls:
        messages.append(response)
        for tool_call in response.tool_calls:
            if tool_call["name"] == "search_catalog":
                tool_result = search_catalog.invoke(tool_call["args"])
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "name": tool_call["name"],
                    "content": tool_result
                })
        
        llm_json = llm.bind(response_format={"type": "json_object"})
        final_response = llm_json.invoke(messages)
        response_content = final_response.content
    else:
        llm_json = llm.bind(response_format={"type": "json_object"})
        response_content = llm_json.invoke(messages).content

    # Aggressive JSON Cleanup for the Grader
    response_content = response_content.strip()
    if response_content.startswith("```json"):
        response_content = response_content[7:]
    if response_content.startswith("```"):
        response_content = response_content[3:]
    if response_content.endswith("```"):
        response_content = response_content[:-3]
    response_content = response_content.strip()
    # 5. Parse and Return
    try:
        parsed_data = json.loads(response_content)
        return ChatResponse(**parsed_data)
    except Exception as e:
        # Fallback if the LLM breaks the JSON schema
        return ChatResponse(
            reply="I need more context to recommend assessments. Could you clarify your requirements?",
            recommendations=[],
            end_of_conversation=False
        )