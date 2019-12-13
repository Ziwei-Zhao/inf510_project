import requests
from bs4 import BeautifulSoup

# I change the size of the film name data set from 500(I mentioned in Milestone1)to 200.
# Since the API I need to use in next steps has a 1000 limits per day.
# I don't want my program can only run two times a day...
def get_film_name():
    name_list = []
    pages = [1, 51, 101, 151]
    for page_number in pages:
        url = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&start={}&ref_=adv_nxt'.format(page_number)
        r = requests.get(url)
        page = r.text

        soup = BeautifulSoup(page, 'html.parser')
        for tag in soup.find_all('div', class_='lister-item mode-advanced'):
            info = tag.find('h3', class_='lister-item-header')
            name = info.find('a').get_text()
            name_list.append(name)

    return name_list

def main():
    print('Getting the film names from the website')
    films = get_film_name()
    print('Writing the film names to movies_name.txt')
    f = open('../data/movies_name.txt', 'w')
    for name in films:
        f.write(name + '\n')

    f.close()
    print('Success!')

if __name__ == '__main__':
    main()








