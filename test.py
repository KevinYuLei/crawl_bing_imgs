import os
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

# 代理配置（替换为实际代理地址和端口）
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 图片的 URL
url = "https://edwps.com/wp-content/uploads/2015/12/AdobeStock_85721347.jpeg"

# 本地目录和文件名
save_dir = "./downloaded_images"
file_name = "test2.jpg"

# 确保保存目录存在
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 完整保存路径
save_path = os.path.join(save_dir, file_name)

# 使用持久会话下载图片
with requests.Session() as session:
    session.headers.update(headers)
    response = session.get(url, stream=True, proxies=proxies)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"图片已成功下载到: {save_path}")
    else:
        print("下载失败，状态码:", response.status_code)
