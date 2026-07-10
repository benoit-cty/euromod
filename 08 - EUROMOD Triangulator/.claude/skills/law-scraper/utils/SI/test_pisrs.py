import httpx
from bs4 import BeautifulSoup
import re

# pisrs.si looks like a modern angular SPA.
# Usually SPAs make API calls. Let's see if we can find an API url in the network or if we can use playwright.
# Or wait, there is an open data portal for pisrs?

# Wait, `https://pisrs.si/Pis.web/pregledPredpisa?id=ZAKO213` loaded perfectly in the batch scraper.
# The batch scraper used `clean_html` which found `soup.get_text()`. Let's look at what we downloaded.
