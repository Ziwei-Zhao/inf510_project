import requests
import sqlite3
import os

def main(filename):
    key = 'f7ff3393'
    film_info_list = []
    if not os.path.exists('../data/film_info_list.txt'):
        print('Getting film information from website')
        f = open('../data/film_info_list.txt', 'w')
        for line in open(filename):
            film_name = line.replace(' ', '+')
            url = 'http://www.omdbapi.com/?apikey={0}&t={1}&r=json'.format(key, film_name)
            r = requests.get(url)
            film_info_str = r.text
            f.write(film_info_str + '\n')
            film_info_dict = eval(film_info_str)
            film_info_list.append(film_info_dict)

        f.close()
    else:
        print('Getting film information from local')
        f = open('../data/film_info_list.txt', 'r')
        for line in f.readlines():
            film_info_dict = eval(line)
            film_info_list.append(film_info_dict)
        f.close()
    print('Finished')
    conn = sqlite3.connect('../data/film.db')
    cur = conn.cursor()
    print('Inserting data into database')
    try:
        cur.execute('''CREATE TABLE film_info
               (Name TEXT,
                Year TEXT,
                Country TEXT)
               ;''')
        conn.commit()

        for film in film_info_list:
            try:
                cur.execute('''INSERT INTO film_info VALUES (?, ?, ?)''', (film['Title'], film['Year'], film['Country']))
            except:
                continue
    except sqlite3.OperationalError:
        for film in film_info_list:
            try:
                cur.execute('''INSERT INTO film_info VALUES (?, ?, ?)''', (film['Title'], film['Year'], film['Country']))
            except:
                continue

    conn.commit()
    cur.close()
    conn.close()
    print('Done')

if __name__ == '__main__':
    main('../data/movies_name.txt')















