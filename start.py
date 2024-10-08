import os
from utils.create_next_exp_folder import create_next_exp_folder
from utils.fetch_dynamic_content import fetch_dynamic_content
from utils.extract_img_urls import extract_img_urls
from utils.remove_duplicate_urls import remove_duplicate_urls
from utils.download_imgs_from_blob_urls import download_imgs_from_blob_urls
from utils.download_imgs_from_urls import download_imgs_from_urls


if __name__ == '__main__':
    # 需要爬取的bing.com/images网址
    # bing_img_url = "https://cn.bing.com/images/search?q=smartphone+on+the+desk&qs=n&form=QBIR&sp=-1&lq=0&pq=smartphone%20on%20the%20desk&sc=7-22&cvid=FB071787232E4B959DF4D4F6EF0F3F1B&ghsh=0&ghacc=0&first=1&cw=1903&ch=653"
    # bing_img_url = "https://www.bing.com/images/search?q=mobile+on+desk&qs=n&form=QBILPG&sp=-1&lq=0&pq=mobile+on+desk&sc=10-14&cvid=FBC7933A4ED345F28A47E0D8FF2FB8DD&ghsh=0&ghacc=0&first=1"
    # bing_img_url = "https://www.bing.com/images/search?q=phone%20on%20the%20desk&qs=SSA&form=QBIR&sp=1&lq=0&pq=phone%20on%20he%20desk&sc=9-16&cvid=E98CAD65D8B84650865A7C23A713FF1E&ghsh=0&ghacc=0&first=1"
    # bing_img_url = "https://www.bing.com/images/search?q=SAO&qs=n&form=QBIR&sp=-1&lq=0&pq=sao&sc=10-3&cvid=3DBE083CCD894388ABC106330F3F93FA&ghsh=0&ghacc=0&first=1"
    
    # exp7 - 腿放在桌子上
    bing_img_url = "https://www.bing.com/images/search?q=%E8%85%BF%E6%94%BE%E5%9C%A8%E6%A1%8C%E5%AD%90%E4%B8%8A&qs=LT&form=QBILPG&sp=1&lq=0&pq=%E8%85%BF%E6%94%BE%E5%9C%A8&sc=4-3&cvid=64993AD720D64F94BECFAB3944B47949&ghsh=0&ghacc=0&first=1"
    
    cwd = os.getcwd()
    imgs_dir = os.path.join(cwd, 'downloaded_imgs')
    runs_dir = os.path.join(cwd, 'runs')
    
    # imgs_exp_folder 用于保存每次运行时爬取url所下载的图片
    imgs_exp_dir = create_next_exp_folder(imgs_dir)
    # runs_exp_folder 用于保存每次运行时所爬取的html_content文件与largest_image_urls文件
    runs_exp_dir = create_next_exp_folder(runs_dir)
    
    # # 创建html文件及其路径
    # html_filename = 'html_content.txt'
    # html_file_path = os.path.join(runs_exp_folder, html_filename)
    
    # 创建存取url的文件及其路径
    imgs_url_filename = 'image_urls.txt'
    imgs_url_path = os.path.join(runs_exp_dir, imgs_url_filename)
    
    # 调用函数，获取页面滚动过程中收集的所有HTML内容
    fetch_dynamic_content(bing_img_url, imgs_url_path)
    
    # # 调用函数，从html文件中获取image的url
    # extract_img_urls(html_file_path, imgs_url_path)
    
    # 调用函数去除重复的URL
    remove_duplicate_urls(imgs_url_path)
    
    # 调用函数下载图片
    download_imgs_from_urls(imgs_url_path, imgs_exp_dir)