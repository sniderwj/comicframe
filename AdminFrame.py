import os
import xml.etree.ElementTree as ET
import config
from flask import Flask, redirect
import html

# Variables

comicCollectorDataPath: str = config.comicFilePath
sourcePath: str = config.sourceImagePath
ip: str
displayImageFilter = ("all", "all")
seriesFilter = []
publisherFilter = []
ageFilter = []
creatorsFilter = []
comicCollection = []
seriesGroupFilter = []

webpageEnd: str = '''
</div>
<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" ''' \
                  + '''integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" ''' \
                  + '''crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" ''' \
                  + '''integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" ''' \
                  + '''crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" ''' \
                  + '''integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" ''' \
                  + '''crossorigin="anonymous"></script>
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
<link rel='stylesheet'  href='static/css/bootstrap.min.css' />
</head>
<body>

<div class='container-sm'>
  
'''

webpage = webpageBody


def build_index_links():
    indexpage = '''<h1 class='text-white'>Comic Frame Filter</h1>'''
    indexpage += '<h2 class=\'text-white\'>Current Image Filter</h2>' + \
                 '<h3 class=\'text-white\'>Category: <b>' + displayImageFilter[0].capitalize() + '</b></h3>' + \
                 '<h3 class=\'text-white\'>Value: <b>' + displayImageFilter[1] + '</b></h3>'
    indexpage += '''<ul class='list-group'>'''
    indexpage += '''<li class='list-group-item'><a class='btn btn-primary mw-100 w-100' ''' + \
                 '''href='seriesgroup'>Series Group</a></li>'''
    indexpage += '''<li class='list-group-item'><a class='btn btn-primary mw-100 w-100' ''' + \
                 '''href='series'>Series</a></li>'''
    indexpage += '''<li class='list-group-item'><a class='btn btn-primary mw-100 w-100' ''' + \
                 '''href='creators'>Creators</a></li>'''
    indexpage += '''<li class='list-group-item'><a class='btn btn-primary mw-100 w-100' ''' + \
                 '''href='publisher'>Publishers</a></li>'''
    indexpage += '''<li class='list-group-item'><a class='btn btn-primary mw-100 w-100' ''' + \
                 '''href='age'>Comic Age</a></li>'''
    indexpage += '''<li class='list-group-item'><a class='btn btn-primary mw-100 w-100' ''' + \
                 '''href='resetFilter'>Reset Filter</a></li>'''
    indexpage += '</ul>'

    return indexpage


def build_webpage_links(selected_filter):
    links = '''<input type="text" class="form-control" id="myInput" onkeyup="searchBarFilter()" ''' \
            + '''placeholder="Search for filters..">'''
    if selected_filter == 'publisher':
        links = '''<h1>Publishers</h1><ul id="myUL" class='list-group'>''' + links
        for publisher in publisherFilter:
            links += "<li class='list-group-item'><a class='btn btn-primary mw-100 w-100'  href='publisher/" \
                     + html.escape(publisher) + "'>" + publisher + "</a></li>"
        links += "</ul>"
    elif selected_filter == 'age':
        links = '''<h1>Comic Book Ages</h1><ul id="myUL" class='list-group'>''' + links
        for age in ageFilter:
            links += "<li class='list-group-item'><a class='btn btn-primary mw-100 w-100' href='age/" \
                     + html.escape(age) + "'>" + age + "</a></li>"
        links += "</ul>"
    elif selected_filter == 'series':
        links = '''<h1>Series</h1><ul id="myUL" class='list-group'>''' + links
        for series in seriesFilter:
            links += "<li class='list-group-item'><a class='btn btn-primary mw-100 w-100' href='series/" \
                     + html.escape(series) + "'>" + series + "</a></li>"
        links += "</ul>"
    elif selected_filter == 'creators':
        links = '''<h1>Creators</h1><ul id="myUL" class='list-group'>''' + links
        for creators in creatorsFilter:
            links += "<li class='list-group-item'><a class='btn btn-primary mw-100 w-100' href='creators/" \
                     + html.escape(creators) + "'>" + creators + "</a></li>"
        links += "</ul>"
    elif selected_filter == 'seriesgroup':
        links = '''<h1>Series Groups</h1><ul id="myUL" class='list-group'>''' + links
        for seriesGroup in seriesGroupFilter:
            links += "<li class='list-group-item'><a class='btn btn-primary mw-100 w-100' href='seriesgroup/" \
                     + html.escape(seriesGroup) + "'>" + seriesGroup + "</a></li>"
        links += "</ul>"

    return links


def refresh_display_file(image_filter):
    global comicCollection
    comicCollection = get_comic_collection()
    file_text = ""

    if image_filter[0] == "all":
        for comic in comicCollection:
            if "coverfront" in comic:
                file_text += os.getcwd() + "/" + config.sourceImagePath + "/" + comic['coverfront'] + '\n'
    else:
        # copy images with filter
        for comic in comicCollection:
            if str(comic.get(image_filter[0])).find(image_filter[1]) >= 0:
                if "coverfront" in comic:
                    file_text += os.getcwd() + "/" + config.sourceImagePath + "/" + comic['coverfront'] + '\n'

    f = open(config.imageFilePath, 'w')
    f.write(file_text)
    f.close()


def get_comic_collection() -> list:
    collection_xml = ET.parse(config.comicFilePath)
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

        collection_array.append(comic_info)
    return collection_array


def get_display_filters(comic_collection: list):
    for comic in comic_collection:
        for filter_item, value in comic.items():
            if filter_item == "series":
                if value not in seriesFilter:
                    seriesFilter.append(value)
            elif filter_item == "seriesgroup":
                if value not in seriesGroupFilter:
                    seriesGroupFilter.append(value)
            elif filter_item == "publisher":
                if value not in publisherFilter:
                    publisherFilter.append(value)
            elif filter_item == "age":
                if value not in ageFilter:
                    ageFilter.append(value)
            elif filter_item == "creators":
                for creator in value.split(";"):
                    if creator.strip() not in creatorsFilter:
                        creatorsFilter.append(creator.strip())
    seriesFilter.sort()
    publisherFilter.sort()
    ageFilter.sort()
    creatorsFilter.sort()
    seriesGroupFilter.sort()


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

    app.run(debug=True, host='0.0.0.0')


if __name__ == "__main__":
    main()
