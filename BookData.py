class BookData:
    def __init__(self, rawXml, date):
        self.date = date
        self.title = rawXml['book']['title_without_series']
        self.numPages = rawXml['book']['num_pages']
        self.imageUrl = rawXml['book']['image_url']
        self.coverColor = 'White'
        self.accentColor = '#000000'

    def to_json(self):
        return {
            'Title': self.title,
            'Date': self.date,
            'NumPages': self.numPages,
            'ImageUrl': self.imageUrl,
            'CoverColor': self.coverColor,
            'AccentColor': self.accentColor
        }

    def set_accent_color(self, accentColor):
        self.accentColor = "#" + accentColor