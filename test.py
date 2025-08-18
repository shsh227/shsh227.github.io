if current_link_tag and time:
            # Now visit the article page
            driver.get(current_link_tag)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "main-wrap")))
            article_html = driver.page_source
            article_content = BeautifulSoup(article_html, "html.parser")
            container = article_content.find("div", class_="site-content cf")
            container_sections = container.find_all("article")

            for container_section in container_sections:
                print("[DEBUG] Article HTML:\n", container_section.prettify()[:500])
                # Title
                content_title_tag = container_section.find("h3", class_="news_post_title")
                content_title = content_title_tag.get_text(strip=True) if content_title_tag else None
                print(f"[DEBUG] Title: {content_title}")

                # Image
                content_img_tag = container_section.find("div", class_="news_post_photo")
                if content_img_tag:
                    style = content_img_tag.get("style", "")
                    img_url_match = re.search(r'url\((.*?)\)', style)
                    content_img = img_url_match.group(1) if img_url_match else None
                    if content_img and content_img.startswith("//"):
                        content_img = "https:" + content_img
                else:
                    content_img = None
                print(f"[DEBUG] Image URL: {content_img}")

                # Summary
                content_summary_tag = container_section.find("p", class_="summary")
                content_summary = content_summary_tag.get_text(strip=True) if content_summary_tag else None
                print(f"[DEBUG] Summary: {content_summary}")




                # === Handle most current article with different structure ===
                current_article_div = content.find("div", class_="story-content")
                if current_article_div:
                    subtitle_link_tag = current_article_div.find("div", class_="entry-subtitle")
                    if subtitle_link_tag:
                        a_tag = subtitle_link_tag.find("a", href=True)
                        if a_tag:
                            current_link_tag = a_tag["href"]
                            print(f"URL from subtitle: {current_link_tag}")
                        else:
                            current_link_tag = None
                    else:
                        current_link_tag = None

                    if not current_link_tag:
                        h2_title = current_article_div.find("h2", class_="entry-title")
                        if h2_title:
                            a_tag = h2_title.find("a", href=True)
                            if a_tag:
                                current_link_tag_correct = a_tag["href"]
                                print(f"URL from title: {current_link_tag_correct}")
                            else:
                                current_link_tag = None

                    # Final fallback: if still no URL found, print a warning
                    if not current_link_tag:
                        print("Warning: No article URL found in this story-content block.")

                    # Date
                    date_tag = current_article_div.find("div", class_="entry-subtitle")
                    if date_tag:
                        raw_time = date_tag.get_text(strip=True)
                        print("[DEBUG] Raw date text:", raw_time)

                        # Try to extract the date part (e.g., "15 AUGUST 2025")
                        match = re.search(r'\d{1,2} \w+ \d{4}', raw_time)
                        if match:
                            try:
                                time = datetime.datetime.strptime(match.group(), "%d %B %Y").date()
                            except ValueError as e:
                                print("[ERROR] Date parsing failed:", e)
                                time = None  # fallback
                        else:
                            print("[WARNING] No date match found in:", raw_time)
                            time = None  # fallback
                    else:
                        print("[WARNING] No date container found")
                        time = None  # fallback

                    if current_link_tag_correct:
                        # Now visit the article page
                        driver.get(current_link_tag_correct)
                        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "main-wrap")))
                        
                        print("[DEBUG] Navigated to:", current_link_tag_correct)
                        print("[DEBUG] Current URL after load:", driver.current_url)

                        article_html = driver.page_source
                        print("[DEBUG] Page source length:", len(article_html))
                        with open("debug_article_page.html", "w", encoding="utf-8") as f:
                            f.write(article_html)
                        
                        article_content = BeautifulSoup(article_html, "html.parser")
                        container = article_content.find("div", class_="site-content cf")
                        container_sections = container.find_all("article")
                        

                        for container_section in container_sections:
                            print("[DEBUG] Article HTML:\n", container_section.prettify()[:500])
                            # Title
                            content_title_tag = container_section.find("h3", class_="news_post_title")
                            content_title = content_title_tag.get_text(strip=True) if content_title_tag else None
                            print(f"[DEBUG] Title: {content_title}")

                            # Image
                            content_img_tag = container_section.find("div", class_="news_post_photo")
                            if content_img_tag:
                                style = content_img_tag.get("style", "")
                                img_url_match = re.search(r'url\((.*?)\)', style)
                                content_img = img_url_match.group(1) if img_url_match else None
                                if content_img and content_img.startswith("//"):
                                    content_img = "https:" + content_img
                            else:
                                content_img = None
                            print(f"[DEBUG] Image URL: {content_img}")

                            # Summary
                            content_summary_tag = container_section.find("p", class_="summary")
                            content_summary = content_summary_tag.get_text(strip=True) if content_summary_tag else None
                            print(f"[DEBUG] Summary: {content_summary}")

                            if content_title and content_summary and content_img:
                                cursor.execute("INSERT INTO news (title, summary, img, date) VALUES (?, ?, ?, ?)", 
                                            (content_title, content_summary, content_img, str(time)))

                    else:
                        print(f"Skipping incomplete article at {url}")


                