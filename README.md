<p align="center">
    <a href="//bin.mayuri.my.id">
        <img src="https://bin.mayuri.my.id/static/img/mayuribin.png" alt="mayuribin" width="500"/>
    </a>
</p>

# Mayuribin

> Elegant pastebin service written in Python

**Mayuribin** is an elegant, free and open-source pastebin web application written in Python and publicly
hosted at [**bin.mayuri.my.id**](//bin.mayuri.my.id). Paste, save and share the link of your text content using a
sleek and intuitive interface!

## Features

- Syntax highlighting for source codes based on file extension.
- Rest api.
- One-click URL copy.

## mayuri-bin API
[See here](https://api.mayuri.my.id/v1/docs)

## self-hosted API

### Using python requests
#### Get Documents
```python
import requests

key = "37e0c61285"
r = requests.get(f"http://127.0.0.1:5556/api/documents?key={key}")
data = r.json()
```
Response:
```json
{
    "ok": true,
    "result": {
        "key": "37e0c61285",
        "content": "test"
    }
}
```

#### Save Documents
```python
import requests

data = {
    "content": "Test"
}
r = requests.post("http://127.0.0.1:5556/api/documents", data=data)
data = r.json()
```
Response:
```json
{
    "ok": true,
    "result": {
        "key": "37e0c61285",
        "title": null,
        "author": null,
        "date": 1725881641.6893768,
        "views": 0,
        "length": 4,
        "content": "test"
    }
}
```
