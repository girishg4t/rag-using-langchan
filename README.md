# rag-using-langchan

## This project demonstrate how to store pdf into vector db and query that data based on input, There are 2 api's for this

```bash
curl --location 'http://127.0.0.1:8001'
```

```bash
result:
{
"message": "Welcome to the Vector Database API"
}

```

````bash
curl --location 'http://127.0.0.1:8000/v1/upload' \
--header 'accept: application/json' \
--form 'file=@"/Users/girish/python/github.com/girishg4t/faq_rag/data/sample_faq.pdf"'```
````

```bash
curl --location 'http://127.0.0.1:8001/v1/matches/?sentence=What%20is%20machine%20learning%3F&limit=2' \
--header 'accept: application/json'
```

result:

```
{
    "matches": [
        {
            "sentence": "Machine Learning is a subset of AI that focuses on building systems that can learn from and make decisions based on data without explicit programming."
        },
        {
            "sentence": "2. What is Machine Learning (ML)?"
        }
    ]
}
```
