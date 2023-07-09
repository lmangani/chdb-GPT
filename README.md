<img src="https://github.com/chdb-io/chdb/raw/pybind/docs/_static/snake-chdb.png" width=320 >

# chdb-GPT
Generate chDB and ClickHouse queries using natural language with ChatGPT/OpenAI APIs

### Status
* Just a toy, hallucinating states 🐍
* Needs Prompt fine tuning and hacks
* Do not use this!

### Requirements
* `OPENAI_API_KEY`
```bash
export OPENAI_API_KEY {your_openai_token_here}
```

### Usage
#### Count local files
```bash
python3 promtp.py "count rows from file data.csv"
```
```sql
SELECT count(*) FROM file('data.csv')
```
```
# python3 -m chdb "$(./prompt.py "count rows from file data.csv" | awk -v FS="(sql|\`\`\`)" '{print $1}')" Pretty
┏━━━━━━━━━┓
┃ count() ┃
┡━━━━━━━━━┩
│       2 │
└─────────┘
```

#### URL Engine, Parquet
```bash
python3 promtp.py "show the top 10 towns from url https://datasets-documentation.s3.eu-west-3.amazonaws.com/house_parquet/house_0.parquet" 
```
```sql
SELECT town, COUNT(*) AS count
FROM url('https://datasets-documentation.s3.eu-west-3.amazonaws.com/house_parquet/house_0.parquet', 'Parquet')
GROUP BY town
ORDER BY count DESC
LIMIT 10;
```
