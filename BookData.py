class BookData:
    def __init__(self, rawXml, date):
        self.date = date
        self.title = rawXml['book']['title_without_series']
        self.numPages = rawXml['book']['num_pages']
        self.imageUrl = rawXml['book']['image_url']
        self.colors = None

    def to_json(self):
        return {
            'Title': self.title,
            'Date': self.date,
            'NumPages': self.numPages,
            'ImageUrl': self.imageUrl,
            'Colors': self.colors
        }