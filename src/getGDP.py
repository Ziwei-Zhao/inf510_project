from pandas_datareader import wb
import sqlite3
import os

def main():
    conn = sqlite3.connect('../data/film.db')
    cur = conn.cursor()
    cur.execute('''SELECT * FROM film_info''')
    result = cur.fetchall()

    conn.commit()

    country_mapping = {}
    f = open('../data/country_iso2code.txt', 'r')
    for line in f.readlines():
        line = line.strip()
        k = line.split(':')[0]
        v = line.split(':')[1]
        country_mapping[k] = v
    f.close()

    print('Getting GDP information and writing to gdp.txt')
    if not os.path.exists('../data/gdp.txt'):
        f1 = open('../data/gdp.txt', 'w')
        for info in result:
            year = int(info[1])
            country_list = info[2].split(',')

            if len(country_list) > 1:
                for country in country_list:
                    country = country.strip()
                    country_code = country_mapping[country]
                    try:
                        dat = wb.download(indicator='NY.GDP.PCAP.CD', country=country_code, start=year, end=year)
                        dat.columns = ['GDP']
                        f1.write(country + ':' + info[1] + ':' + str(dat['GDP'][0]) + '\n')
                    except:
                        f1.write(country + ':' + info[1] + ':' + '#' + '\n')

            else:
                country = country_list[0].strip()
                country_code = country_mapping[country]
                try:
                    dat = wb.download(indicator='NY.GDP.PCAP.CD', country=country_code, start=year, end=year)
                    dat.columns = ['GDP']
                    f1.write(country + ':' + info[1] + ':' + str(dat['GDP'][0]) + '\n')
                except:
                    f1.write(country + ':' + info[1] + ':' + '#' + '\n')

        f1.close()
        print('Done')
    else:
        print('gdp.txt already exist.')


