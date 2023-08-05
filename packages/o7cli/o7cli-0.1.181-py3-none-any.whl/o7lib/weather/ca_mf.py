#!/usr/bin/python
#************************************************************************
# Copyright 2021 O7 Conseils inc (Philippe Gosselin)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#************************************************************************


#--------------------------------
#
#--------------------------------
import pprint
import xml.etree.ElementTree as ET
# https://docs.python.org/3/library/xml.etree.elementtree.html
import logging
import requests


#*************************************************
#  Canadian Marine Forecast
#
# https://meteo.gc.ca/mainmenu/marine_menu_f.html
#
#
#
#*************************************************

# create logger
logger = logging.getLogger('ca_maritime')
logger.setLevel(logging.DEBUG)


#*************************************************
#
# https://meteo.gc.ca/marine/region_f.html?mapID=12
#
#*************************************************
def GetForecast(siteId = 23100):
    """Get Marine Forecast for Site Id"""

    logger.info(f'GetForecast for site id: {siteId}')

    # Get forecast
    r = requests.get(f'https://meteo.gc.ca/rss/marine/{siteId}_f.xml')

    #print(f'Results --> \n{r.text}')
    root = ET.fromstring(r.text)
    #print(f'root.tag --> {root.tag}')

    # Get Namespace
    #ns = {'ns': 'http://www.w3.org/2005/Atom'}
    ns = None
    ns_found = root.tag.split('}')[0].strip('{')
    if len(ns_found) > 0:  ns = {'ns': ns_found}
    #print(f'namespace --> {ns}')

    ret = []


    for entry in root.findall('.//ns:entry', ns):

        title = entry.find(f".//ns:title",ns).text
        summary = entry.find(f".//ns:summary",ns).text

        ret.append({
            "title" : title,
            "summary" : summary
        })

    return ret

#*************************************************
#
#*************************************************
if __name__ == "__main__":

    forecast = GetForecast()
    pprint.pprint(forecast)