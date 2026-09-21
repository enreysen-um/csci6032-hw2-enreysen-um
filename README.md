Course: CSCI 6032

Homework: Homework 2

Repository url: https://github.com/enreysen-um/csci6032-hw2-enreysen-um

Host OS: Windows 11

Description:
The goal of this homework is to teach students how to use AI agents safely. It includes using GitHub Copilot CLI, bounding it to a workspace, using Git checkpoints, creating a Linux container for the agent to run in, and create a reusable skill to submit the homework.

## Text statistics

Run the text statistics script with:

```bash
python src/text_stats.py sample.txt
```

Use `--top N` to include the `N` most frequent words in the JSON output. Words
are compared case-insensitively, and ties are ordered alphabetically:

```bash
python src/text_stats.py sample.txt --top 5
```

The optional result is returned in a `top_words` array:

```json
"top_words": [
  {"word": "the", "count": 12},
  {"word": "text", "count": 8}
]
```
