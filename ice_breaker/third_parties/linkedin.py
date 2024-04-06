import os
import bs4
import requests
import json


def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles
    Manually scrape the information from the LinkedIn profile
    Args:
        linkedin_profile_url (str): url
    """
    api_key = os.environ["PROXYCURL_API_KEY"]
    headers = {"Authorization": "Bearer " + api_key}
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"


    response = requests.get(
        api_endpoint, params={"url": linkedin_profile_url}, headers=headers
    ).json()
    data = [
        "full_name",
        "profile_pic_url",
        "occupation",
        "headline",
        "follower_count",
        "summary",
        "country_full_name",
        "city",
        "experiences",
        "education",
        "accomplishment_honors_awards",
        "certifications",
    ]
    response = {k: v for k, v in response.items() if k in data}

    return response

# def scrape_linkedin_profile(linkedin_profile_url: str):
#     """scrape information from LinkedIn profiles
#     Manually scrape the information from the LinkedIn profile
#     Args:
#         linkedin_profile_url (str): url
#     """
#     response = requests.get(
#         "https://gist.githubusercontent.com/marioToribi0/c2337d4a0c91d65a3047fcfc335bd922/raw/18381b2e9633ef174426341e1460bd7fa88ef181/mario-toribio.json"
#     )
#     response = response._content
#     response = json.loads(response)
#     data = [
#         "full_name",
#         "profile_pic_url",
#         "occupation",
#         "headline",
#         "follower_count",
#         "summary",
#         "country_full_name",
#         "city",
#         "experiences",
#         "education",
#         "accomplishment_honors_awards",
#         "certifications",
#     ]
#     response = {k: v for k, v in response.items() if k in data}

#     return response


# if __name__ == "__main__":
#     print(scrape_linkedin_profile("")["profile_pic_url"])
