<img src="https://github.com/chdb-io/chdb/raw/pybind/docs/_static/snake-chdb.png" width=320 >

# chdb-GPT
Generate chDB and ClickHouse queries using natural language with ChatGPT/OpenAI APIs

### Status
* Just a toy, hallucinating
* Needs more ClickHouse arguments
* Needs more Schema and Function Examples
* Do not use this!

### Usage
```
python3 promtp.py "count rows from file data.csv"
```
```sql
SELECT count(*) FROM file('data.json')
```
