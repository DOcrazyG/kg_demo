"""
Medical data preprocessing script.
Download medical.json from: https://github.com/liuhuanyong/QASystemOnMedicalKG
"""

import json

# Field mapping (English to Chinese)
FIELD_MAP = {
    "name": "疾病名称",
    "desc": "疾病简介",
    "category": "所属类别",
    "cause": "病因",
    "symptom": "症状",
    "prevent": "预防措施",
    "get_way": "传播途径",
    "get_prob": "发病率",
    "easy_get": "易患人群",
    "acompany": "并发症",
    "cure_department": "治疗科室",
    "cure_way": "治疗方式",
    "cure_lasttime": "治疗时长",
    "cured_prob": "治愈率",
    "cost_money": "治疗费用",
    "check": "检查项目",
    "common_drug": "常用药物",
    "recommand_drug": "推荐药物",
    "do_eat": "宜吃食物",
    "not_eat": "忌吃食物",
    "recommand_eat": "推荐食谱",
    "yibao_status": "医保状态",
}


def clean_text(text):
    """Clean text by removing newlines and extra spaces."""
    if not text:
        return ""
    return str(text).replace("\n", "").replace("\r", "").strip()


def format_list(items):
    """Format list to Chinese comma-separated string."""
    if not items:
        return ""
    if isinstance(items, list):
        return "、".join([str(i) for i in items if i])
    return str(items)


def convert_to_text(data):
    """Convert single disease data to text description."""
    parts = []

    # Name
    name = clean_text(data.get("name"))
    if name:
        parts.append(f"{name}")

    # Description
    desc = clean_text(data.get("desc"))
    if desc:
        parts.append(f"简介：{desc}")

    # Category
    category = format_list(data.get("category"))
    if category:
        parts.append(f"所属类别：{category}")

    # Cause
    cause = clean_text(data.get("cause"))
    if cause:
        parts.append(f"病因：{cause}")

    # Symptom
    symptom = format_list(data.get("symptom"))
    if symptom:
        parts.append(f"症状：{symptom}")

    # Prevention
    prevent = clean_text(data.get("prevent"))
    if prevent:
        parts.append(f"预防措施：{prevent}")

    # Transmission
    get_way = clean_text(data.get("get_way"))
    if get_way:
        parts.append(f"传播途径：{get_way}")

    # Incidence rate
    get_prob = clean_text(data.get("get_prob"))
    if get_prob:
        parts.append(f"发病率：{get_prob}")

    # Susceptible population
    easy_get = clean_text(data.get("easy_get"))
    if easy_get:
        parts.append(f"易患人群：{easy_get}")

    # Complications
    acompany = format_list(data.get("acompany"))
    if acompany:
        parts.append(f"并发症：{acompany}")

    # Treatment department
    cure_department = format_list(data.get("cure_department"))
    if cure_department:
        parts.append(f"治疗科室：{cure_department}")

    # Treatment method
    cure_way = format_list(data.get("cure_way"))
    if cure_way:
        parts.append(f"治疗方式：{cure_way}")

    # Treatment duration
    cure_lasttime = clean_text(data.get("cure_lasttime"))
    if cure_lasttime:
        parts.append(f"治疗时长：{cure_lasttime}")

    # Cure rate
    cured_prob = clean_text(data.get("cured_prob"))
    if cured_prob:
        parts.append(f"治愈率：{cured_prob}")

    # Cost
    cost_money = clean_text(data.get("cost_money"))
    if cost_money:
        parts.append(f"治疗费用：{cost_money}")

    # Check items
    check = format_list(data.get("check"))
    if check:
        parts.append(f"检查项目：{check}")

    # Common drugs
    common_drug = format_list(data.get("common_drug"))
    if common_drug:
        parts.append(f"常用药物：{common_drug}")

    # Recommended drugs
    recommand_drug = format_list(data.get("recommand_drug"))
    if recommand_drug:
        parts.append(f"推荐药物：{recommand_drug}")

    # Recommended foods
    do_eat = format_list(data.get("do_eat"))
    if do_eat:
        parts.append(f"宜吃食物：{do_eat}")

    # Avoided foods
    not_eat = format_list(data.get("not_eat"))
    if not_eat:
        parts.append(f"忌吃食物：{not_eat}")

    # Recommended diet
    recommand_eat = format_list(data.get("recommand_eat"))
    if recommand_eat:
        parts.append(f"推荐食谱：{recommand_eat}")

    # Insurance status
    yibao_status = clean_text(data.get("yibao_status"))
    if yibao_status:
        parts.append(f"医保状态：{yibao_status}")

    return "。".join([p for p in parts if p]) + "。"


def process_medical_json(
    input_file="data/medical.json", output_file="data/medical.csv"
):
    """Process medical.json and output as Chinese text descriptions."""
    results = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    text = convert_to_text(data)
                    if text.strip():
                        results.append(text)
                except json.JSONDecodeError:
                    continue

    with open(output_file, "w", encoding="utf-8") as f:
        for text in results:
            f.write(text + "\n\n")

    print(f"已成功转换 {len(results)} 条记录到 {output_file}")


if __name__ == "__main__":
    process_medical_json()
