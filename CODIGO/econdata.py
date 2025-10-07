"""
econdata.py: An AI Agent using FRED - Educational Example
=========================================================
Demonstrates the core concepts of an AI agent that can:
1. Understand a question (Think)
2. Fetch economic data (Act) 
3. Analyze results (Observe)
4. Generate an answer (Respond)

Setup:
1. pip install openai fredapi python-dotenv colorama
2. Get API keys from:
   - FRED: https://fred.stlouisfed.org/docs/api/api_key.html
   - OpenAI: https://platform.openai.com/api-keys
3. Create .env file with your keys in the following format:

"""

import os, json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fredapi import Fred
from openai import OpenAI
from colorama import init, Fore, Style

load_dotenv()
init()

class FREDAgent: # Define agent class
    
    def __init__(self): # Runs when new agent instance created
        self.fred = Fred(api_key=os.getenv('FRED_API_KEY'))
        self.llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def think(self, question): # Plan what data to fetch
        prompt = f"""What FRED series code would help answer this question?
Question: {question}

Common FRED codes: UNRATE (unemployment), FPCPITOTLZGUSA (CPI inflation), GDP, DFF (fed funds rate)

Return JSON: {{"explanation": "why this helps", "series_code": "EXACT_FRED_CODE"}}"""
        
        print(f"\n{Fore.CYAN}=== THINK: LLM Call ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Input:{Style.RESET_ALL}\n{prompt}")
        
        response = self.llm.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        output = response.choices[0].message.content
        print(f"\n{Fore.YELLOW}Output:{Style.RESET_ALL}\n{output}")
        
        plan = json.loads(output)
        return plan['series_code']
    
    def act(self, series_code): # Fetch requested data from FRED
        print(f"\n{Fore.GREEN}=== ACT: FRED API Call ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Fetching:{Style.RESET_ALL} {series_code}")
        
        # Get series metadata for units
        info = self.fred.get_series_info(series_code)
        units = info['units']
        
        # Get last 2 years of data
        end = datetime.now()
        start = end - timedelta(days=730)
        
        print(f"{Fore.YELLOW}Period:{Style.RESET_ALL} {start.date()} to {end.date()}")
        
        data = self.fred.get_series(series_code, start, end)
        print(f"{Fore.YELLOW}Result:{Style.RESET_ALL} {len(data)} data points")
        print(f"Latest: {data.iloc[-1]:.2f} {units} ({data.index[-1].date()})")
        
        return data, units
    
    def observe(self, data, units): # Analyze fetched data
        observations = {
            "current_value": float(data.iloc[-1]),
            "current_date": data.index[-1].strftime("%Y-%m-%d"),
            "units": units
        }
        
        print(f"\n{Fore.MAGENTA}=== OBSERVE: Data Analysis ==={Style.RESET_ALL}")
        print(json.dumps(observations, indent=2))
        
        return observations
    
    def respond(self, question, observations): # Generate natural language response
        prompt = f"""Answer this question using the data:
Question: {question}
Data: {json.dumps(observations, indent=2)}

Provide a brief, clear answer citing specific numbers."""
        
        print(f"\n{Fore.CYAN}=== RESPOND: LLM Call ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Input:{Style.RESET_ALL}\n{prompt}")
        
        response = self.llm.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}]
        )
        
        output = response.choices[0].message.content
        print(f"\n{Fore.YELLOW}Output:{Style.RESET_ALL}\n{output}")
        
        return output
    
    def answer(self, question): # Define orchestrator agent
        # Think -> Act -> Observe -> Respond
        print(f"\n{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Question: {question}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
        
        try:
            series_code = self.think(question) # Think: What data?
            data, units = self.act(series_code) # Act: Fetch data
            observations = self.observe(data, units) # Observe: Analyze data
            response = self.respond(question, observations) # Respond: Generate an answer
            
            print(f"\n{Fore.GREEN}=== FINAL ANSWER ==={Style.RESET_ALL}")
            print(response)
            
            return response
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"\n{Fore.RED}{error_msg}{Style.RESET_ALL}")
            return error_msg

# Example usage
if __name__ == "__main__": # Execute agent with example and interactive prompt
    agent = FREDAgent()
    
    # Example query
    agent.answer()
    
    # Interactive mode
    print(f"\n{Fore.CYAN}Interactive mode{Style.RESET_ALL}")
    question = input(f"\n{Fore.YELLOW}Ask an economic question: {Style.RESET_ALL}")
    agent.answer(question)




a = """What are the latest data fior these variables in Argentina?
- Indicador de actividad (preferiblemente algo análogo al EMAE, sino producción industrial).
- Términos de intercambio de commodities.
- Tipo de cambio nominal.
- Tasa de interés de préstamos del sector bancario local.
- IPC.
- Tasa de política monetaria o interbancaria.
- EMBI (emerging)
                 """