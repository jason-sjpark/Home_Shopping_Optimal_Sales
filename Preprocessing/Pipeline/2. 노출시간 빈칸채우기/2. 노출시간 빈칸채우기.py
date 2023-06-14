import csv

f = open('./원본/실적데이터.csv', 'r', encoding='utf-8')
rdr1 = csv.reader(f)
w = open('1. 노출시간 빈칸채우기.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(w)

for line1 in rdr1:
    if line1[1]=='':
        datetime = line1[0]
        foundtime = 20000
        s = open('./원본/실적데이터.csv', 'r', encoding='utf-8')
        rdr2 = csv.reader(s)
        for line2 in rdr2:
            if line2[0] == datetime:
                foundedtime = line2[1]
                break
        line1[1] = foundedtime
    wr.writerow(line1)

f.close()
w.close()
s.close()