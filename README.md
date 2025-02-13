# Context-Aware Chatting App

## Overview

This is a context-aware chatting application that leverages a local Large Language Model (LLM) to provide project-specific assistance. Instead of manually querying web-based LLMs, this app ensures that responses are tailored to the specific project you are working on by maintaining context on a per-directory basis.

## Features

### 1. Context-Aware Chat

- When the app is invoked from a terminal within a specific project directory, it retrieves stored context related to that project.
- The LLM responds based on the project's programming language and existing discussions.
- Context is maintained on a folder basis to ensure relevant responses.

### 2. Configuration-Based Execution

- The app loads settings from a `config.yaml` file. The file shall be stored in the root project directory.
- The configuration file allows customization of:
  - Number of GPU layers
  - Context size
  - Number of processing threads
  - Path to the LLM model
  - Path to the summary model

### 3. Local Context Storage

- Stores chat history and context in a local SQLite database.
- When a new query is made, previous chat summaries are prepended for better contextual responses.

### 4. Chat Explorer

- Enables users to explore previous conversations and memories stored in the local database.

## How It Works

1. The user invokes the app from a terminal within a project directory.
2. The app checks if there is an existing context for that directory in the SQLite database.
3. If context exists, it prepends the summary of past conversations to the new query.
4. The LLM processes the query and returns a response based on the project-specific context.
5. The chat is logged for future reference.

## Getting Started

### Prerequisites

- A compatible local LLM model (e.g., CodeLlama for coding-related projects).
- Python installed on the system.
- Required dependencies installed (`pip install -r requirements.txt`).

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/kiransilwal1/chat-ai.git
   cd chat-ai
   ```

2. Configure the `config.yaml` file to specify model paths and performance settings.
3. Run the application from a project directory:

   ```sh
   python main.py
   ```

## Recommendations

### For Developers

- Use LLMs specialized in coding languages, such as CodeLlama, for better accuracy.
- Use LLMs that has low parameters and low context size to summarize the previous chat.

### For Content Writers

- Opt for LLMs with larger context sizes for handling extensive documents.
- Use LLMs that has low parameters and low context size to summarize the previous chat. If you want to summarize all the summaries in each summarization you can add all the previous summaries to summarize the app and use LLMs with high context as the summarizer.

## Contribution & License

This is the first version of the app and is publicly available for cloning, modification, and reuse. Contributions are welcome! Feel free to submit pull requests and suggest improvements.

---

Made with ❤️ for developers and content creators!
