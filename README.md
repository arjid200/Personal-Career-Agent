🚀 Global Career & Networking Agent
 *Your AI-Powered Executive Assistant for Professional Growth*

Built for the  Google Gen AI Academy APAC  , this project is a multi-agent AI system designed to solve the "chaos" of job hunting and professional networking. Instead of just chatting, this agent **acts**—organizing your career pipeline, tracking recruiter contacts, and managing your goals through a unified, intelligent interface.

🌟 What is this?
The **Global Career Agent** is an automated workspace that understands professional intent. Whether you're a student looking for your first internship or a professional managing multiple job offers, this agent helps you:
 **Track Applications:** Save job listings with a single sentence.
 **Manage Networking:** Log recruiters and mentors into a persistent database.
 **Automate Workflows:** Move applications through stages (Interested → Applied → Interviewing).
 **Maintain Context:** Unlike basic chatbots, this system "remembers" your career history using Google Cloud's serverless infrastructure.

 🛠️ The Tech Stack (What we used)
This project leverages the **Google Cloud Ecosystem** to create a scalable, production-ready AI application.

 **The "Brain" (AI & Orchestration)**
 **Gemini 1.5 Flash:** Our core Large Language Model (LLM) for fast, intelligent reasoning.
 **Google ADK (Agent Development Kit):** Used to build a **Multi-Agent Architecture** consisting of a *Root Coordinator* and a *Specialized Career Worker*.
 **FastAPI:** The high-performance Python framework powering our backend API.

 **The "Memory" (Data & Storage)**
* **Google Cloud Datastore (NoSQL):** A highly scalable database used to store job listings and networking contacts. This ensures your data persists across sessions.

 **The "Hands" (Tools & Integration)**
* **Model Context Protocol (MCP):** The secret sauce. We used MCP to create a standardized "bridge" between the AI's logic and our database tools.
* **Uvicorn:** The ASGI server used to host our web application.

 **The "Platform" (Deployment)**
* **Google Cloud Run:** The entire system is containerized and deployed as a serverless microservice, ensuring it is globally accessible via a secure URL.
* **Cloud Build:** Automates the creation of our container images for seamless deployment.

🏗️ Multi-Agent Architecture

The project follows a **Sequential Agent Workflow**:
1.  **Root Agent:** Acts as the "Receptionist." It captures the user's raw input and sets the conversation state.
2.  **Career Specialist Agent:** The "Expert." It holds the permissions to use specific tools (Datastore, Networking Log) to execute the user's request.

🚀 Getting Started

**Prerequisites**
* Python 3.10+
* Google Cloud Project with **Datastore API** enabled.
* A Gemini API Key from **Google AI Studio**.

**Installation**
1.  **Clone the repo:**
    ```bash
    git clone https://github.com/arjid200/Personal-Career-Agent.git 
    cd career-agent
    ```
2.  **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```
3.  **Set up environment variables:**
    Create a `.env` file:
    ```
    MODEL=gemini-1.5-flash
    GOOGLE_CLOUD_PROJECT=your-project-id
    ```

💡 How to Use
Once the agent is live, you can interact with it naturally:
"I found a Software Intern role at Google in Kochi, please save it to my tracker."
"Show me all my current job opportunities."
"I met a recruiter named Sarah from Amazon today. She was very helpful, add her to my network."
"Update my Google application status to 'Interviewing'."

🏆 Hackathon Goals Met
✅ **Multi-Agent Coordination:** Primary agent delegating to a sub-agent.
✅ **Structured Data:** Implementation of Google Cloud Datastore for persistent memory.
✅ **MCP Integration:** Standardized tool logic for database interactions.
✅ **Real-World Workflow:** Solving the specific problem of career management and networking.

Developed by Arjid Biju for the Google Gen AI Academy APAC 2026.
<img width="1913" height="911" alt="hackthon 2" src="https://github.com/user-attachments/assets/8fdc3b22-7a2f-480f-903d-41ed09e2909e" />
<img width="1918" height="912" alt="hackthon 1" src="https://github.com/user-attachments/assets/4db6b337-e337-420b-b235-0ccc8bf58d86" />
