# Lecture 03 Answers

## Exercises

### 1. Differences between the Lecture 01 (bare LLM) and agent answers

- In Lecture 01, the bare LLM generated answers directly using its pretrained knowledge and the context provided in the prompt. It did not independently retrieve information from external tools.
- In Lecture 03, the AI agent follows a tool-based approach. It understands the user's question, selects an appropriate tool, executes it, processes the returned information and generates a final answer.
- For example, when asked about LoRA, the agent calls `search_glossary` to retrieve the definition and related information from the course glossary.
- Similarly, when asked about Lecture 03, the agent calls `get_lecture_summary` to retrieve the relevant lecture content.
- Therefore, the main difference is that the agent can retrieve course-specific information using tools instead of relying only on the LLM's pretrained knowledge.

### 2. Tool calls shown by `--trace` (tool names and arguments)

The `--trace` experiments showed the following tool calls:

**Experiment 1: Question – "What is LoRA?"**

- Tool called: `search_glossary`
- Argument: `query="LoRA"`
- Returned information: Definition of LoRA, the lecture in which it was covered and related terms.

**Experiment 2: Question – "What do we learn in Lecture 3?"**

- Tool called: `get_lecture_summary`
- Argument: `lecture=3`
- Returned information: Lecture 03 summary, including its aims, key concepts and exercises.

The traces demonstrate how the agent selects the appropriate tool and passes the required arguments depending on the user's question.

### 3. Number of LLM calls for one question (`requests`)

The usage information obtained from both experiments was:

| Experiment | LLM requests | Tool calls |
|---|---:|---:|
| What is LoRA? | 2 | 1 |
| What do we learn in Lecture 3? | 2 | 1 |

For both experiments, the agent made two LLM requests and one tool call.

The first LLM request was used to determine the appropriate tool and its arguments. After the tool returned the requested information, the second LLM request generated the final response.

This demonstrates that the number of LLM requests and the number of tool calls are different. A single tool call can be part of a process involving multiple LLM requests.

### 4. Tool added and the description in its docstring

The additional tool implemented for Lecture 03 is `get_lecture_summary`.

Function signature:

`def get_lecture_summary(lecture: int) -> str:`

Its docstring is:

> Return key points from the specified session (an integer starting at 1).
>
> Use when asked about session content or relationships, such as "What will we learn in Lecture 03?".

The tool retrieves the corresponding lecture Markdown file from the data directory and returns its contents.

The docstring explains the purpose of the tool, its expected argument and the situations in which the model should use it.

This tool allows the agent to answer lecture-specific questions using the actual course material rather than relying only on its pretrained knowledge.



## Homework

### Level: Advanced (a) – Rebuilding the Agent using Google ADK

### 1. Objective

The objective was to rebuild the existing glossary learning assistant using Google's Agent Development Kit (ADK), while keeping the original instructions and tools unchanged.

The experiment aimed to understand how different agent frameworks implement and execute the same AI agent.

### 2. Implementation

I used the existing Pydantic AI implementation as the baseline and created a separate implementation using Google ADK.

The following components were reused without modification:

- INSTRUCTIONS from app/agent.py
- search_glossary from app/tools.py
- get_lecture_summary from app/tools.py

I created:

- adk_agent/glossary_agent/agent.py
- adk_agent/glossary_agent/__init__.py

The ADK agent used the same Gemini model, instructions and tools as the original implementation.

### 3. Experimental Results

I tested both implementations using identical questions.

**Test 1: Glossary Search**

Question: LoRAとは何ですか？

Pydantic AI:
- Successfully returned an explanation of LoRA.
- The answer explained parameter-efficient fine-tuning.

Google ADK:
- Successfully called search_glossary(query="LoRA").
- Returned the LoRA definition and related glossary entries, including Rank and QLoRA.
- Identified Lecture 02 as the relevant lecture.

**Test 2: Lecture Summary**

Question: 第3回では何を学びますか？

Pydantic AI:
- Successfully called get_lecture_summary with lecture=3.
- Retrieved the Lecture 03 AI Agents summary.

Google ADK:
- Successfully called get_lecture_summary with lecture=3.
- Retrieved the Lecture 03 AI Agents summary.
- Presented the main topics in a numbered format.

### 4. Framework Comparison

**Pydantic AI**
- Creates the agent using Agent().
- Registers tools separately using tool_plain().
- Provides an explicit --trace option to inspect tool calls, arguments and returned results.

**Google ADK**
- Creates the agent using Agent().
- Registers tools directly through the tools parameter.
- Uses root_agent as the entry point for agent discovery.
- Provides an event-based execution mechanism.
- Tool calls and responses were verified by inspecting the ADK SQLite session database.

### 5. Observations

1. Both frameworks successfully executed the same agent using the same model, instructions and tool implementations.

2. Google ADK selected search_glossary for the LoRA question and passed the correct query argument.

3. For the lecture-specific question, Google ADK selected get_lecture_summary and passed lecture=3.

4. The ADK glossary search returned related terms along with the requested definition, demonstrating that the tool's returned information can influence the final answer.

5. Both frameworks produced useful answers, although their answer formatting and level of detail differed.

6. The two frameworks provide different approaches to tool registration, agent execution and observability.

7. This experiment demonstrated that the harness is an important component of an AI agent, in addition to the underlying language model.

### 6. Conclusion

Rebuilding the glossary learning assistant using Google ADK helped me understand how different frameworks implement the agent harness.

Although the underlying model, instructions and tools remained unchanged, the agent construction and execution mechanisms differed between Pydantic AI and Google ADK.

The experiment demonstrated that the framework is responsible for orchestrating model interactions, tool execution and the handling of tool results.

### 7. Questions

- How do different agent frameworks handle tool execution, retries and conversation state internally?
- Does changing the harness affect tool-selection reliability?
- How do different frameworks handle parallel tool execution and human approval?
