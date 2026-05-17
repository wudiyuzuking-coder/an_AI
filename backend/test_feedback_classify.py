import requests

BASE_URL = "http://127.0.0.1:8080/api/feedback"

test_cases = [
    {
        "input": "今天一食堂的餐具上全是油，根本没洗干净。",
        "expected": "食品卫生"
    },
    {
        "input": "打菜的那个胖阿姨，手抖得厉害，跟她多要点饭还冲我翻白眼。",
        "expected": "服务态度"
    },
    {
        "input": "素菜都卖5块钱一盘了，能不能考虑一下民生啊？",
        "expected": "菜价建议"
    }
]

print("=" * 60)
print("反馈分类功能测试")
print("=" * 60)

for i, case in enumerate(test_cases, 1):
    print(f"\n测试用例 {i}:")
    print(f"输入: {case['input']}")
    print(f"期望分类: {case['expected']}")
    
    res = requests.post(BASE_URL, json={"content": case["input"]})
    
    if res.status_code == 200:
        data = res.json()
        actual = data.get("category", "未知")
        status = "通过" if actual == case["expected"] else "失败"
        print(f"实际分类: {actual}")
        print(f"状态: {status}")
        print(f"返回消息: {data.get('message', '')}")
    else:
        print(f"请求失败: {res.status_code}")
    
    print("-" * 60)

print("\n测试完成！")
