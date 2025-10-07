"""
deep_research_agent.py: Deep Research Agent for Economic Research using LangGraph
================================================================================
A multi-agent system that performs comprehensive research on economic topics through:
1. Lead Researcher - Develops research strategy and synthesizes findings
2. Search Agents - Execute parallel searches across multiple sources  
3. Analysis Agents - Analyze results from different perspectives
4. Synthesis Agent - Integrates all findings into a comprehensive report

Setup:
1. pip install langchain-openai langgraph tavily-python python-dotenv
2. Get API keys from:
   - OpenAI: https://platform.openai.com/api-keys
   - Tavily: https://app.tavily.com/
3. Create .env file with your keys in the following format:
   OPENAI_API_KEY=[enter key]
   
"""

import os
from typing import Dict, List, TypedDict, Annotated, Literal
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from tavily import TavilyClient

# Load environment variables
load_dotenv()

class ResearchState(TypedDict):
    question: str
    research_plan: Dict[str, List[str]]
    subtasks: List[Dict[str, str]]
    search_results: List[Dict[str, any]]
    analysis_results: List[Dict[str, str]]
    final_report: str



class ResearchState(TypedDict):
    """State that flows through the research graph"""
    question: str
    research_plan: Dict[str, List[str]]
    subtasks: List[Dict[str, str]]
    search_results: List[Dict[str, any]]
    analysis_results: List[Dict[str, str]]
    final_report: str
    messages: Annotated[List, add_messages]
    current_subtask: int
    max_iterations: int

# Perform parallel searches using ThreadPoolExecutor
search_futures = []
for query in subtask['search_queries']:
    future = self.executor.submit(self._perform_search, query)
    search_futures.append(future)

# Collect results from all parallel searches
for future in search_futures:
    results = future.result()
    state['search_results'].extend(results)
