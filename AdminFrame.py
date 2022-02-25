import html
import os
from os.path import exists
import re
import xml.etree.ElementTree as XMLTree
from typing import List
from flask import Flask, redirect
import config

# Variables
comicCollection: List
comicCollectorDataPath: str = config.comicFilePath
sourcePath: str = config.sourceImagePath
ip: str
displayImageFilter = ("all", "all")
filterList = [("Series Group", "seriesgroup", []),
              ("Series", "series", []),
              ("Creators", "creators", []),
              ("Publishers", "publishers", []),
              ("Comic Age", "age", []),
              ("Grading Company", "gradingcompany", []),
              ("Location", "location", [])]

webpageEnd: str = '''
 </div>
<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" ''' \
 + '''integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" ''' \
 + '''crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" ''' \
 + '''integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" ''' \
 + '''crossorigin="anonymous"></script>
<!-- JavaScript Bundle with Popper -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
<script>
    function searchBarFilter() {
        var input, filter, ul, li, a, i, txtValue;
        input = document.getElementById("myInput");
        filter = input.value.toUpperCase();
        ul = document.getElementById("myUL");
        li = ul.getElementsByTagName("li");
        for (i = 0; i < li.length; i++) {
            a = li[i].getElementsByTagName("a")[0];
            txtValue = a.textContent || a.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                li[i].style.display = "";
            } else {
                li[i].style.display = "none";
            }
        }
    }
</script>
</body>
'''

# webpageBody is the main template for the http served webpage. This is where you can make that page..prettier
webpageBody: str = '''
<!doctype html>
<html lang='en'>
<head><title>Comic Frame Filters</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- CSS only -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
<link href="style.css" rel="stylesheet">
</head>
<body class='bg-secondary'>
<div class='container-sm'>
'''

webpage = webpageBody


def find(search_list, search_string):
    for row in search_list:
        if row[1] == search_string:
            return row
    return ["All", "all", []]


def build_index_links():
    index_page = '''<h1 class='text-primary'>Comic Frame Filter</h1>'''
    index_page += '<h2 class=\'text-primary\'>Current Image Filter</h2>' + \
                  '<h3 class=\'text-primary\'>Category: <b>' + find(filterList, displayImageFilter[0])[0] + '</b></h3>' + \
                  '<h3 class=\'text-primary\'>Value: <b>' + displayImageFilter[1] + '</b></h3>'
    index_page += '''<ul class='list-group'>'''
    for filterItem in filterList:
        index_page += "<li class='list-group-item'><a class='btn btn-primary mw-100 w-100' " + \
                     "href='" + filterItem[1] + "'>" + filterItem[0] + "</a></li>"
    index_page += '''<li class='list-group-item'><a class='btn btn-primary mw-100 w-100' ''' + \
                  '''href='resetFilter'>Reset Filter</a></li>'''
    index_page += '''<li class='list-group-item'><a class='btn btn-primary mw-100 w-100' ''' + \
                  '''href='rebuildFilter'>Rebuild Filter</a></li>'''
    index_page += '</ul>'
    return index_page


def build_webpage_links(selected_filter):
    links = '''<input type="text" class="form-control" id="myInput" onkeyup="searchBarFilter()" ''' \
            + '''placeholder="Search for filters..">'''
    links = "<h1>" + find(filterList, selected_filter)[0] + "</h1><ul id='myUL' class='list-group'>" + links
    selected_filter_list = find(filterList, selected_filter)
    for filter_item in selected_filter_list[2]:
        links += "<li class='list-group-item'><a class='btn btn-primary mw-100 w-100'  href='" \
                + selected_filter_list[1] + "/" + html.escape(filter_item) + "'>" + filter_item + "</a></li>"
    links += "</ul>"
    return links


