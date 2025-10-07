"""
econdata_langgraph.py: FRED Agent with LangGraph
================================================
A concise LangGraph implementation demonstrating graph-based agent architecture
for economic data retrieval. Maintains the same flow as econdata.py but with
explicit state management and graph structure.

Setup:
1. pip install openai fredapi python-dotenv colorama langgraph grandalf "langsmith==0.3.45"
2. Use an .env file with FRED_API_KEY and OPENAI_API_KEY
"""

import os, json
from datetime import datetime, timedelta
from typing import TypedDict, Optional
from dotenv import load_dotenv
from fredapi import Fred
from openai import OpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# State definition - data that flows through the graph
class AgentState(TypedDict):
    question: str
    series_code: Optional[str]
    data_value: Optional[float]
    data_date: Optional[str]
    units: Optional[str]
    response: Optional[str]
    error: Optional[str]

# Initialize clients
fred = Fred(api_key=os.getenv('FRED_API_KEY'))
llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Node functions - each represents a step in our analysis
def think_node(state):
    """Determine which FRED series to fetch based on the question."""
    prompt = f"""What FRED series code would help answer this question? 
Question: {state['question']}
    
Common FRED codes: UNRATE (unemployment), FPCPITOTLZGUSA (CPI inflation), GDP, DFF (fed funds rate)

Return JSON: {{"series_code": "CODE"}}"""
    
    response = llm.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    result = json.loads(response.choices[0].message.content)
    return {"series_code": result['series_code']}

def act_node(state):
    """Fetch data from FRED API."""
    try:
        # Get series info and recent data
        info = fred.get_series_info(state['series_code'])
        data = fred.get_series(
            state['series_code'], 
            observation_start=datetime.now() - timedelta(days=365)
        )
        
        return {
            "data_value": float(data.iloc[-1]),
            "data_date": data.index[-1].strftime("%Y-%m-%d"),
            "units": info['units']
        }
    except Exception as e:
        return {"error": str(e)}

def respond_node(state):
    """Generate natural language response from the data."""
    if state.get('error'):
        return {"response": f"Error: {state['error']}"}
    
    prompt = f"""Answer this question using the data:
    Question: {state['question']}
    Data: {state['data_value']} {state['units']} as of {state['data_date']}"""
    
    response = llm.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return {"response": response.choices[0].message.content}

# Build the graph
def create_fred_agent():
    """Construct the agent graph."""
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("think", think_node)
    graph.add_node("act", act_node)
    graph.add_node("respond", respond_node)
    
    # Define flow
    graph.add_edge("think", "act")
    graph.add_edge("act", "respond")
    graph.add_edge("respond", END)
    
    # Set entry point
    graph.set_entry_point("think")
    
    return graph.compile()

# Example usage
if __name__ == "__main__":
    agent = create_fred_agent()
    question = "How is the US labor market doing?"
    result = agent.invoke({"question": question})
    
    print(f"\nQuestion: {question}")
    print(f"Answer: {result['response']}")
     
    # Show graph structure
    print("\nGraph Structure:")
    print(agent.get_graph().draw_ascii())