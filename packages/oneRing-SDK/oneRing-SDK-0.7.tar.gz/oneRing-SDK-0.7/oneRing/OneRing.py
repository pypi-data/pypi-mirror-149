import requests

class Client(object):

    BASE_URL = "https://the-one-api.dev/v2/"
    g_apiKey = ""

    def __init__(self, apiKey):
        self.g_apiKey = apiKey

    def __makeRequest(self, **kwargs):

        if "path" in kwargs:
            path = kwargs['path']

        # { param -> { operator : "!=<>", "value" : "100"}}

        if "options" in kwargs:
            options = kwargs['options']
            if options:
                queryParams = ""
                for param in options:
                    if param != 'sort':
                        queryParams += param + options[param]['operator'] + options[param]['value'] + "&"
                    else:
                        queryParams += 'sort=' + options['sort']['criteria'] + ':' + options['sort']['order']
                path += '?' + queryParams[:-1]

        if "authenticate" in kwargs:
            headers = {'Authorization':"Bearer " + self.g_apiKey} if kwargs['authenticate'] else {}
            return requests.get(self.BASE_URL + path, headers=headers).json()



    # Book functions:

    def getAllBooks(self, options_dict=None):
        return self.__makeRequest(path="book", authenticate=False, options=options_dict)

    def getBookById(self, book_id):
        return self.getAllBooks({"_id": { "operator": "=", "value": book_id}})

    def getBookByName(self, book_name):
        return self.getAllBooks({"name": { "operator": "=", "value": book_name}})



    # Chapter functions

    def getAllChapters(self, options_dict=None):
        return self.__makeRequest(path="chapter", authenticate=True, options=options_dict)

    def getAllChaptersOfBook(self, book_id):
        return self.__makeRequest(path="book/" + book_id + "/chapter", authenticate=False)

    def getChapterById(self, chapter_id):
        return self.getAllChapters({"_id": { "operator": "=", "value": chapter_id}})

    def getChapterByName(self, chapter_name):
        return self.getAllChapters({"chapterName": { "operator": "=", "value": chapter_name}})



    # Movie functions:

    def getAllMovies(self, options_dict=None):
        return self.__makeRequest(path="movie", authenticate=True, options=options_dict)

    def getMovieById(self, movie_id):
        return self.getAllMovies({"_id": { "operator": "=", "value": movie_id}})

    def getMovieByName(self, movie_name):
        return self.getAllMovies({"name": { "operator": "=", "value": movie_name}})



    # Character functions:

    def getAllCharacters(self, options_dict=None):
        return self.__makeRequest(path="character", authenticate=True, options=options_dict)

    def getCharacterQuotes(self, character_id):
        return self.__makeRequest(path="character/" + character_id + "/quote", authenticate=True)

    def getCharacterById(self, character_id):
        return self.getAllCharacters({"_id": { "operator": "=", "value": character_id }})

    def getCharactersByName(self, character_name):
        return self.getAllCharacters({"name": { "operator": "=", "value": character_name}})



    # Quote functions:

    def getAllQuotes(self, options_dict=None):
        return self.__makeRequest(path="quote", authenticate=True, options=options_dict)

    def getQuoteById(self, quote_id):
        return self.getAllQuotes({"_id": {'operator': '=', 'value': quote_id}})