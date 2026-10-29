import re

API_KEY = ""
BASE_URL = ""
MODEL_ID = ""
TAVILY_API_KEY = ""
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

llm = OpenAICompatibleClient(
    model=MODEL_ID,
    api_key=API_KEY,
    base_url=BASE_URL
)

user_prompt = input("请输入您的问题：")
prompt_history = [f'用户请求:{user_prompt}']
print(f'用户请求:{user_prompt}\n' + "=" * 40)

#运行主循环
for i in range(5):
    print(f'第{i+1}轮对话')
    #构建prompt
    full_prompt = "\n".join(prompt_history)
    #调用llm生成回应
    llm_output = llm.generate(prompt=full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
    #模型可能会输出多余的thought-action，需要截断
    match = re.search(r"(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)",
                       llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("检测到多余的Thought-Action，已截断")
    print(f'模型输出:\n{llm_output}\n' + "=" * 40)
    prompt_history.append(f'模型输出:{llm_output}')

    #解析并执行任务
    action_match = re.search(r"Action:\s*(.*)", llm_output, re.DOTALL)
    if not action_match:
        observation = "未检测到Action，请确保你的回复严格遵循 Thought-Action 格式。"
        observation_str = f"Observation: {observation}"
        print(f'{observation_str}\n' + "=" * 40)
        prompt_history.append(observation_str)
        continue
    action_str = action_match.group(1).strip() 

    if action_str.startswith("Finish"):
        finial_answer = re.match(r"Finish\((.*)\)", action_str)
        print(f'任务完成，最终答案: {finial_answer}')
        break

    tool_name = re.search(r"(\w+)\(", action_str).group(1)
    args_str = re.search(r"\((.*)\)", action_str).group(1)
    kwargs = dict(re.findall(r"(\w+)\s*=\s*'([^']*)'", args_str))

    if tool_name in available_tools:
        observation = available_tools[tool_name](**kwargs)
    else:
        observation = f"未找到工具: {tool_name}，请确保工具名称正确。"

    #记录观察结果
    observation_str = f"Observation: {observation}"
    print(f'{observation_str}\n' + "=" * 40)
    prompt_history.append(observation_str)