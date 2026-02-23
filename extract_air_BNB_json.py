import json
from pydantic import BaseModel
from typing import Dict,List,Any

class Airbnb(BaseModel):
    Baner_Name: str
    Baner_Id: int
    Basic_information: Dict[str, Any]
    Location: Dict[str, str]
    allAmenities: Dict[str, List[str]]
    images: List[Dict[str, str]]
    Host_Details: Dict[str, Any]

Base_path = r'C:\Users\hemanshu.marwadi\Desktop\Air_BNB\air_bnb_.json'

def read_json_data(filename):
    with open(filename, 'rb') as json_file:
        json_data = json.loads(json_file.read().decode())
        return json_data


def find_first_embed_name(json_data):
    basic_info = dict()
    for item in json_data.get("niobeClientData", []):
        if isinstance(item, list):
            for element in item:
                if isinstance(element, dict):
                    root_path = element.get('data',{}).get('presentation',{}).get('stayProductDetailPage',{}).get('sections',{})
                    for i in root_path['sections']:
                        if i['section'] is not None:
                            info = i.get('section').get('shareSave',{}).get('embedData',{})
                            base = i.get('section',{})
                            # print(base.get('__typename'))
                            if base.get('__typename') == 'LocationSection':
                                full_adress = base.get('subtitle')
                                basic_info['Location'] = {
                                    'Address': full_adress
                                }




                            if info:
                                basic_info['Baner_Name'] = info.get('name')
                                basic_info['Baner_Id'] = info.get('id')
                                basic_info['Basic_information'] = {
                                    'PropertyType' : info.get('propertyType'),
                                    'Max_guests_Capacity' : info.get('personCapacity'),
                                    'Review' : info.get('reviewCount'),
                                    'Rating' : info.get('starRating')
                                }

                            amenity_groups = i.get('section').get("seeAllAmenitiesGroups", []) + i.get('section').get("previewAmenitiesGroups", [])


                            if amenity_groups:
                                basic_info["allAmenities"] = {}

                                for group in amenity_groups:
                                    if isinstance(group, dict):
                                        category = group.get("title")
                                        amenities_list = group.get("amenities", [])

                                        if category and isinstance(amenities_list, list):
                                            basic_info["allAmenities"][category] = []

                                            for amenity in amenities_list:
                                                if isinstance(amenity, dict):
                                                    title = amenity.get("title")
                                                    if title:
                                                        basic_info["allAmenities"][category].append(title)

                            media_items = i.get('section').get("mediaItems", [])

                            if isinstance(media_items, list):
                                basic_info.setdefault("images", [])

                                for media in media_items:
                                    if isinstance(media, dict):
                                        label = media.get("accessibilityLabel")
                                        url = media.get("baseUrl")

                                        if url:
                                            basic_info["images"].append({
                                                "label": label,
                                                "url": url
                                            })
                            if base.get("__typename") == "MeetYourHostSection":

                                basic_info["host"] = {}
                                basic_info["host"]["about"] = {}

                                card = base.get("cardData", {})

                                basic_info["host"]["name"] = card.get("name")
                                basic_info["host"]["rating"] = card.get("ratingAverage")
                                basic_info["host"]["review_count"] = card.get("ratingCount")

                                years = card.get("timeAsHost", {}).get("years")
                                if years:
                                    basic_info["host"]["hosting_year"] = f"{years} year"

                                for host_info in base.get("hostHighlights", []):
                                    title = host_info.get("title", "")

                                    if "My work:" in title:
                                        basic_info["host"]["about"]["work"] = title.replace("My work:", "").strip()

                                    elif "Fun fact:" in title:
                                        basic_info["host"]["about"]["fun_fact"] = title.replace("Fun fact:", "").strip()

                                    elif "For guests, I always:" in title:
                                        basic_info["host"]["about"]["for_guests"] = title.replace("For guests, I always:","").strip()

                                    elif "Pets:" in title:
                                        basic_info["host"]["about"]["pets"] = title.replace("Pets:", "").strip()

                    ordered_info = {}
                    ordered_info["Baner_Name"] = basic_info.get("Baner_Name")
                    ordered_info["Baner_Id"] = basic_info.get("Baner_Id")
                    ordered_info["Basic_information"] = basic_info.get("Basic_information")
                    ordered_info["Location"] = basic_info.get("Location")
                    ordered_info["allAmenities"] = basic_info.get("allAmenities")
                    ordered_info["images"] = basic_info.get("images")
                    ordered_info['Host_Details'] = basic_info.get('host')

                    return ordered_info

def convert_json_file(data):
    with open("air_bnb_data.json", "w") as files:
        json.dump(data, files, indent=4)







data = read_json_data(Base_path)
name = find_first_embed_name(data)

validated = Airbnb.model_validate(name)
va = validated.model_dump()
convert_json_file(va)

