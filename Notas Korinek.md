

---

- LLM Tradicionales

- Modelos de razonamiento

- Agentic chatbots



---



---

## Servicios

ltman has already floated the possibility that he may soon sell access to a Ph.D.-level scientist system at a cost of $20,000 per year (Palazzolo and Weinberg, 2025).
![[Pasted image 20251006031518.png]]

free:
meta llama
 gpt-oss-120B and gpt-oss-20
Mistral AI
Kimi-K2
Qwen
DeepSeek
EXTRA: Minimax


---


---
## LLMS

 "system-1" thinking, which leads to characteristic limitations: they process text in a unidirectional stream without the ability to ponder on and revise earlier output, they lack access to real-time information beyond their training cuto!, and they struggle with tasks requiring multi-step logical reasoning or mathematical derivations. 

Comparacion de LLMs:

https://lmarena.ai/leaderboard


## Reasoning

These models are still next-token predictors but are trained via reinforcement learning to generate tokens that imitate "system-2" thinking in humans—deliberate, step-by-step problem solving that can perform complex and systemic analysis while also identifying and correcting errors. The reinforcement learning teaches the models to follow techniques such as producing chains of thought and tree search to solve complex analytic problems step-ty-step.


little advantage over traditional LLMs for tasks primarily requiring language fluency or creative generation. F
![[Pasted image 20251006030951.png]]

## Agentic

utonomously take actions and call on external tools to accomplish the goals specified by the use
los previos -> les das una instruccion y tienen que generar una respuesta "con lo que ya tienen" con las weights, etc. la funcionalidad extra:
 web searches, interact with databases, execute code, manipulate files, and even control computer interfaces to accomplish complex tasks
 es "agentic" porque deja a la ia "tomar la decision" de usar una herramienta a la que tiene acceso. 
 AI system that can conduct end-to-end analyses: downloading datasets, cleaning and processing data, running econometric analyses, creating visualizations, and synthesizing results into coherent narratives. (tps de macrometrics)

sk agentic chatbots for their sources in data analysis tasks and verify it. I 


### EXTRA: Reinforcement Learning. ¿Qué es un agente?

Sutton & Barto: https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf 

![[Pasted image 20251006034426.png]]
Figure : Finite markov decision processes illsutration from Sutton

En computacion los agentes perciben su ambiente mediante "sensores" y actuan sobre el ambiente por "actuators." 
(variables de estado y de salto)
Estos sensores y actuadores son las herramientas que el agente puede llamar (google, tus documentos, ...)
Ya lo sabemos esto!... en economia agentes maximizan una funcion objetivo sujeta a restricciones de información y conocimiento. Los agentes de IA quieren satisfacer un objetivo con un prompt inicial ($x_{0}$) 
operan sujetos a limites de memoria y de tokens (output) y tambien sujeto a las herramientas a las que tiene acceso (eeg: funciones de produccion)
RL busca aproximar el razonamiento que logra el objetivo sujeto a esas restricciones.

¿Alignment?: "In economics, much of the focus of agency theory is on the potential misalignment between principal and agent; for AI agents, the question of alignment is likewise receiving a growing amount of attention (Hendrycks, 2025)"


---

# 3. AI Agents for Economic Research




![[Pasted image 20251006040233.png]]
Figure: an orchestrator passes the original objective (for example a user prompt) and the list of available external tools to a reasoning LLM. This LLM represents the digital equivalent of the system’s brain: it strategizes how to pursue the objective and decides what external tools to call. These tools provide the system with an interface with the external world, giving it the digital equivalent of eyes to see its environment and hands to perform actions. Common examples of such tools are search engines, web browsers, code execution, database queries, or LLM subagents, all of which we will explore below. Each time the reasoning engine wants to call a tool, it generates tokens that indicate to the orchestrator to call upon the designated external tool and feed the result back to the reasoning engine before continuing the token generation process. Moreover, a memory system allows the agent to store context and build upon past results

### Deep research
Creado por google deepmind 2024
![[Pasted image 20251006043212.png]]
Usan arquitecura multi agente para investigacion abierta 
un agente lider es el orchestrator que recibe el query, arma subtasks y cada una la realiza alguno de los 


### Coding Agents
terminal based
– “vibe coding – that is, creating entire software projects based on user prompts in natural language. Vibe coding has made it possible for users with no programming experience to create software projects from beginning to end.

Full vibe coding:
Claude Code, Gemini CLI, Codex + Open codex

Intermedio:
GitHub Copilot, Cursor, and Windsurf + EXTRA: Cline

Manus



---
# 4. Under the Hood: Building AI Agents for Research

---
## Data retrievl agent (first gen)

hat makes this code an "agent" rather than a simple script is its autonomous, goaldirected behavior through multiple steps

Instead, it exhibits the planning and tool-calling capabilities that define AI agents: it first thinks about what data would help answer the question, then acts by calling the appropriate external tool (the FRED API), observes by analyzing the returned data, and finally responds with a natural language answer. This Think-Act-Observe loop characterizes sophisticated agentic systems


## LangGraph Agents
What if the agent needs to fetch multiple data series? What if the initial data suggests a follow-up query would be valuable? What if we want the agent to backtrack when it realizes it’s pursuing an unproductive path?


## Deep Research Agent Using LangGraph


---
# Protocolos
## The Model Context Protocol (MCP): 
(Anthropic, 2024)

or economists, generaluse MCP servers provide AI agents automated access to the user’s file system, email systems (e.g., Gmail or Outlook), local databases, GitHub, or apps like Slack. There are also economics-specific MCPs, for example third-party wrappers that provide access to FRED or IMF data available on the website pulsemcp.com that users can connect to so that their AI agents or chatbots can automatically access the relevant data.

## Agent2Agent Protoco




---
# EXTRA

---

### EXTRA: AI Co-Scientist

**Si todo lo puede hacer la IA ¿para qué servimos los economistas? ¿la investigación va a quedar obsoleta?**

Por ahora, no. 

While AI agents excel at synthesis and implementation, the spark of insight that identifies novel research questions, the intuition connecting disparate phenomena, and the judgment recognizing profound implications remain human contributions. However, there are also efforts underway that seek to automate these creative contributions by using agentic AI systems — see, e.g., Google’s [AI Co-Scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/).




---
### EXTRA: Refine.ink


![[Pasted image 20251006040503.png]]

https://x.com/dunc_webb/status/1972737350586482706/photo/1


![[Pasted image 20251006045658.png]]





----

Lo que vamos a hacer hoy:
- crear una pagina web con Claude Code (Codex / GeminiCLI) 
- crear un agente que conecta con datos fred - uno simple y uno LangGraph y con MCPs
- Prueba de refine.ink


---
