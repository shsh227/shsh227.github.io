title_tag = article.find("h3", class_="entry-title")
        if title_tag:
            title = title_tag.find("a").text.strip()
            print(f"Title: {title}")
        else:
            title = None

        link_tag = article.find("h3", class_="entry-title").find("a")
        if link_tag and link_tag["href"]:
            url = link_tag["href"]
            print(f"URL: {url}")
        else:
            url = None

        img_tag = article.find("div", class_="entry-thumb")
        if img_tag:
            img = img_tag.find("img")["src"]
            print(f"Image: {img}")
        else:
            img = None

        