import json


def parse_articles(file_name, parse_file_name):
    with open(file_name, 'r') as file:
        messages = json.load(file)

    parsed_articles = []

    for msg in messages:
        lines = [line.strip()
                 for line in msg['message'].split('\n') if line.strip()]
        article_index = 0

        for i in range(1, len(lines), 2):
            title = lines[i]
            body = lines[i + 1] if i + 1 < len(lines) else ""

            article = {
                "id": msg['id'],
                "date": msg['date'],
                "title": title,
                "body": body,
                "url": msg['urls'][article_index] if article_index < len(msg['urls']) else None,
                "media": msg['media']
            }

            parsed_articles.append(article)
            article_index += 1

    with open(parse_file_name, 'w') as file:
        json.dump(parsed_articles, file, indent=2)
    print("Articles parsed and saved to parsed_articles.json")
