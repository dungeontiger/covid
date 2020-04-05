import pandas as pd


def create_country_menu():
    df = pd.read_csv('data/covid_country.csv')
    countries = df['Country'].unique()
    # create a map of lists
    name_map = {}
    for country in countries:
        first_letter = country[0:1]
        if first_letter not in name_map:
            name_map[first_letter] = []
        name_map[first_letter].append(country)
    # get the list of keys from the map and sort them (just to be sure)
    letters = sorted(name_map.keys())
    # build up the menu for GitHub.io (navbar in bootstrap)
    output = '<div class="container">\n'
    for l in letters:
        list_countries = sorted(name_map[l])
        label = list_countries[0] + '...' + list_countries[len(list_countries) - 1]
        output += '    <div class="row"><a class="dropdown-item" href="javascript:$(\'#{}\').toggleClass(\'collapse\')">{}</a></div>\n'.format(l, label)
        output += '    <div class="collapse" id="{}">\n'.format(l)
        for c in list_countries:
            output += '            <a class="dropdown-item" href="javascript:country_handler(\'{}\')">{}</a>\n'.format(c.replace(' ', '-'), c)
        output += '    </div>\n'
    output += '</div>\n'
    with (open('output.html', 'w')) as f:
        f.write(output)


if __name__ == "__main__":
    create_country_menu()

