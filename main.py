import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def fetch_wikipedia_content(url):
    # 發送 GET 請求
    if("http" not in url):
        url="https://zh.wikipedia.org/wiki/"+url
        
    response = requests.get(url)

    # 檢查響應的狀態碼
    if response.status_code == 200:
        # 解析 HTML 響應
        soup = BeautifulSoup(response.text, "html.parser")

        # 找到整個內容的主要部分
        content_div = soup.find(id="content")

        # 提取所有段落內容
        paragraphs = content_div.find_all("p")

        # 創建空字串以保存內容
        content = ""
        for paragraph in paragraphs:
            content += paragraph.text + "\n"

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
    content= None
    if(args.url):
        url = args.url
        content = fetch_wikipedia_content(url)
    elif(args.topic):
        topic = args.topic
        content = fetch_wikipedia_content(topic)

    # 輸出內容
    if content:
        print(content)


if __name__ == "__main__":
    main()
