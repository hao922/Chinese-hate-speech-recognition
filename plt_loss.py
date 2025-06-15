import json
import matplotlib.pyplot as plt

steps = []
losses = []
lrs = []

# 读取 trainer_log.jsonl
with open("train_loss/trainer_log_e6.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        log = json.loads(line.strip())
        if "loss" in log and "current_steps" in log and "lr" in log:
            steps.append(log["current_steps"])
            losses.append(log["loss"])
            lrs.append(log["lr"])

if not steps:
    print("没有读取到任何数据，请检查文件格式。")
else:
    # 找最小 Loss 及对应 Step
    min_loss = min(losses)
    min_index = losses.index(min_loss)
    min_step = steps[min_index]

    # 创建图形
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # 左轴：绘制 Loss 曲线
    ax1.plot(steps, losses, marker='o', linestyle='-', color='blue', label='Training Loss', markersize=1)
    ax1.set_xlabel("Training Steps")
    ax1.set_ylabel("Loss", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # 标出最小 Loss 点
    ax1.scatter(min_step, min_loss, color='red', label=f'Min Loss: {min_loss:.4f}', zorder=5)
    ax1.annotate(f'{min_loss:.4f} at step {min_step}',
                 xy=(min_step, min_loss),
                 xytext=(min_step + 50, min_loss + 0.1),
                 arrowprops=dict(arrowstyle='->', color='red'),
                 fontsize=9, color='red')

    # 右轴：绘制 Learning Rate 曲线
    ax2 = ax1.twinx()
    ax2.plot(steps, lrs, color='orange', linestyle='--', label='Learning Rate')
    ax2.set_ylabel("Learning Rate", color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    # 图例合并两个轴的曲线
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

    # 布局、保存和显示
    plt.title("Training Loss and Learning Rate over Steps")
    plt.tight_layout()
    plt.savefig("training_plot.png", dpi=300)
    plt.show()