def refresh_display_file(image_filter):
    global comicCollection
    comicCollection = get_comic_collection()
    file_text = ""
    if image_filter[0] == "all":
        for comic in comicCollection:
            if "coverfront" in comic and exists(os.getcwd() + "/" + config.sourceImagePath + "/" + comic['coverfront']):
                file_text += os.getcwd() + "/" + config.sourceImagePath + "/" + comic['coverfront'] + '\n'
    else:
        for comic in comicCollection:
            if str(comic.get(image_filter[0])) == image_filter[1]:
                if "coverfront" in comic and exists(os.getcwd() + "/" + config.sourceImagePath + "/" + comic['coverfront']):
                    file_text += os.getcwd() + "/" + config.sourceImagePath + "/" + comic['coverfront'] + '\n'
    f = open(config.imageFilePath, 'w')
    f.write(file_text)
    f.close()


def get_comic_collection() -> list:
    collection_xml = XMLTree.parse(config.comicFilePath)
    collection_array = []
    for comic in collection_xml.findall("./comiclist/"):
        comic_info = {}
        for info in comic.findall("*"):
            if info.tag == "allcreators":
                comic_info["creators"] = info.text
            elif info.tag == "coverfront":
                comic_info["coverfront"] = os.path.split(info.text)[1]
            elif info.tag == "publisher":
                comic_info["publisher"] = info.find("displayname").text
            elif info.tag == "age":
                comic_info["age"] = info.find("displayname").text
            elif info.tag == "seriesgroup":
                comic_info["seriesgroup"] = info.find("displayname").text
            elif info.tag == "mainsection":
                comic_info["series"] = info.find("series/displayname").text
            elif info.tag == "gradingcompany":
                comic_info["gradingcompany"] = info.find("displayname").text
            elif info.tag == "location":
                comic_info["location"] = info.find("displayname").text.replace("#", '')

        collection_array.append(comic_info)
    return collection_array


def get_display_filters(comic_collection: list):
    for comic in comic_collection:
        for filter_item, value in comic.items():
            if filter_item == "series":
                if value not in filterList[1][2]:
                    filterList[1][2].append(value)
            elif filter_item == "seriesgroup":
                if value not in filterList[0][2]:
                    filterList[0][2].append(value)
            elif filter_item == "publisher":
                if value not in filterList[3][2]:
                    filterList[3][2].append(value)
            elif filter_item == "age":
                if value not in filterList[4][2]:
                    filterList[4][2].append(value)
            elif filter_item == "creators":
                for creator in value.split(";"):
                    if creator.strip() not in filterList[2][2]:
                        filterList[2][2].append(creator.strip())
            elif filter_item == "gradingcompany":
                if value not in filterList[5][2]:
                    filterList[5][2].append(value)
            elif filter_item == "location":
                if value not in filterList[6][2]:
                    filterList[6][2].append(value)
    filterList[0][2].sort()
    filterList[1][2].sort()
    filterList[2][2].sort()
    filterList[3][2].sort()
    filterList[4][2].sort()
    filterList[5][2].sort()
    filterList[6][2].sort(key=natural_keys)


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def main():
    # Get Comic Collection
    global comicCollection
    comicCollection = get_comic_collection()
    get_display_filters(comicCollection)

    global displayImageFilter
    refresh_display_file(displayImageFilter)

    # Start Web Page
    app = Flask(__name__)

    @app.route('/')
    def index():
        return webpage + build_index_links() + webpageEnd

    @app.route('/<newfilter>')
    def display_filter(newfilter):
        global comicCollection
        comicCollection = get_comic_collection()
        get_display_filters(comicCollection)
        return webpage + build_webpage_links(newfilter) + webpageEnd

    @app.route('/<newfilter>/<value>')
    def series_filter(newfilter, value):
        global displayImageFilter
        displayImageFilter = (newfilter, html.unescape(value))
        refresh_display_file(displayImageFilter)
        return redirect('/', )

    @app.route('/resetFilter')
    def reset_filter():
        global displayImageFilter
        displayImageFilter = ("all", "all")
        refresh_display_file(displayImageFilter)
        return redirect('/', )

    @app.route('/rebuildFilter')
    def rebuild_filter():
        global displayImageFilter
        refresh_display_file(displayImageFilter)
        return redirect('/')

    @app.route('/debug')
    def debug_route():
        global displayImageFilter
        print("displayImage:")
        print(displayImageFilter)
        global filterList
        print("locations:")
        print(filterList[6][2])
        return webpage

    app.run(debug=True, host='0.0.0.0')


if __name__ == "__main__":
    main()
