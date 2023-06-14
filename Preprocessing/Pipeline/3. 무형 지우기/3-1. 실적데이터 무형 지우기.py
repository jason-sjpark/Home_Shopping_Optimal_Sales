import csv

f = open('1. 노출시간 빈칸채우기.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
w = open('2-1. 실적데이터 무형 지우기.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(w)

for line in rdr:
    if line[5] != '무형':
        wr.writerow(line)

f.close()
w.close()