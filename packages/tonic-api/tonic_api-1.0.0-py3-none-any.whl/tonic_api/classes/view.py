class View:
    def __init__(self, id, view_json):
        self.id = id
        self.name = view_json['name']
        self.query = view_json['query']
        self.parameters = view_json['nnModelConfig']
        self.encodings = view_json['columnEncodings']

    def describe(self):
        print("View: " + self.name + " [" + self.id + "]")
        print("View Query: " + self.query)
        print("View Model Parameters: " + str(self.parameters))
        print("View Column Encodings: " + str(self.encodings))
