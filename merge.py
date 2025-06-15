import json


merged_data = []
for i in range(80):
    k = i * 50
    # 读取第一个文件
    with open(f"./data/train_processed_{k}_{k+50}.json", "r", encoding="utf-8") as f1:
        data1 = json.load(f1)

    # 合并内容
    merged_data = merged_data + data1

# 保存为新的文件
with open("train_processed_merged.json", "w", encoding="utf-8") as fout:
    json.dump(merged_data, fout, ensure_ascii=False, indent=2)

print("合并完成，输出文件为 train_processed_merged.json")
