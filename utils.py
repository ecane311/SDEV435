import csv

#Reusable read csv function
def readCsv(path, skipheader=False):
    rows=[]
    with open(path, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        if skipheader:
            next(reader, None)
        for row in reader:
            rows.append(row)
    return rows

#reusable write csv function
def writeCsv(path, header, rows):
    with open(path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

#reusable append csv function
def appendCsv(path, row):
    with open(path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)