# 割合計算をするスクリプト
# 例えば、13700*90%と17800*70%の比較などに使う
# 「使い方」
# スペース区切りで数値を入力してください。
# （A B C D）と入力した場合、A*B/100とC*D/100が計算されます。

while True:
    nums = list(map(int, input().split()))
    if len(nums) == 0:
        break
    value = [l * (1 - r / 100) for l, r in zip(nums[::2], nums[1::2])]

    print(value)