class DeepResearchAgent:
    """Multi-agent system for deep economic research"""
    
    def __init__(self, openai_api_key: str = None, tavily_api_key: str = None):
        # Use provided keys or fall back to environment variables
        openai_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        tavily_key = tavily_api_key or os.getenv('TAVILY_API_KEY')
        
        if not openai_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in .env file")
        if not tavily_key:
            raise ValueError("Tavily API key not found. Please set TAVILY_API_KEY in .env file")
        
        # Initialize LLMs
        self.lead_llm = ChatOpenAI(
            model="gpt-4.1",
            temperature=0.1,
            api_key=openai_key
        )
        self.analysis_llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0.1,
            api_key=openai_key
        )
        
        # Initialize tools
        self.tavily = TavilyClient(api_key=tavily_key)
        self.executor = ThreadPoolExecutor(max_workers=10)  # Increased for more parallelism
        
        # Build the research graph
        self.graph = self._build_graph()
    def _build_graph(self) -> StateGraph:
        """Construct the research workflow graph"""
        workflow = StateGraph(ResearchState)
        
        # Add nodes
        workflow.add_node("lead_researcher", self.lead_researcher_node)
        workflow.add_node("spawn_subtasks", self.spawn_subtasks_node)
        workflow.add_node("search_agent", self.search_agent_node)
        workflow.add_node("analysis_agent", self.analysis_agent_node)
        workflow.add_node("synthesis_agent", self.synthesis_agent_node)
        
        # Define edges
        workflow.set_entry_point("lead_researcher")
        workflow.add_edge("lead_researcher", "spawn_subtasks")
        workflow.add_edge("spawn_subtasks", "search_agent")
        workflow.add_conditional_edges(
            "search_agent",
            self.should_continue_searching,
            {
                "continue": "search_agent",
                "analyze": "analysis_agent"
            }
        )
        workflow.add_edge("analysis_agent", "synthesis_agent")
        workflow.add_edge("synthesis_agent", END)
        
        return workflow.compile()

    # --- NODE IMPLEMENTATIONS ---

    def lead_researcher_node(self, state: ResearchState) -> ResearchState:
        prompt = (
            f"You are a lead economic researcher. "
            f"Given the question: '{state['question']}', "
            f"break it down into 2-4 key research topics and for each, "
            f"list 1-3 specific search queries."
        )
        response = self.lead_llm.invoke([SystemMessage(content=prompt)])
        # Expecting the LLM to return a JSON-like plan
        try:
            plan = json.loads(response.content)
        except Exception:
            plan = {"General": [state['question']]}
        state["research_plan"] = plan
        state["messages"] = state.get("messages", []) + ["Lead researcher: Created research plan."]
        return state

    def spawn_subtasks_node(self, state: ResearchState) -> ResearchState:
        # Create subtasks from the research plan
        subtasks = []
        for topic, queries in state["research_plan"].items():
            for q in queries:
                subtasks.append({"topic": topic, "search_queries": [q]})
        state["subtasks"] = subtasks
        state["current_subtask"] = 0
        state["messages"] = state.get("messages", []) + ["Spawned subtasks."]
        return state

    def search_agent_node(self, state: ResearchState) -> ResearchState:
        idx = state.get("current_subtask", 0)
        if idx >= len(state["subtasks"]):
            return state
        subtask = state["subtasks"][idx]
        results = []
        for q in subtask["search_queries"]:
            try:
                search_result = self.tavily.search(q, max_results=3)
                # Tavily returns a list of dicts with 'title', 'url', 'content'
                for item in search_result:
                    results.append({
                        "query": q,
                        "title": item.get("title"),
                        "url": item.get("url"),
                        "content": item.get("content")
                    })
            except Exception as e:
                results.append({"query": q, "error": str(e)})
        state.setdefault("search_results", []).extend(results)
        state["messages"] = state.get("messages", []) + [f"Searched for subtask {idx}."]
        state["current_subtask"] = idx + 1
        return state

    def should_continue_searching(self, state: ResearchState) -> Literal["continue", "analyze"]:
        # Continue searching if there are more subtasks
        if state.get("current_subtask", 0) < len(state.get("subtasks", [])):
            return "continue"
        return "analyze"

    def analysis_agent_node(self, state: ResearchState) -> ResearchState:
        analyses = []
        for r in state.get("search_results", []):
            prompt = (
                f"Analyze the following search result for the research question '{state['question']}':\n"
                f"Title: {r.get('title')}\n"
                f"URL: {r.get('url')}\n"
                f"Content: {r.get('content')}\n"
                f"Provide a summary and note if this is a credible source."
            )
            response = self.analysis_llm.invoke([HumanMessage(content=prompt)])
            analyses.append({
                "query": r.get("query"),
                "title": r.get("title"),
                "url": r.get("url"),
                "summary": response.content
            })
        state["analysis_results"] = analyses
        state["messages"] = state.get("messages", []) + ["Analysis complete."]
        return state

    def synthesis_agent_node(self, state: ResearchState) -> ResearchState:
        analyses = state.get("analysis_results", [])
        analyses_str = "\n".join(
            f"Query: {a.get('query')}\nTitle: {a.get('title')}\nURL: {a.get('url')}\nSummary: {a.get('summary')}\n"
            for a in analyses
        )
        prompt = (
            f"Synthesize the following analyses into a comprehensive report for the question: '{state['question']}'.\n"
            f"For each point, cite the relevant sources by title and URL.\n"
            f"Analyses:\n{analyses_str}"
        )
        response = self.lead_llm.invoke([HumanMessage(content=prompt)])
        state["final_report"] = response.content
        state["messages"] = state.get("messages", []) + ["Synthesis complete."]
        return state

    # --- MAIN RESEARCH METHOD ---

    async def research(self, question: str) -> str:
        # Initialize state
        state = {
            "question": question,
            "research_plan": {},
            "subtasks": [],
            "search_results": [],
            "analysis_results": [],
            "final_report": "",
            "messages": [],
            "current_subtask": 0,
            "max_iterations": 10,
        }
        # Run the workflow graph
        result = await self.graph.ainvoke(state)
        return result["final_report"]

    def shutdown(self):
        self.executor.shutdown(wait=True)

if __name__ == "__main__":
    # Initialize and run research
    agent = DeepResearchAgent()
    question = "What are the labor market effects of transformative AI expected to be?"
    
    print(f"Starting deep research on: {question}")
    print("-" * 80)
    
    report = asyncio.run(agent.research(question))
    
    print("\n" + "="*80)
    print("RESEARCH REPORT")
    print("="*80)
    print(report)
    
    # Clean up resources
    agent.shutdown()