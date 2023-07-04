import re
import scrapy

class BraveSearchSpider(scrapy.Spider):
    name = "brave_search"
    
    def start_requests(self):
        search_query = "captain nepali"
        url = f"https://search.brave.com/search?q={search_query}+imdb"
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        infobox = response.css('div#infobox')
        
        movie_name = infobox.css('.infobox-title::text').get().strip()
        director = infobox.css('span.infobox-attr-name:contains("Directed by") + span.attr-value::text').get(default='').strip()
        # Extract the year using regular expressions
        description = response.css('div.body > div.mb-6::text').get().strip()
        year_match = re.search(r'(\d{4})', description)
        year = year_match.group(1) if year_match else None
        thumbnail = infobox.css('.infobox-thumbnail .thumb::attr(style)').re_first(r"url\((.*?)\)")
        # Extract the first sentence from the description
        first_sentence_match = re.match(r'^([^\.!?]+[\.!?])', description)
        first_sentence = first_sentence_match.group(1).strip() if first_sentence_match else ""
        imdb_rating = infobox.css('.r-num::text').get().strip()
        
        
        data = {
            "Movie Name": movie_name,
            "Directed By": director,
            "Year": year,
            "Thumbnail": thumbnail,
            "Description": first_sentence,
            "IMDb Rating": imdb_rating,
        }
        
        yield data
