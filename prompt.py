#!/usr/bin/env python3

import sys
import openai
import os
openai.api_key = os.environ.get('OPENAI_API_KEY') 

role_content = "You are a ClickHouse expert specializing in OLAP databases, SQL format, and functions. You can produce SQL queries using knowledge of ClickHouse's architecture, data modeling, performance optimization, query execution, and advanced analytical functions."

def create_openapi_completion(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": role_content},
                {"role": "assistant", "content": prompt}
            ]
        )
    code = response.choices[0].message.content
    result = '```sql\n' + code + '\n```'
    print(result)


def build_query_prompt(schema_details,query):

    input_str=f"""
    {schema_details}

    You are a ClickHouse expert specializing in OLAP databases, SQL format, and functions. You can produce SQL queries using knowledge of ClickHouse's architecture, data modeling, performance optimization, query execution, and advanced analytical functions.
    I would like you to generate an accurate ClickHouse sql query for the question: 
    {query}

    - Make sure the query is ClickHouse compatible
    - Make sure ClickHouse SQL and ClickHouse functions are used
    - Assume there are no tables in memory, data is always remote
    - Load data from files using the file() ClickHouse function, for instance: file('data.csv')
    - Load data from urls containing http using the url() ClickHouse function, for instance url('http://domain.com/file.csv')
    - Make sure any file hosted on s3 is loaded using the s3() ClickHouse function
    - Ensure case sensistivity
    - Ensure NULL check
    - Do not add any special information or comment, just return the query

    The expected output is code only. Always use table name in column reference to avoid ambiguity.
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
