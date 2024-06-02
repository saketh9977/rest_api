import duckdb

import pprint

IN_FILE_PATH = '../in/zomato_dataset.csv'

def get_dish_details(dish, city):
    dish_ = dish.lower()
    city_ = city.lower()

    query = f"""
select
    restaurant,
    round((dining_rating + delivery_rating) / 2, 1) as rating,
    cuisine,
    place_name,
    city,
    list(item_name order by t.votes desc) as item_name_list,
    list(votes order by t.votes desc) as votes_list,
    list(price order by t.votes desc) as price_inr
from
    '{IN_FILE_PATH}' as t
where
    lower(item_name) like '%{dish_}%' and
    lower(city) like '%{city_}%' and
    best_seller != 'None'
group by
    1,2,3,4,5
order by 
    2 desc
    """
    
    res = duckdb.sql(query).fetchall()

    # generate JSON
    out = []
    for row in res:
        parsed_row = {
            'restaurant': row[0],
            'rating': row[1],
            'cuisine': row[2],
            'place_name': row[3],
            'city': row[4],
            'menu': []
        }

        # fill menu
        ind = 0
        while ind < len(row[5]):
            menu_item_dict = {
                'item': row[5][ind],
                'votes': row[6][ind],
                'price_inr': row[7][ind]
            }
            parsed_row['menu'].append(menu_item_dict)
            ind = ind + 1

        out.append(parsed_row)

    pprint.pprint(out)

    return out

if __name__ == '__main__':
    get_dish_details('fish', 'hyderabad')