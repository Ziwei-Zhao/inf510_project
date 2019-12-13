import argparse
import film_API, getCountry, Spider, analysis, getGDP
import os


def get_info():
    parser = argparse.ArgumentParser()
    parser.add_argument("-source", choices=["local", "test"], help="where data should be gotten from")
    args = parser.parse_args()

    location = args.source

    if location == "local":
        if os.path.exists('../data/movies_name.txt'):
            film_API.main('../data/movies_name.txt')
            getCountry.main()
            getGDP.main()
        else:
            print('You need to run "-source=test" to gain source data!')

    else:
        Spider.main()
        film_API.main('../data/movies_name.txt')
        getCountry.main()
        getGDP.main()

def Analysis():
    analysis.UpdateGDP()
    analysis.film_Analysis()
    analysis.country_analysis()

if __name__ == '__main__':
    get_info()
    try:
        Analysis()
        analysis.GDP_Analysis('USA')
    except:
        print('Fail, Try to run again -source=test')

