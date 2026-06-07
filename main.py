import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from pypdf import PdfReader
import json


load_dotenv(override=True)


extract_text_from_pdf_json = {
    "name": "extract_text_from_pdf",
    "description": "  When user provides file url use this function to extract content from the file.",
    "parameters": {
        "type": "object",
        "properties": {
            "file": {
                "type": "string",
                "description": "The pdf file path or url to extract text from"
            },
            
        },
        "required": ["file"],
        "additionalProperties": False
    }
}


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


tools = [{"type": "function", "function": extract_text_from_pdf_json}]


def handle_tool_call( tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results

def clean_history(history):
    clean_history = []
    if history:
        for message in history:
            texts = [
                item["text"] for item in message.get("content", []) if item.get("type") == "text"
            ]
            if texts:
                clean_history.append({
                    "role": message["role"],
                    "content": "\n".join(texts)
                })
    return clean_history

def chat(message,history):
    print(message)
    print(history)
    history = clean_history(history)
    system_prompt = """You are a helpful assistant.

Behavior Rules:\

1. Always greet the user at the beginning of the conversation.
2. Answer general questions directly using your own knowledge.
3. Do NOT call any tool for general conversation, greetings, explanations, summaries, coding questions, or knowledge-based questions.
4. Only call a tool when the user explicitly provides a file URL and asks for information from that file.
5. If no file URL is present, never call any tool.
6. Do not mention tools, functions, APIs, or internal implementation details.
7. Do not fabricate information about a file. If a file URL cannot be accessed, politely inform the user.
8. Be polite and concise.

Decision Logic:
- File URL present → Use tool.
- No File URL present → Do NOT use any tool."""
    user_query = message["text"]
    uploaded_files = message["files"]
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message['text']}]
    if uploaded_files:
        for file in uploaded_files:
         messages.append({"role":"user" , "content": "user has upload files, you can use the tool to extract contnet . The file url is : " + file}) 
    done = False
    response = None
    while not done:
        openai = OpenAI(base_url='http://localhost:11434/v1',api_key="ollama")
        response = openai.chat.completions.create(model="qwen3:8b",messages=messages,tools=tools)
        print('response for tool calls')
        print(response)
        if response.choices[0].finish_reason == "tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_call(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
             done = True
    return response.choices[0].message.content




def main(message,history):
    api_key = os.getenv("OPENAI_API_KEY")
    response = None
    if not api_key:
        print("No API key found - error in key")
    else:
        user_query = message["text"]
        uploaded_files = message["files"]

        print(message)

        if uploaded_files:
            file_texts = []
            for file in uploaded_files:
                    text = extract_text_from_pdf(file)
                    file_texts.append(text)
            file_texts = "Extracted text from uploaded files: " + " ".join(file_texts)
            if user_query:
                file_texts += " User query: " + user_query
            messages = [{"role": "system", "content": "You are a helpful assistant. Always start with greeting user."}] + history +  [{"role": "user", "content": file_texts}]
            openai = OpenAI(base_url='http://localhost:11434/v1',api_key="ollama")
            response = openai.chat.completions.create(model="llama3.2",messages=messages)
            response = response.choices[0].message.content 
        elif user_query:
            messages = [{"role": "system", "content": "You are a helpful assistant. Always start with greeting user."}] + history +  [{"role": "user", "content": message["text"]}]
            print(messages)
            openai = OpenAI(base_url='http://localhost:11434/v1',api_key="ollama")
            response = openai.chat.completions.create(model="llama3.2",messages=messages)
            response = response.choices[0].message.content 
            #print(history)
        
    return response

demo = gr.ChatInterface(
    fn=chat, 
    multimodal=True,
    title="Multimodal Chat Bot"
)

if __name__ == "__main__":
    demo.launch()

