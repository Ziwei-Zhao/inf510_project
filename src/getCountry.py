import wbdata
import sqlite3

def main():
    conn = sqlite3.connect('../data/film.db')
    cur = conn.cursor()
    cur.execute('''SELECT * FROM film_info''')
    result = cur.fetchall()

    conn.commit()

    print('Getting iso2code')
    country_dict = {}
    for data in result:
        country_list= data[2].split(',')
        if len(country_list) > 1:
            for country in country_list:
                country = country.strip()
                if country not in country_dict:
                    try:
                        country_code = wbdata.search_countries(country)[0]['iso2Code']
                        country_dict[country] = country_code
                    except:
                        country_dict[country] = ' '

        else:
            country = country_list[0].strip()
            if country not in country_dict:
                try:
                    country_code = wbdata.search_countries(country)[0]['iso2Code']
                    country_dict[country] = country_code
                except:
                    country_dict[country] = ' '

    print('Recording results to country_iso2code.txt')
    f = open('../data/country_iso2code.txt', 'w')
    for key, value in country_dict.items():
        f.write(key + ':' + value + '\n')

    f.close()
    print('Done')




