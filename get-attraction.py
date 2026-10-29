import os
from tavily import TavilyClient

def get_attraction(city:str,weather:str) -> str:
    """
    通过调用Tavily的API获取指定城市的旅游景点信息。
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "错误：未设置Tavily API密钥，请在环境变量中设置TAVILY_API_KEY。"

    client = TavilyClient(api_key=api_key)
    prompt = f"请提供{city}的旅游景点信息，并结合当前天气情况：{weather}。"
    
    try:
        response = client.search(query = prompt,search_depth ='basic',include_answer =True )
        if response.get('answer'):
            return response['answer']

        formatted_results = []
        for result in response.get('results',[]):
            formatted_results.append(f'- {result['title']}:{result['content']}')
        if not formatted_results:
            return '抱歉。没有找到相关景点推荐'
        return '根据搜索，为你找到以下信息:\n' + '\n'.join(formatted_results)
    except Exception as e:
        return f"错误：查询旅游景点时遇到问题 - {e}"