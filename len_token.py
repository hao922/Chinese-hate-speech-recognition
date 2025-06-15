from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("/data/xuqi/hog/nlp/model")
text = "请将以下句子划分为四元组"
tokens = tokenizer.encode(text)
print("Token 数量:", len(tokens))

