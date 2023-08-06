"""
.. include:: ../../docs-readme.md
"""

import requests

API_KEY = None
SERVER_URL = "https://goflike.app/api"
VERSION = "v0"

class FlikeException(Exception):
    """Exception raised by Flike API.

    Attributes
    ----------
    status : str
        status code of the error (HTTP error code)
    message : str
        explanation of the error
    """

    def __init__(self, response: requests.Response):
        self.status = response.status_code
        self.message = response.text
        super().__init__(f'{response.status_code} - {response.text}')

class Recommendation:
    """Recommendation of a content item for a user

    Attributes
    ----------
    item_id : str
        Unique identifier of the content item being recommended
    probability : str
        Probability of a user 'liking' the recommended item
    """

    def __init__(self, item_id:str, probability:float):
        self.item_id = item_id
        self.probability = probability

    def __str__(self):
        return f'{self.item_id} ({self.probability})'

class RecommendationsResponse:
    """Response to a recommendation request.

    Attributes
    ----------
    items : str
        Recommendations for a user
    correlation_id : str
        Unique identifier of the content item being recommended
    """

    def __init__(self, items:list[Recommendation], correlation_id:str):
        self.items = items
        self.correlation_id = correlation_id

    def __str__(self):
        return f'{self.correlation_id} ({self.items})'

def inititialize(api_key: str, server_url:str = None, version:str=None):
    """Initialize the recommender.

    Parameters
    ----------
    api_key : str
        Your API Key
    server_url : str (optional)
        This is only used for internal testing
    version : str (optional)
        Version of the API to use
    """

    global API_KEY
    global SERVER_URL
    global VERSION

    API_KEY = api_key
    if server_url is not None:
        SERVER_URL = server_url
    if version is not None:
        VERSION = version

def start(user_id: str, item_id:str, correlation_id:str):
    """Registers a user starting to consume/interact with a content item..

    Parameters
    ----------
    user_id : str
        The unique identifier of the user
    item_id : str
        The unique identifier of the 
    corellation_id
        The unique identifier of a recommendation
    """

    response = requests.push(f'{SERVER_URL}/{VERSION}/recommender/start', params={'user_id':user_id, 'item_id':item_id},headers={'x-api-key': API_KEY})
    if(response.status_code != 200):
        raise FlikeException(response)

def like(user_id: str, item_id:str):
    """Registers a user-started item as 'liked' by the user.
    'Like' refers to any action indicating that a user likes the content item.
    E.g. for a video, this could be a user watching more than 85% of the video.

    Parameters
    ----------
    user_id : str
        The unique identifier of the user
    item_id : str
        The unique identifier of the content item
    """

    response = requests.push(f'{SERVER_URL}/{VERSION}/recommender/like', params={'user_id':user_id, 'item_id':item_id},headers={'x-api-key': API_KEY})
    if(response.status_code != 200):
        raise FlikeException(response)

def dislike(user_id: str, item_id:str):
    """Registers a user-started item as 'disliked' by the user.
    'Dislike' refers to any action indicating that a user dislikes the content item.
    E.g. for a video, this could be a user only watching 5% of the video and not finishing it.

    Parameters
    ----------
    user_id : str
        The unique identifier of the user
    item_id : str
        The unique identifier of the content item
    """

    response = requests.push(f'{SERVER_URL}/{VERSION}/recommender/dislike', params={'user_id':user_id, 'item_id':item_id},headers={'x-api-key': API_KEY})
    if(response.status_code != 200):
        raise FlikeException(response)


def recommend(user_id: str, num_item:int):
    """Get an array of content items that a user is probable to consume/buy/subscribe/like or similar.
    Recommendations are sorted by descending probability of a user 'liking' them.

    Parameters
    ----------
    user_id : str
        The unique identifier of the user
    num_item : str
        Number of content items that should be suggested
    """

    response = requests.get(f'{SERVER_URL}/{VERSION}/recommender/recommend', params={'user_id':user_id, 'num_items':num_item},headers={'x-api-key': API_KEY})
    if(response.status_code != 200):
        raise FlikeException(response)
    return response.json()['recommendations']
