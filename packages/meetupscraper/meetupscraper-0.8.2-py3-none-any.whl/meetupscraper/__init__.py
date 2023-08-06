import urllib.parse
import logging
import dataclasses
import datetime
import json

import dateutil.parser
import lxml.html
import requests


LOGGER = logging.getLogger("meetupscraper")
# logging.basicConfig(level='DEBUG')


@dataclasses.dataclass(frozen=True)
class Venue:
    name: str
    street: str


@dataclasses.dataclass(frozen=True)
class Event:
    url: str
    date: datetime.datetime
    title: str
    venue: Venue


def _get_venue(html):
    h = lxml.html.fromstring(html)

    try:
        j = json.loads(h.xpath('//script [@id="__NEXT_DATA__"]')[0].text)
        venue = j["props"]["pageProps"]["event"]["venue"]
        return Venue(name=venue["name"], street=venue["address"])
    except (KeyError, IndexError):
        pass

    try:
        street = h.xpath('//* [@data-testid="location-info"]/text()')[0]
    except IndexError:
        try:
            street = h.xpath(
                '//* [@class="venueDisplay-venue-address '
                'text--secondary text--small text--wrapNice"]/text()'
            )[0]
        except IndexError:
            street = ""
    street = street.split(" · ")[0]
    try:
        venue_name = h.xpath(
            '//* [@data-event-label="event-location"]/text()'
        )[0]
    except IndexError:
        try:
            venue_name = h.xpath(
                '//* [@class="wrap--singleLine--truncate"]/text()'
            )[0]
        except IndexError:
            try:
                venue_name = h.xpath(
                    '//* [@data-testid="venue-name-value"]/text()'
                )[0]
            except IndexError:
                # with open('/tmp/fail.txt', 'w') as f:
                #    f.write(html)
                LOGGER.debug("html=%r", html)
                raise
    return Venue(
        name=venue_name,
        street=street,
    )


def get_upcoming_events(meetup_name):
    prefix = "https://www.meetup.com/" + urllib.parse.quote(meetup_name)
    url = prefix + "/events/"
    LOGGER.info("Looking up %r", url)
    r = requests.get(url)
    h = lxml.html.fromstring(r.text)

    timestamps = []
    for item in h.xpath('//a [@class="eventCardHead--title"]'):
        meetup_url = urllib.parse.urljoin(
            "https://meetup.com", item.get("href")
        )
        title = item.text
        date_s = int(item.xpath("../..//* [@datetime]/@datetime")[0]) / 1000
        date = datetime.datetime.fromtimestamp(date_s)
        now = datetime.datetime.today()
        if date < now:
            date = date.replace(year=date.year + 1)
        LOGGER.info("Looking up %r", meetup_url)
        yield Event(
            title=title,
            date=date,
            url=meetup_url,
            venue=_get_venue(requests.get(meetup_url).text),
        )
