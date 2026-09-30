# NLP to SQL Query Converter

**Ask a database a question in plain English and get the SQL and the answer back.**

Writing SQL is a barrier for anyone who doesn't know the schema or the syntax. I built this so a user can type a question like "show all orders from last month" and have it turned into a structured SQL query and run against a relational database.

<!-- Add a screenshot or GIF here: docs/demo.png -->

---

## What it does

- Takes a natural-language question as input
- Parses it and maps it to database operations
- Generates the SQL query and runs it against a relational database
- Shows the result in a simple interface

<!-- TODO: confirm each line above against how app.py really works -->

**Built with:** Python, SQL, MySQL <!-- TODO: add the libraries from requirements.txt, and the NLP approach (rule-based, LLM, or both) -->

## How it works

<!-- TODO: 3 to 5 sentences. What happens between the user typing a question and the result appearing? What does ingest.py do? Why is there a mysql_ingest.py as well? -->

## Example

<!-- TODO: one real example -->

```
Question: <a real question you tested>
Generated SQL: <the SQL it produced>
```

## Run it locally

You'll need Python 3.10+ and a MySQL database. <!-- TODO: confirm versions -->

```bash
git clone https://github.com/PrajyotKorde-18/NLP-to-SQL-Query-Converter.git
cd NLP-to-SQL-Query-Converter
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your values. <!-- TODO: list the variables it contains -->

```bash
python app.py        # or run.bat on Windows
```

## Project layout

```
NLP-to-SQL-Query-Converter/
├── app.py             # Main application
├── ingest.py          # TODO: what it does
├── mysql_ingest.py    # TODO: what it does
├── Text to SQL/       # TODO: what it holds
├── docs/
├── requirements.txt
├── .env.example
└── run.bat
```

<!--## What I learned-->

<!-- TODO: 2 or 3 honest points, e.g. where the parsing broke on odd phrasing, how you handled ambiguous questions -->

## Author

**Prajyot Korde**, IT undergrad at Ramdeobaba University
[LinkedIn](https://www.linkedin.com/in/prajyot-korde-912621281) · [GitHub](https://github.com/PrajyotKorde-18)
