import requests

def get_weather(city:str) -> str:
    """
    通过调用wttr.in的API获取指定城市的天气信息。
    """
    url = f"https://wttr.in/{city}?format=j1"
    try:
        reponse = requests.get(url,timeout =30) # 发送GET请求
        reponse.raise_for_status()  # 检查请求是否成功(200为成功)
        data = reponse.json()  # 将响应内容解析为JSON格式

        # 提取当前天气状况
        current_condition = data['current_condition'][0]
        weather_desc = current_condition['weatherDesc'][0]['value']
        temp_c = current_condition['temp_C']

        # 格式化成自然语言返回
        return f"{city}当前天气：{weather_desc}，温度为{temp_c}°C。"
    except requests.exceptions.RequestException as e:
        return f"错误：查询天气时遇到网络问题 - {e}"
    except (KeyError, IndexError) as e:
        return f"错误：无法解析天气数据,可能是城市名称无效- {e}"
