import pandas as pd

input_dir = "./input"
output_dir = "./output"

file_path = input_dir + '/raw_test.csv'

df = pd.read_csv(file_path)

print(df.info())
print(df.describe())

# json 파일 저장
# with open('output_file_path', 'w', encoding='utf-8') as f:
#     data.to_json(f, force_ascii=False, orient='records')
    