import asyncio
from openai import AsyncOpenAI
import requests
import json
import os

# Configure the OpenAI client with your API key
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Conversation:
    messages = None

    def __init__(self):
        Conversation.messages = [
            {
                "role": "system",
                "content": (
                    "You are a ClickHouse expert specializing in OLAP databases, SQL format, and functions. You can produce SQL queries using knowledge of ClickHouse's architecture, data modeling, performance optimization, query execution, and advanced analytical functions."
                ),
            }
        ]

    async def answer(self, user_prompt):
        prompt = self.build_query_prompt(user_prompt)
        self._update("user", prompt)

        chat_completion = await client.chat.completions.create(
            messages=Conversation.messages,
            model="gpt-3.5-turbo",
        )

        response_content = chat_completion.choices[0].message.content
        self._update("assistant", response_content)

        return response_content

    def _update(self, role, content):
        new_message = {"role": role, "content": content}
        new_message_length = len(json.dumps(new_message))  # Estimate the token length

        while len(Conversation.messages) > 0 and new_message_length + len(json.dumps(Conversation.messages)) > 4096:
            Conversation.messages.pop(0)  # Remove the oldest message

        Conversation.messages.append(new_message)

    def build_query_prompt(self, query):
        input_str = f"""
        I want you to act as a ClickHouse expert specializing in OLAP databases, SQL format, and functions. You can produce SQL queries using knowledge of ClickHouse's architecture, data modeling, performance optimization, query execution, and advanced analytical functions.
        I want you to generate an accurate ClickHouse SQL query for the question:
        {query}

        - Make sure the query is ClickHouse compatible
        - Make sure ClickHouse SQL and ClickHouse functions are used
        - Make sure the simplest ClickHouse SQL query is used and avoid complexity.
        - Assume there are no tables in memory, data is always remote
        - Load data from URLs containing http or https URLs using the url() ClickHouse function, for instance url('https://domain.com/file.csv')
        - Load data from files using the file() ClickHouse function, for instance: file('data.csv')
        - Make sure any file hosted on s3 is loaded using the s3() ClickHouse function
        - Ensure case sensitivity
        - Ensure NULL check
        - When LIMIT is 1 or lower than 10 always select *.
        - Do not write explanations. Just return the SQL query in a single code block.

        The expected output is code only. Always use table name in column reference to avoid ambiguity.
        """
        return input_str

async def execute_sql_query(query: str):
    """Execute SQL query and return results."""
    base_url = "https://chdb.fly.dev/"
    params = {"query": query, "default_format": "JSONCompact"}
    response = requests.get(base_url, params=params)

    # print("Debug Query:\n",query)

    try:
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            return 'Query execution failed with status code {}: {}'.format(response.status_code, data)
    except json.JSONDecodeError:
        return response.text

async def generate_contextual_response(user_query, query_results):
    prompt = f"Based on the following data: {query_results}, how would you summarize the answer to this query: '{user_query}'?"

    # print("Debug Results:\n",query_results)

    chat_completion = await client.chat.completions.create(
        messages=[{"role": "system", "content": prompt}],
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content

async def main():
    conversation = Conversation()

    print("\nHi, I'm chdbGPT, an AI assistant that can execute ClickHouse SQL queries for you.")

    while True:
        user_input = input("\nWhat would you like to know? => ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting SQLGPT. Goodbye!")
            break

        sql_query = await conversation.answer(user_input)
        query_results = await execute_sql_query(sql_query)
        contextual_response = await generate_contextual_response(user_input, query_results)

        print(contextual_response)
        break

asyncio.run(main())
