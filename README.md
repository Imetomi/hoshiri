**Project Specification: Hoshiri Terminal Applet**

## Overview
Hoshiri is a highly flexible terminal-based Python applet that dynamically expands its capabilities by generating and executing scripts based on user input. It is designed to analyze commands, determine necessary actions, and either execute them directly or generate new scripts/modules to handle the task. Additionally, it integrates Anthropic AI to process natural language queries and respond in plain language.

---

## Core Functionalities
### 1. **Dynamic Script Generation & Execution**
   - Analyzes user input to determine necessary tasks.
   - Generates Python scripts/modules to fulfill requests.
   - Executes scripts and integrates their results into responses.
   - Stores generated scripts for reuse and modification.

### 2. **Self-Tracking Capabilities**
   - Maintains a registry of available modules and their functionalities.
   - Stores metadata regarding past executions.
   - Uses a file-based system, lightweight database, or structured storage to track scripts and capabilities.

### 3. **Natural Language Processing with Anthropic AI**
   - Processes user input and interprets intent.
   - Provides natural language responses while executing tasks in the background.
   - Leverages AI for complex queries and decision-making.

### 4. **Task Automation & API Integration**
   - Supports multiple API integrations (e.g., Gmail, Google Calendar, project management tools).
   - Handles multi-step operations (e.g., fetching emails, processing text, extracting key information).
   - Allows execution of scheduled or recurring tasks.

### 5. **Command Processing & Modular Expansion**
   - Allows users to enter a variety of commands, ranging from simple questions to complex automation requests.
   - Dynamically loads and extends functionalities by writing new modules as needed.
   - If a command cannot be properly executed, Hoshiri will highlight the error and provide a plain-language explanation of what went wrong.
   - During request processing, a "Thinking..." loading animation will be displayed in the terminal to indicate activity.


---

## Technical Architecture
### **Programming Language:** Python

### **Storage & Self-Tracking Mechanism:**
   - SQLite database or JSON-based registry to maintain script metadata.
   - Versioned script storage to keep track of modifications.

### **AI Integration:**
   - Uses Anthropic AI for natural language processing.
   - AI determines execution logic based on command intent.
   - The module uses a chat flow with Claude Sonnet 3.5 and it should remember my previous discussions like what did I request previously

### **Execution Flow:**
1. User inputs a command.
2. AI interprets and determines the required actions. Checks if it just a simple chat action or requires a script to solve. 
3. Checks existing module registry. 
4. If a script exists, it is executed.
5. If no script exists, a new one is generated, stored, and executed.
6. Results are sent once again to the API and are dispalyed after they are processed and anlayzed by Claude. The AI can decide to show the raw format or draw conclusions based upon the user request. 
7. If an error occurs, Hoshiri highlights the issue and provides a clear explanation.
8. A "Thinking..." loading animation appears in the terminal during processing.


### **Security Considerations:**
   - OAuth2 for API authentication (e.g., Gmail, Calendar).
   - Execution sandboxing to prevent malicious script execution.
   - Logging and monitoring of automated actions.

---

## Use Case Examples

### **Email Processing**
**Command:** _"Open my emails and check new emails regarding fundraising."_
   - Generates a script to:
     1. Authenticate with Gmail API.
     2. Retrieve unread emails.
     3. Parse subjects and body text for fundraising-related keywords.
     4. Summarize and display relevant emails.

### **Meeting Scheduling**
**Command:** _"List my meetings for next week."_
   - Generates a module to:
     1. Connect to Google Calendar API.
     2. Fetch events for the upcoming week.
     3. Format and display a structured list of meetings.

### **Task Management Integration**
**Command:** _"List my pending tasks from Trello."_
   - Generates a script to:
     1. Authenticate with Trello API.
     2. Retrieve tasks from assigned boards.
     3. Display pending tasks with due dates and priorities.

### **News Aggregation**
**Command:** _"Summarize the latest tech news."_
   - Generates a script to:
     1. Fetch news articles from RSS feeds or APIs (e.g., Google News, NYT).
     2. Summarize key points using NLP.
     3. Display a concise list of headlines with links.

### **Expense Tracking**
**Command:** _"Add an expense for lunch, $15."_
   - Writes a new script that:
     1. Stores expense records in a database or file.
     2. Supports CLI-based entry of expense items.
     3. Generates summaries on demand.

### **System Resource Monitoring**
**Command:** _"Check my system performance."_
   - Generates a module to:
     1. Retrieve CPU, memory, and disk usage statistics.
     2. Display formatted system health information.
     3. Suggest optimizations if resource usage is high.

### **File Management**
**Command:** _"Find and list all PDFs in my Documents folder."_
   - Generates a script to:
     1. Search for PDF files in the specified directory.
     2. List them with file sizes and modification dates.
     3. Offer options to open, move, or delete files.

### **Weather Updates**
**Command:** _"What’s the weather like today?"_
   - AI responds conversationally while running an external API call in the background to fetch real-time weather data.

### **Music Control**
**Command:** _"Play my favorite playlist on Spotify."_
   - Generates a script to:
     1. Authenticate with Spotify API.
     2. Fetch user’s favorite playlist.
     3. Start playback on the connected device.

### **Expanding Its Own Functionality**
**Command:** _"Create a module to track my daily expenses."_
   - Writes a new script that:
     1. Stores expense records in a database or file.
     2. Supports CLI-based entry of expense items.
     3. Generates summaries on demand.

---

## Future Enhancements
- Web-based dashboard for script management.
- Voice command integration.
- More advanced AI-driven decision-making capabilities.
- Plugin support for third-party services.

---

## Conclusion
Hoshiri is a flexible, intelligent terminal applet designed for natural language task execution and self-expansion. By leveraging dynamic script generation and AI-based processing, it enables automation, conversational responses, and continuous improvement of its capabilities.

