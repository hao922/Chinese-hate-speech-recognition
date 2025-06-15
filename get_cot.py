import requests
import json
import concurrent.futures
from typing import List, Dict, Any
import argparse

# API配置
url = "https://api.siliconflow.cn/v1/chat/completions"
api_key = " "  # 替换为申请的密钥


def get_answer(input_text: str) -> Dict[str, Any]:
    """发送请求到API获取仇恨言论识别结果"""
    # 构造请求数据
    payload = {
        "model": "Qwen/Qwen2.5-VL-72B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": "### 细粒度片段级中文仇恨言论识别模型Prompt  #### 任务概述 你需要处理社交媒体文本，输出仇恨四元组，格式为：评论对象（Target）| 论点（Argument）| 目标群体（Targeted Group）| 是否仇恨（Hateful）[END]。若有多个四元组，用[SEP]分隔。目标群体包括：地域、种族、性别、LGBTQ、其他5类。非仇恨内容需标注为non-hate。   #### 输入输出规范 - **评论对象（Target）**：具体评述的人或群体，无具体目标时设为NULL - **论点（Argument）**：对评论目标的关键观点片段 - **目标群体（Targeted Group）**：从{地域, 种族, 性别, LGBTQ, 其他}中选择 - **是否仇恨（Hateful）**：判断是否构成仇恨言论，取值为hate或non-hate  **示例1**   输入：你可真是头蠢驴，这都做不好。   输出：你 | 蠢驴 | non-hate | non-hate [END]  **示例2**   输入：老黑我是真的讨厌，媚黑的还倒贴。   输出：老黑 | 讨厌 | Racism | hate [SEP] 媚黑的 | 倒贴 | Racism | hate [END]   #### 决策逻辑指南 1. **分割评论对象与论点**      - 提取文本中被评价的主体作为Target（如“老黑”“媚黑的”）    - 提取对Target的具体评价内容作为Argument（如“讨厌”“倒贴”）  2. **目标群体分类规则**      - **种族（Racism）**：涉及肤色（黑/白）、国籍（非裔/亚裔）、种族称谓（老黑/洋鬼子）    - **性别（Sexism）**：针对男性/女性的歧视性表述（母坦克/普信男）    - **地域（Region）**：地域名称+负面评价（潮汕黑成灰/山东没资格）    - **LGBTQ**：涉及同性恋、性别认同的歧视（基佬/同杏恋）    - **其他（others）**：无法归类到上述群体的仇恨对象（女权/汉奸）  3. **仇恨言论判定标准**      - 包含侮辱性词汇（蠢驴/母坦克）、攻击性论断（该锤死/该枪毙）    - 强化群体刻板印象（黑人=暴力/女性=没人权）    - 煽动对立或排斥（别嫁给黑人/开除女籍）    - 非仇恨场景：单纯事实陈述（“我不跟非裔结婚”需结合语境，若仅表达个人选择则可能为non-hate）   #### 特殊情况处理 - **多四元组场景**     输入：想反女权还得看女权，舔狗龟男理中客们不是男人能打醒的     输出：女权 | 想反女权还得看女权 | Sexism | hate [SEP] 舔狗龟男理中客们 | 不是男人能打醒的 | Sexism | hate [END]  - **隐含评论对象**     输入：没爹的黑孩到处扔     处理：补全Target为“黑孩”，Argument为“没爹的到处扔”     输出：黑孩 | 没爹的到处扔 | Racism | hate [END]  - **非仇恨文本**     输入：你是汉族吗     输出：你 | 是汉族吗 | non-hate | non-hate [END]   #### 输出格式严格要求 - 四元组元素用\" | \"分隔，末尾加[END] - 多四元组用[SEP]连接（如A[END][SEP]B[END]） - 所有英文术语首字母大写（Racism/Sexism） - 无具体目标时Target填NULL（如“国际除虫人人有责”输出：虫 | 国际除虫 | Racism | hate [END]）   #### 测试集处理示例 请按上述规则处理以下样本：   **输入**：就算她不拿刀你就能打得过180斤起步的母坦克?   **输出**：她 | 180斤起步的母坦克 | Sexism | hate [END]  **输入**：评论区里面的三观真让人叹为观止。这就是大国气度？   **输出**：评论区里面的三观 | 叹为观止 | non-hate | non-hate [END]   #### 模型输出要求 请对每条输入文本生成结构化四元组，确保：   1. Target和Argument为文本中实际出现的连续片段   2. Targeted Group分类准确   3. Hateful判断符合仇恨言论定义   4. 格式完全符合\"元素|分隔[END][SEP]元素|分隔[END]\"规范"
            },
            {
                "role": "assistant",
                'content': '### 测试集处理示例\n\n#### 输入1：\n就算她不拿刀你就能打得过180斤起步的母坦克?\n\n#### 输出1：\n她 | 180斤起步的母坦克 | Sexism | hate [END]\n\n#### 处理逻辑：\n- **Target:** "她" 是被评价的主体。\n- **Argument:** "180斤起步的母坦克" 是对“她”的具体评价，其中“母坦克”是侮辱性词汇，针对女性。\n- **Targeted Group:** "Sexism" 因为这里涉及对女性的贬低。\n- **Hateful:** "hate" 因为使用了侮辱性词汇“母坦克”。\n\n#### 输入2：\n评论区里面的三观真让人叹为观止。这就是大国气度？\n\n#### 输出2：\n评论区里面的三观 | 叹为观止 | non-hate | non-hate [END]\n\n#### 处理逻辑：\n- **Target:** "评论区里面的三观" 是被评价的主体。\n- **Argument:** "叹为观止" 是对“评论区里面的三观”的具体评价。\n- **Targeted Group:** "non-hate" 因为没有涉及对特定群体的仇恨言论。\n- **Hateful:** "non-hate" 因为这句评价没有使用侮辱性词汇或攻击性论断，仅是表达个人的观点和疑问。\n\n### 测试集处理示例（新增）\n\n#### 输入3：\n这个地区的人都很懒惰，真是让人失望。\n\n#### 输出3：\n这个地区的人都 | 很懒惰 | Region | hate [END]\n\n#### 处理逻辑：\n- **Target:** "这个地区的人都" 是被评价的主体。\n- **Argument:** "很懒惰" 是对“这个地区的人都”的具体评价。\n- **Targeted Group:** "Region" 因为这里涉及对特定地区的贬低。\n- **Hateful:** "hate" 因为使用了贬低性词语“懒惰”，并且可能强化了对某一地域人群的负面刻板印象。\n\n#### 输入4：\n听说那边的同性恋越来越多，真是乱七八糟。\n\n#### 输出4：\n那边的同性恋 | 越来越多，真是乱七八糟 | Lgbtq | hate [END]\n\n#### 处理逻辑：\n- **Target:** "那边的同性恋" 是被评价的主体。\n- **Argument'
            },
            {
                "role": "user",
                'content': f"{input_text}, 其中，content是输入，output是输出，请同时附上处理逻辑作为reason字段",
            }
        ],
        "stream": False,
        "max_tokens": 4096,
        "enable_thinking": True,
        "thinking_budget": 4096,
        "temperature": 0.7,
        "response_format": {"type": "text"}
    }

    # 设置请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        # 发送请求
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        print(f"请求错误：{e}")
        if hasattr(e, 'response') and e.response:
            print(f"错误详情：{e.response.text}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        print("响应解析失败，非JSON格式数据")
        print(response.text)
        return {"error": "JSON解析失败"}


def process_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    """处理单个数据条目并添加API响应结果"""
    result = get_answer(entry["content"])
    entry["output"] = result.get("choices", [{}])[0].get("message", {}).get("content", "")
    return entry


def load_data(file_path: str) -> List[Dict[str, Any]]:
    """从JSON文件加载数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"错误：文件 {file_path} 不是有效的JSON格式")
        return []


def save_results(results: List[Dict[str, Any]], file_path: str) -> None:
    """将处理结果保存到JSON文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到 {file_path}")
    except Exception as e:
        print(f"保存结果时出错：{e}")


import time  # 确保加在 import 区域

if __name__ == '__main__':
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='批量处理 train.json 数据')
    parser.add_argument('--start', type=int, default=0, help='开始索引（包含）')
    parser.add_argument('--end', type=int, default=4000, help='结束索引（不包含），-1表示处理到结尾')
    args = parser.parse_args()

    # 加载数据
    data = load_data('train.json')

    if not data:
        print("没有数据可处理，程序退出")
    else:
        total_data = len(data)
        start_idx = max(0, args.start)
        end_idx = total_data if args.end == -1 else min(args.end, total_data)

        if start_idx >= end_idx:
            print(f"错误：开始索引({start_idx})必须小于结束索引({end_idx})")
            exit(1)

        batch_size = 50
        total_batches = (end_idx - start_idx + batch_size - 1) // batch_size

        print(f"共加载 {total_data} 条数据，将处理从索引 {start_idx} 到 {end_idx - 1}（共 {end_idx - start_idx} 条，分 {total_batches} 批）")

        for batch_num in range(total_batches):
            batch_start = start_idx + batch_num * batch_size
            batch_end = min(batch_start + batch_size, end_idx)

            data_to_process = data[batch_start:batch_end]
            print(f"\n开始处理第 {batch_num + 1}/{total_batches} 批，索引范围：{batch_start} 到 {batch_end - 1}")

            # 并行处理
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(process_entry, item) for item in data_to_process]
                processed_data = []
                for i, future in enumerate(concurrent.futures.as_completed(futures)):
                    result = future.result()
                    processed_data.append(result)
                    print(f"已处理当前批次的 {i + 1}/{len(data_to_process)} 条数据")

            # 保存
            output_file = f'train_processed_{batch_start}_{batch_end}.json'
            save_results(processed_data, output_file)

            # 等待
            if batch_num < total_batches - 1:
                print("等待30秒后继续处理下一批...")
                time.sleep(30)

        print("\n✅ 所有数据处理完成。")


