import requests
import time 
import re 

URL = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/skins.json"
KNIFE_WEAR_FALLBACKS = ["Field-Tested", "Minimal Wear", "Factory New"]
GUN_WEAR_FALLBACKS = ["Battle-Scarred", "Well-Worn"]


def normalize_name(name):
    name = name.lower().strip()
    name = name.replace('-', '')
    name = name.replace('|', ' ')
    while '  ' in name:
        name = name.replace('  ', ' ')
    return name

def load_skins():
    return requests.get(URL).json()


def search_skins(query):
    skins = load_skins()
    q = normalize_name(query)
    results = []
    for skin in skins:
        if q in normalize_name(skin.get('name', '')):
            results.append(skin)
    return results

def get_collections_by_partial_name(query):
    q = normalize_name(query)
    skins = load_skins()
    matches = []
    for skin in skins:
        if q in normalize_name(skin.get('name', '')):
            combined = []
            combined += skin.get('collections', [])
            combined += skin.get('cases', [])
            combined += skin.get('crates', [])
            combined += skin.get('containers', [])
            matches.append({'skin': skin.get('name'), 'sources': combined})

    return matches if matches else None


def normalize_rarity(r):
    if isinstance(r, dict):
        return (r.get("name") or "").strip().lower()
    return str(r or "").strip().lower()

def get_covert_skins_in_collections(collection_list):
    targets = {str(c).strip().lower() for c in collection_list}

    skins = load_skins()
    results = []

    for skin in skins:
        if normalize_rarity(skin.get("rarity")) != "covert":
            continue

        combined_sources = []
        combined_sources += skin.get('collections', [])
        combined_sources += skin.get('cases', [])
        combined_sources += skin.get('crates', [])
        combined_sources += skin.get('containers', [])

        for source in combined_sources:
            if isinstance(source, dict):
                s_name = source.get('name')
            else:
                s_name = str(source)
            
            if s_name and s_name.strip().lower() in targets:
                results.append(skin.get("name"))
                break 

    return list(set(results)) 


def get_item_price(item_name):
    url = "https://steamcommunity.com/market/priceoverview/"

    params = {
        "country": "US",
        "currency": 1, 
        "appid": 730, 
        "market_hash_name": item_name
    }

    headers = {"User-Agent": "Mozilla/5.0"}
    time.sleep(1) 
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception:
        return "ERROR"

    if data.get("success"):
        lowest_price = data.get("lowest_price", "N/A")
        return lowest_price.replace('$', '').strip() if lowest_price else "N/A"
    else:
        return "N/A"

def get_steam_market_price(skin_name, wear_fallbacks=None):

    if wear_fallbacks:
        for wear in wear_fallbacks:
            market_name = f"{skin_name} ({wear})"
        
            
            price = get_item_price(market_name)
            
            if price not in ["N/A", "ERROR"]:
                return f"{price} ({wear})" 
        
        wears_str = ", ".join(wear_fallbacks)
        return f"N/A (Checked: {wears_str})"
            
    return "N/A (Wear State List Missing)" 

def get_numerical_price(price_string):
    match = re.search(r'\d+\.?\d*', price_string)
    if match:
        try:
            return float(match.group(0))
        except ValueError:
            return float('inf') 
    return float('inf')


if __name__ == "__main__":
    
    name = input("Input the knife name: ")
    
    all_matched_skins = search_skins(name)
    input_skin_name = next((s.get('name') for s in all_matched_skins 
                            if '★' in s.get('name', '') or 'Glove Case' in s.get('name', '')), None)

    collections = get_collections_by_partial_name(name)
    
    if not collections:
        print(f"No skins found matching '{name}'.")
    else:
        names12 = []
        for item in collections:
            cols = item.get('sources', [])
            if not cols:
                continue
            for col in cols:
                if isinstance(col, dict) and 'name' in col:
                    cname = col['name']
                else:
                    cname = str(col)
                if cname not in names12:
                    names12.append(cname)
        
        result = get_covert_skins_in_collections(names12)

        knife_list = []
        other_covert_skins = []

        for s in result:
            if '★' in s or 'Glove Case' in s:
                if s == input_skin_name:
                    knife_list.append(s)
            else:
                other_covert_skins.append(s)
        
        all_knives_in_collection = [s for s in result if '★' in s or 'Glove Case' in s]
        
        if not knife_list and input_skin_name:
            knife_list.append(input_skin_name)
        
        def print_skins_with_prices(title, skin_list, wear_fallbacks=None): 
            priced_skins = []
            numerical_prices = []
            
            for s_name in skin_list:
                price_string = get_steam_market_price(s_name, wear_fallbacks=wear_fallbacks) 
                
                num_price = get_numerical_price(price_string)
                if num_price != float('inf'):
                    numerical_prices.append(num_price)
                    
                priced_skins.append((s_name, price_string))
                print(f"FINAL price for {s_name}: {price_string}") 

                
            print("---------------------")
            
            return priced_skins, numerical_prices

        print("\n--- KNIFE PRICE ---")
        knife_priced_list, knife_prices = print_skins_with_prices("Input Knife", knife_list, wear_fallbacks=KNIFE_WEAR_FALLBACKS)
        gun_priced_list, gun_prices = print_skins_with_prices("Other Covert Skins (Guns/Rifles)", other_covert_skins, wear_fallbacks=GUN_WEAR_FALLBACKS)
        
        
        #Final Calculations
        
        print("\n" + "="*50)
        print("FINAL CALCULATION")
        total_cost = 0.0
        cheapest_price = 0.0
        cheapest_skin = "N/A"

        if gun_prices:
            cheapest_price = min(gun_prices)
            total_cost = cheapest_price * 5
            cheapest_skin = next((name for name, price_str in gun_priced_list 
                                  if get_numerical_price(price_str) == cheapest_price), "N/A")
            print(f"  Lowest Price: **${cheapest_price:.2f}** ({cheapest_skin})")
            print(f"  Total Cost (x5) of the trade-up: **${total_cost:.2f}**")
        else:
            print("\n**ERROR**: No valid numerical prices found for 'Other Covert Skins'. Cannot perform cost calculation.")

        # 5.2 Determine Knife Price and Possible Profit
        knife_price_float = 0.0
        possible_profit = "N/A"
        
        if knife_prices:
            knife_price_float = knife_prices[0] # The list only contains one price for the input knife
            possible_profit = knife_price_float - total_cost
            
            print(f"\nInput Knife Price: **${knife_price_float:.2f}**")
            print(f"Possible Profit (Knife Price - Total Cost): **${possible_profit:.2f}**")
        else:
            print("\n**ERROR**: No valid price found for the input knife. Cannot perform profit calculation.")

        odds_fraction = f"1/{len(all_knives_in_collection)}"
        
        if len(all_knives_in_collection) > 0:
            odds_percentage = (1 / len(all_knives_in_collection)) * 100
            print(f"\nPossibility of getting the desired knife from the trade-up:")
            print(f"  Fraction: **{odds_fraction}**")
            print(f"  Percentage: **{odds_percentage:.2f}%**")
            print(f"\nNote: This is the chance of getting that *specific* knife you entered") 
        else:
            print("\n**ERROR**: Cannot calculate odds. The input knife was not found in any collection to determine the total number of knives.")
            
        print("="*50)