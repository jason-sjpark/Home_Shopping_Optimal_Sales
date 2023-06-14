import csv

f = open('./원본/예측데이터.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
w = open('2-2. 예측데이터 무형 지우기.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(w)

for line in rdr:
    if line[3] != '무형':
        wr.writerow(line)

f.close()
w.close()