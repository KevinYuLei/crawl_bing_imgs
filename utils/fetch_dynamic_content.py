import time
import os
import keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fetch_dynamic_content(url, save_file_path):
    # 设置Chrome浏览器的选项，确保浏览器不会显示自动化工具控制的提示信息
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')  # 禁用GPU加速（可选）
    options.add_argument('--start-maximized')  # 启动时最大化窗口

    # 启动Chrome浏览器，使用上述配置
    driver = webdriver.Chrome(options=options)

    # 通过Chrome DevTools Protocol (CDP) 禁用webdriver特征检测，使浏览器看起来像是由人操作的
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })

    # 访问bing/images页面
    driver.get(url)

    # 定位页面中用于展示图片的动态元素的CSS选择器
    element_selector = "#mmComponent_images_1"
    
    # 手动刷新页面确保能获取CSS选择器
    keyboard.press_and_release('f5')
    # 短暂停顿0.5s
    time.sleep(0.5)

    # 等待页面的初始加载，直到目标元素出现在页面中
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, element_selector))
    )



    # 获取页面目前总高度
    last_height = driver.execute_script("return document.body.scrollHeight")
    

    # 通过模拟滚动操作，逐步加载页面内容，直到内容加载完毕
    while True:
        driver.execute_script(f"window.scrollTo(0, {last_height})")
        # 等待3秒，确保新内容加载完毕
        time.sleep(3)
        
        # 获取当前滚动后的页面高度
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 如果当前页面高度等于document.body.scrollHeight，说明到达页面底部，退出循环
        if abs(new_height - last_height) < 10:  # 允许10像素的误差范围
            break
        else:
            last_height = new_height

    # 获取当前页面中目标元素的动态HTML内容
    dynamic_elements = driver.find_elements(
            By.CSS_SELECTOR, element_selector)
    dynamic_html_content = "\n".join(
            [element.get_attribute('innerHTML') for element in dynamic_elements])
    # 关闭浏览器，释放资源
    driver.quit()
    
    save_filename = os.path.basename(save_file_path)
    # 将收集的HTML内容保存到txt文件中
    with open(save_file_path, 'w', encoding='utf-8') as file:
        file.write(dynamic_html_content)
        file.write('\n')
        print(f"HTML内容已保存到 {save_filename} 文件中。")



if __name__ == '__main__':
    bing_img_url = "https://cn.bing.com/images/search?q=smartphone+on+the+desk&qs=n&form=QBIR&sp=-1&lq=0&pq=smartphone%20on%20the%20desk&sc=7-22&cvid=FB071787232E4B959DF4D4F6EF0F3F1B&ghsh=0&ghacc=0&first=1&cw=1903&ch=653"
    
    cwd = os.getcwd()
    runs_folder = os.path.join(cwd, 'runs')

    html_filename = 'html_content.txt'
    html_file_path = os.path.join(runs_folder, html_filename)

    # 调用函数，获取页面滚动过程中收集的所有HTML内容
    fetch_dynamic_content(bing_img_url, html_file_path)
