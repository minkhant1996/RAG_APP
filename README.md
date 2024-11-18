# RAG_APP

## Table of Contents
- [To Do Next](#to-do-next)
- [How to Run This App](#how-to-run-this-app)
    - [Prerequisites](#prerequisites)
    - [Cloning and Setup](#cloning-and-setup)
- [User Guide](#user-guide)
    - [How This App Works](#how-this-app-works)
    - [How to Get Chat History](#how-to-get-chat-history)
    - [How to Clear Chat History](#how-to-clear-chat-history)
    - [How to Use LangChain QA Eval](#how-to-use-langchain-qa-eval)


## To Do Next
- Improve evaluation on doc extraction
- PDF Extraction Speed
- Experiments more on Chunking
- Multi PDF upload
- Add threading to work with workers to process all pdf at the same time
- Add New Doc to FAISS (Current Version: It will replace if new pdf is uploaded)
- Add Logs
- Add more content type

## How to run this app

### Prerequisites
- **Docker**: Ensure Docker is installed on your system. Refer to [Docker's official installation guide](https://docs.docker.com/get-docker/).

### Cloning and Setup

#### **1. Clone the Repository**
Clone the repository to your local machine:
```bash
git clone https://github.com/minkhant1996/RAG_APP.git
```

#### **2. Navigate to the Project Directory**
Move into the cloned directory:
```bash
cd RAG_APP
```

#### **3. Configure the Application**
Create an `.env` file for application configuration. Use `.env.example` as a reference to populate the required fields and values.

#### **4. Run the docker**
Check the instruction below.

---

### **Running the Application with Docker**

#### **Build the Application**
To build the application in the development environment:
```bash
bash run_docker.sh build dev
```

#### **Run the Application**
To start the application:
```bash
bash run_docker.sh up dev
```

#### **Stop the Application**
To stop the running application:
```bash
bash run_docker.sh down dev
```

#### **Restart the Application**
To restart the application:
```bash
bash run_docker.sh restart dev
```

## User Guide

### How this app works

#### Upload pdf with your userID (string): UserID can be anyting in text, just use it to call chat history

Example API call

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/upload_pdf' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'userId=u123456' \
  -F 'file=example.pdf;type=application/pdf'
```

Example Response

```bash
{
  "message": "File uploaded successfully"
}
```

#### Then you can start chatting with your pdf

Example API call

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/chatbot' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "userId": "u123456",
  "user_query": "ok, what did I just asked?"
}'
```

Example Response

```bash
{
  "response": "You just asked me to summarize a paper, and I provided a summary of the paper titled \"How to Prompt LLMs for Text-to-SQL: A Study in Zero-shot, Single-domain, and Cross-domain Settings.\" If you have any further questions or need more information about that paper or another topic, feel free to ask!"
}
```

## How to get chat history

Example API call

```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/retrieve_conversation?userId=u123456' \
  -H 'accept: application/json'
```

Example Response

```bash
{
  "chat_history": [
    {
      "query": "summarize me this paper",
      "response": "The paper titled \"How to Prompt LLMs for Text-to-SQL: A Study in Zero-shot, Single-domain, and Cross-domain Settings\" investigates effective prompt construction strategies for large language models (LLMs) in the text-to-SQL task. It explores various settings including zero-shot, single-domain, and cross-domain scenarios.\n\nKey findings include:\n1. **Importance of Database Knowledge**: The study emphasizes the critical role of table relationships and content in prompting LLMs effectively. The representation of this information in prompts is crucial, especially in zero-shot and cross-domain settings.\n\n2. **In-domain Demonstrations**: Utilizing in-domain examples can reduce LLM sensitivity to different representations of database knowledge, but cannot replace the need for actual table content knowledge.\n\n3. **Prompt Length**: The paper identifies that prompt length significantly affects performance, revealing a \"sweet spot\" for optimal prompt length that enhances accuracy.\n\n4. **Comparative Analysis**: The authors conduct a thorough comparison of different prompt constructions across various text-to-SQL settings, providing insights that can guide future research in the area.\n\nOverall, the findings suggest that careful consideration of prompt design is essential for improving LLM performance in converting natural language questions into SQL queries, and these insights can inform future text-to-SQL studies.",
      "timestamp": {
        "query": "2024-11-18 17:19:21",
        "response": "2024-11-18 17:19:30"
      }
    },
    {
      "query": "ok, what did I just asked?",
      "response": "You just asked me to summarize a paper, and I provided a summary of the paper titled \"How to Prompt LLMs for Text-to-SQL: A Study in Zero-shot, Single-domain, and Cross-domain Settings.\" If you have any further questions or need more information about that paper or another topic, feel free to ask!",
      "timestamp": {
        "query": "2024-11-18 17:19:45",
        "response": "2024-11-18 17:19:50"
      }
    }
  ]
}
```

## How to clear chat history

Example API call

```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/clear_conversation?userId=u123456' \
  -H 'accept: application/json'
```

Example Response:
```bash
{
  "message": "Conversation cleared successfully."
}
```

## How to use lanchain QA eval

Example API call

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/run_langchain_eval_qa' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "userId": "u123456",
    "question": [
      "What is the primary focus of this research paper?",
      "What are the key components of a text-to-SQL prompt as discussed in the paper?",
      "How does normalized prompt construction impact LLM performance in text-to-SQL tasks?",
      "What role do in-domain demonstration examples play in text-to-SQL tasks?",
      "What database knowledge is crucial for effectively prompting LLMs?"

    ],
    "ref_answer": [
      "The paper focuses on investigating and comparing different strategies for constructing prompts for large language models (LLMs) in text-to-SQL tasks across zero-shot, single-domain, and cross-domain settings.",
      "The key components include task instructions, the test database, the test natural language query (NLQ), and optional demonstration examples.",
      "Normalized prompts reduce token counts and improve execution accuracy in most cases for both Codex and ChatGPT.",
      "In-domain demonstrations mitigate LLM sensitivity to different representations of database knowledge and enhance performance, particularly in single-domain settings.",
      "Table relationships and table content are crucial, with specific emphasis on how they are represented in prompts."
    ]
  }'
```

Example Response

```bash
{
  "response": [
    {
      "query": "What is the primary focus of this research paper?",
      "ref_answer": "The paper focuses on investigating and comparing different strategies for constructing prompts for large language models (LLMs) in text-to-SQL tasks across zero-shot, single-domain, and cross-domain settings.",
      "response": "The primary focus of the research paper is to investigate effective prompting strategies for the text-to-SQL task using large language models (LLMs). The authors compare various prompt constructions across three settings: zero-shot, single-domain, and cross-domain text-to-SQL. They aim to provide insights into the impact of different database and demonstration prompt constructions on the performance of LLMs, while emphasizing the importance of table relationships and content in effective prompting. The findings are intended to guide future research in the field of text-to-SQL with LLMs.",
      "grade": "CORRECT"
    },
    {
      "query": "What are the key components of a text-to-SQL prompt as discussed in the paper?",
      "ref_answer": "The key components include task instructions, the test database, the test natural language query (NLQ), and optional demonstration examples.",
      "response": "The key components of a text-to-SQL prompt, as discussed in the paper, include:\n\n1. **Task Instruction**: This specifies the action that the model needs to perform, such as generating a SQL query from a natural language question.\n\n2. **Test Database**: This includes the database schema and content that the model will use to generate the SQL query.\n\n3. **Test Natural Language Question (NLQ)**: This is the question posed in natural language that the model must convert into a SQL query.\n\n4. **Optional Demonstrations**: These are pairs of NLQs and their corresponding SQL queries that provide examples of how to form the SQL query based on the test database. These can be included in zero-shot, single-domain, or cross-domain settings.\n\nThese components work together to enable large language models to effectively perform the text-to-SQL task by providing the necessary context and examples.",
      "grade": "CORRECT"
    },
    {
      "query": "How does normalized prompt construction impact LLM performance in text-to-SQL tasks?",
      "ref_answer": "Normalized prompts reduce token counts and improve execution accuracy in most cases for both Codex and ChatGPT.",
      "response": "Normalized prompt construction significantly impacts the performance of large language models (LLMs) in text-to-SQL tasks. According to the document, using normalized schemas tends to reduce the token count in comparison to unnormalized schemas across various database constructions. This normalization often results in slightly improved performance. Specifically, for Codex, normalized prompts showed improvements across all configurations, while for ChatGPT, normalized prompts either improved accuracy or achieved the same level of accuracy as unnormalized schemas in most cases.\n\nThe normalization process helps standardize the prompt text, which reduces variations among different databases and minimizes overall prompt length. This is crucial because LLMs can be sensitive to how input is structured, and a well-normalized prompt can lead to better understanding and execution of the SQL queries generated from natural language questions.\n\nIn summary, employing normalized prompt construction can enhance LLM performance in text-to-SQL tasks by reducing token count, improving execution accuracy, and providing a more standardized input for the models to process.",
      "grade": "CORRECT"
    },
    {
      "query": "What role do in-domain demonstration examples play in text-to-SQL tasks?",
      "ref_answer": "In-domain demonstrations mitigate LLM sensitivity to different representations of database knowledge and enhance performance, particularly in single-domain settings.",
      "response": "In the context of text-to-SQL tasks, in-domain demonstration examples play a crucial role in enhancing the performance of large language models (LLMs). According to the provided document, when in-domain examples are included in prompts, they lead to a notable improvement in the performance of models like Codex and ChatGPT. Specifically, the presence of these examples helps LLMs better adapt to the database and question format, thereby increasing execution accuracy.\n\nAs the number of in-domain demonstration examples increases, the performance of the models continues to enhance. However, it is also noted that while in-domain demonstrations help mitigate sensitivity to the representation of table content, they cannot replace the need for table content knowledge itself. This suggests that while in-domain examples are beneficial, it remains essential to include relevant table content in the prompts for optimal performance in text-to-SQL tasks.",
      "grade": "CORRECT"
    },
    {
      "query": "What database knowledge is crucial for effectively prompting LLMs?",
      "ref_answer": "Table relationships and table content are crucial, with specific emphasis on how they are represented in prompts.",
      "response": "The crucial database knowledge for effectively prompting large language models (LLMs) includes both table relationships and table content. According to the provided document, incorporating these elements significantly enhances the performance of LLMs in the text-to-SQL task. \n\nSpecifically, table relationships can be represented using foreign keys, which help in understanding how tables are interconnected. Additionally, exposing LLMs to the actual content of the database through various prompt constructions (like showing distinct values from columns) is also important. The representation of this content needs to be carefully chosen, as it can impact the model's understanding and performance. Overall, both table relationships and content play a pivotal role in creating effective prompts for LLMs in the text-to-SQL context.",
      "grade": "CORRECT"
    }
  ]
}
```
