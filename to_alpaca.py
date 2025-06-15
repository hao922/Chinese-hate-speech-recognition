import json


def train_to_alpaca():
    # 原始文件路径
    file_path = "train.json"

    # 读取原始 JSON 数据
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 转换为 Alpaca 格式
    alpaca_format = []
    # instruction = (
    #     "请判断下面的句子是否包含仇恨言论，并提取评论对象、论点、目标群体、是否仇恨，输出格式为：评论对象 | 论点 | 目标群体 | hate/not_hate。"
    # )
    instruction = (
        "本任务为细粒度片段级中文仇恨言论识别。给定社交媒体文本，需抽取仇恨四元组，顺序依次为："
        "评论对象（Target）、论点（Argument）、目标群体（Targeted Group）、是否仇恨（Hateful）。\n\n"

        "四元组定义如下：\n"
        "1. 评论对象（Target）：帖子的评述对象，如某人或某群体；无具体对象时设为 NULL。\n"
        "2. 论点（Argument）：针对评论对象的核心攻击内容或观点。\n"
        "3. 目标群体（Targeted Group）：该评论对象-论点对所针对的群体。可选类别为：“地域”、“种族”、“性别”、“LGBTQ”、“其他”。\n"
        "4. 是否仇恨（Hateful）：判断该评论是否为仇恨言论，标签为 hate 或 non-hate。\n\n"

        "注意事项：\n"
        "- 非仇恨文本或未明确指向特定群体的攻击性言论，也需提取评论对象和论点，Hateful 标签设为 non-hate。\n"
        "- 一条文本可能包含多个四元组，需逐一提取。\n\n"

        "输出格式：每个四元组用 ' | ' 分隔，以 [END] 结尾；多个四元组之间用 [SEP] 分隔。\n"
        "示例输出：评论对象 | 论点 | 目标群体 | hate [END] 评论对象2 | 论点2 | 目标群体2 | non-hate [END]"
    )

    for entry in data:
        alpaca_entry = {
            "instruction": instruction,
            "input": entry.get("content", ""),
            "output": entry.get("output", "")
        }
        alpaca_format.append(alpaca_entry)

    # 保存为新文件
    output_path = "train_alpaca.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(alpaca_format, f, ensure_ascii=False, indent=2)

    print(f"Alpaca 格式数据已保存到: {output_path}")


def test_to_alpaca():
    # 原始文件路径
    input_file = "test1.json"
    # 转换后文件路径
    output_file = "test1_alpaca.json"

    # 统一的 prompt 指令
    # instruction = (
    #     "请判断下面的句子是否包含仇恨言论，并提取评论对象、论点、目标群体、是否仇恨，输出格式为：评论对象 | 论点 | 目标群体 | hate/not_hate。"
    # )
    instruction = (
        "本任务为细粒度片段级中文仇恨言论识别。给定社交媒体文本，需抽取仇恨四元组，顺序依次为："
        "评论对象（Target）、论点（Argument）、目标群体（Targeted Group）、是否仇恨（Hateful）。\n\n"

        "四元组定义如下：\n"
        "1. 评论对象（Target）：帖子的评述对象，如某人或某群体；无具体对象时设为 NULL。\n"
        "2. 论点（Argument）：针对评论对象的核心攻击内容或观点。\n"
        "3. 目标群体（Targeted Group）：该评论对象-论点对所针对的群体。可选类别为：“地域”、“种族”、“性别”、“LGBTQ”、“其他”。\n"
        "4. 是否仇恨（Hateful）：判断该评论是否为仇恨言论，标签为 hate 或 non-hate。\n\n"

        "注意事项：\n"
        "- 非仇恨文本或未明确指向特定群体的攻击性言论，也需提取评论对象和论点，Hateful 标签设为 non-hate。\n"
        "- 一条文本可能包含多个四元组，需逐一提取。\n\n"

        "输出格式：每个四元组用 ' | ' 分隔，以 [END] 结尾；多个四元组之间用 [SEP] 分隔。\n"
        "示例输出：评论对象 | 论点 | 目标群体 | hate [END] 评论对象2 | 论点2 | 目标群体2 | non-hate [END]"
    )

    with open(input_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    converted_data = []
    for item in raw_data:
        converted_data.append({
            "instruction": instruction,
            "input": item["content"],
            "output": ""
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # train_to_alpaca()
    test_to_alpaca()
