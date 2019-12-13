import sqlite3
import matplotlib.pyplot as plt

def UpdateGDP():
    conn = sqlite3.connect('../data/film.db')
    cur = conn.cursor()
    try:
        cur.execute('''ALTER TABLE film_info ADD COLUMN GDP TEXT''')
        conn.commit()
    except sqlite3.OperationalError:
        pass

    f = open('../data/gdp.txt', 'r')
    check_gdp = {}
    for line in f.readlines():
        line = line.strip().split(':')
        value = line[2]
        if '.' in value:
            value = value.split('.')[0] + '.' + value.split('.')[1][:2]
        check_gdp[line[0] + line[1]] = value
    f.close()

    cur.execute('''SELECT * FROM film_info''')
    rows = cur.fetchall()
    print('Updating GDP to database')
    for row in rows:
        countries = row[2].strip().split(',')
        if len(countries) == 1:
            if row[2] + row[1] in check_gdp:
                gdp = check_gdp[row[2] + row[1]]
                cur.execute('''UPDATE film_info set GDP = ? WHERE Year=? and Country=?''', (gdp, row[1], row[2]))
                conn.commit()
            else:
                continue
        else:
            gdp = ''
            for country in countries:
                if country.strip() + row[1] in check_gdp:
                    gdp += check_gdp[country.strip() + row[1]] + ','
                else:
                    continue
            cur.execute('''UPDATE film_info set GDP = ? WHERE Year=? and Country=?''', (gdp, row[1], row[2]))
            conn.commit()

    conn.commit()
    cur.close()
    conn.close()
    print('Done')

def film_Analysis():
    print('Analyzing film information ')
    conn = sqlite3.connect('../data/film.db')
    cur = conn.cursor()
    cur.execute('''SELECT Year as year, COUNT(*) as times FROM film_info GROUP BY Year''')
    results = cur.fetchall()
    x, y = [], []
    for result in results:
        x.append(result[0])
        y.append(result[1])

    plt.figure(figsize=(20, 2))
    plt.xticks(fontsize=5)
    plt.plot(x, y)
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.savefig('../data/year_times.png')
    plt.close()
    cur.close()
    conn.close()
    print('Done, result has been exported to ../data/year_times.png')

def country_analysis():
    print('Analyzing country information ')
    conn = sqlite3.connect('../data/film.db')
    cur = conn.cursor()
    cur.execute('''SELECT Country FROM film_info''')
    results = cur.fetchall()
    countries = {}
    for result in results:
        result = result[0].split(',')
        for country in result:
            if country.strip() in countries:
                countries[country.strip()] += 1
            else:
                countries[country.strip()] = 1

    sample = sorted(countries.items(), key=lambda ele: ele[1], reverse=True)[:10]
    labels = [sample[i][0] for i in range(len(sample))]
    values = [sample[i][1] for i in range(len(sample))]
    plt.figure()
    plt.pie(values, labels=labels, autopct='%1.2f%%')
    plt.title('Countries')
    plt.savefig('../data/Countries.png')
    plt.close()
    cur.close()
    conn.close()
    print('Done, result has been exported to ../data/Countries.png')

def GDP_Analysis(countryname):
    print('Analyzing GDP of {}'.format(countryname))
    record = {}
    f = open('../data/gdp.txt', 'r')
    for line in f.readlines():
        info = line.strip().split(':')
        if info[0] == countryname:
            if info[1] not in record and '.' in info[2]:
                record[info[1]] = info[2].split('.')[0] + '.' + info[2].split('.')[1][:2]

    GDP = sorted(record.items(), key=lambda ele: ele[0])
    x = [GDP[i][0] for i in range(len(GDP))]
    y = [GDP[i][1] for i in range(len(GDP))]
    plt.figure(figsize=(15, 15))
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=10)
    plt.xlabel('Year')
    plt.ylabel('GDP')
    plt.plot(x, y)
    plt.savefig('../data/{}_GDP.png'.format(countryname))
    plt.close()
    print('Done, the result has been exported to ../data/{}_GDP.png'.format(countryname))












