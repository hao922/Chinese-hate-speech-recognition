import json
import argparse


def extract_predict_to_txt(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in, \
                open(output_file, 'w', encoding='utf-8') as f_out:

            line_num = 0
            for line in f_in:
                line_num += 1
                data = json.loads(line.strip())

                if 'predict' in data:
                    predict_text = data['predict']
                    num_newlines = predict_text.count('\n')

                    if num_newlines > 0:
                        print(f"第 {line_num} 行 predict 中包含 {num_newlines} 个换行符")

                    f_out.write(predict_text + '\n')
                else:
                    print(f"警告: 第 {line_num} 行不包含 'predict' 字段")

        print(f"成功从 {input_file} 提取 predict 内容到 {output_file}")

    except FileNotFoundError:
        print(f"错误: 文件 {input_file} 不存在")
    except json.JSONDecodeError as e:
        print(f"错误: JSON解析错误 - {e}")
    except Exception as e:
        print(f"错误: 发生未知错误 - {e}")


if __name__ == "__main__":
    # 执行提取操作
    extract_predict_to_txt("generated_predictions.jsonl", "test1_output.txt")

