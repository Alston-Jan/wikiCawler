import argparse
import requests
from bs4 import BeautifulSoup

# from urllib.parse import urlparse
import re


def remove_numeric_and_specific_substrings(input_string):
    # 使用正则表达式匹配所有包含数字和特定文本的子字符串
    pattern = r"\[[^\]]*\]|\[需要較佳來源\]"  # 匹配形如 [数字] 的子字符串和特定文本
    result = re.sub(pattern, "", input_string)  # 用空字符串替换匹配到的子字符串
    print(result)
    return result


def findTitle(inputString):
    firstPeriod = inputString.find("。")
    title = inputString[: firstPeriod + 1]
    return title


def fetch_wikipedia_content(url):
    # 發送 GET 請求
    if "http" not in url:
        url = "https://zh.wikipedia.org/wiki/" + url

    response = requests.get(url)

    # 檢查響應的狀態碼
    if response.status_code == 200:
        # 解析 HTML 響應
        soup = BeautifulSoup(response.text, "html.parser")

        # 找到整個內容的主要部分
        content_div = soup.find(id="content")

        # 提取所有段落內容
        paragraphs = content_div.find_all("p")

        title = findTitle(paragraphs[0].text)
        print(title)
        # 創建空字串以保存內容
        content = ""
        for paragraph in paragraphs:
            paragraph = remove_numeric_and_specific_substrings(paragraph.text)
            if(paragraph != "\n"):
                content += (title + paragraph + "\n")

        return content
    else:
        print("Failed to fetch Wikipedia content.")
        return None


def main():
    # 創建解析器
    parser = argparse.ArgumentParser(
        description="Fetch Wikipedia content for a given URL."
    )
    parser.add_argument("--url", type=str, help="The URL of the Wikipedia page")
    parser.add_argument("--topic", type=str, help="The topic of the Wikipedia")

    # 解析命令列參數
    args = parser.parse_args()

    # 擷取URL並爬取內容
    content = None
    if args.url:
        url = args.url
        content = fetch_wikipedia_content(url)
    elif args.topic:
        topic = args.topic
        content = fetch_wikipedia_content(topic)

    # 輸出內容
    if content:
        print(content)


if __name__ == "__main__":
    main()
