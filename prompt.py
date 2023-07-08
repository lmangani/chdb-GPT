import sys
import openai
import os
openai.api_key = os.environ.get('OPENAI_API_KEY') 

def create_openapi_completion(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "I would like you to be my database specialist and generate an accurate ClickHouse sql query for the question"},
                {"role": "assistant", "content": prompt}
            ]
        )
    code = response.choices[0].message.content
    result = '```sql\n' + code + '\n```'
    print(result)


def build_query_prompt(schema_details,query):

    input_str=f"""
    {schema_details}

    I would like you to be my database specialist and generate an accurate ClickHouse sql query for the question
    {query}

    - Make sure the query is ClickHouse compatiable
    - Make sure ClickHouse SQL and ClickHouse functions are used
    - Assume there are no tables in memory, data is always remote
    - Load data from files using the file() function, for instance: file('data.csv')
    - Ensure case sensistivity
    - Ensure NULL check
    - Do not add any special information or comment, just return the query

    The expected output is code only. Always use table name in column reference to avoid ambiguity
    """

    return input_str


if len(sys.argv) > 1:
    query = sys.argv[1]
else:
    query = input("Describe your desired query: ")

with open('constant.txt') as f:
    example_schema = f.readlines()

full_prompt = build_query_prompt(example_schema, query=query)
create_openapi_completion(full_prompt)
