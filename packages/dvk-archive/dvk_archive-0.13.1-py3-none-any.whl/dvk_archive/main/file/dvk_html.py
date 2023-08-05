#!/usr/bin/env python3

from argparse import ArgumentParser
from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.file.dvk_handler import DvkHandler
from dvk_archive.main.color_print import color_print
from dvk_archive.main.processing.html_processing import add_escapes
from dvk_archive.main.processing.html_processing import create_html_tag
from dvk_archive.main.processing.string_processing import get_extension
from dvk_archive.main.processing.string_processing import pad_num
from dvk_archive.main.processing.list_processing import clean_list
from dvk_archive.main.processing.list_processing import list_to_string
from os import mkdir, pardir
from os.path import abspath, exists, isdir, join
from shutil import rmtree
from tempfile import gettempdir
from traceback import print_exc
from typing import List
from webbrowser import open as web_open

def get_file_as_url(file:str=None) -> str:
    """
    Converts a file path to be read as a URL in a web browser.

    :param file: File path to convert, defaults to None
    :type file: str, optional
    :return: File URL
    :rtype: str
    """
    # Return empty string if path is invalid
    if file is None or file == "":
        return ""
    # Replace characters with escapes if necessary
    url = ""
    for i in range(0, len(file)):
        char = file[i]
        value = ord(char)
        if ((value > 47 and value < 58)
                    or (value > 64 and value < 91)
                    or (value > 96 and value < 123)
                    or char == "-"
                    or char == "/"
                    or char == "\\"
                    or char == "."):
            # Use existing character
            url = url + char
        else:
            # Use URL escape character
            url = url + "%" + hex(value)[2:].upper()
    # Return path with "file://" url tag
    return "file://" + url

def get_temp_directory(delete:bool=False) -> str:
    """
    Returns a temporary directory for holding HTML files.

    :param delete: Whether to delete previous directory contents, defaults to False
    :type delete: bool, optional
    :return: Path of the temporary directory
    :rtype: str
    """
    # Get path of the temp directory
    temp_dir = abspath(join(abspath(gettempdir()), "dvk_html"))
    # Delete directory if specified
    temp_exists = exists(temp_dir)
    if delete and temp_exists:
        rmtree(temp_dir)
        temp_exists = False
    # Create temp directory if necessary
    if not temp_exists:
        mkdir(temp_dir)
    return temp_dir

def list_to_lines(lst:List[str]=None) -> str:
    """
    Converts a list of strings into a single string with items on separate lines.

    :param lst: List of strings, defaults to None
    :type lst: list[str], optional
    :return: Single string with items on separate lines
    :rtype: str
    """
    # Return empty string if list is None
    if lst is None:
        return ""
    # Convert list to single string
    lines = ""
    for i in range(0, len(lst)):
        # Add new line character if necessary
        if i > 0:
            lines = lines + "\n"
        # Add item to the string
        lines = lines + lst[i]
    return lines

def get_time_string(dvk:Dvk=None, twelve_hour:bool=True) -> str:
    """
    Returns a HTML string showing a Dvk's time published in a readable format.

    :param dvk: Dvk to get time info from, defaults to None
    :type dvk: Dvk, optional
    :param twelve_hour: Whether to use a 12-hour instead of a 24-hour clock, defaults to True
    :type twelve_hour: bool, optional
    :return: HTML string showing the time published
    :rtype: str
    """
    # Check if the time published is invalid
    if dvk is None or dvk.get_time() == "0000/00/00|00:00":
        return "Unknown Publication Date"
    # Get the year
    time = dvk.get_time()
    year = time[0:4]
    # Get the month
    month_int = int(time[5:7])
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month = months[month_int-1]
    # Get the day
    day = time[8:10]
    # Get the hour
    hour_int = int(time[11:13])
    # Get the minute
    minute = time[14:16]
    # Get the clock string
    clock_string = ":" + minute
    if twelve_hour:
        # Convert 24-hour time to 12-hour clock
        if hour_int < 12:
            clock_string = clock_string + " AM"
            if hour_int == 0:
                hour_int = 12
        else:
            clock_string = clock_string + " PM"
            if not hour_int == 12:
                hour_int -= 12
    clock_string = pad_num(str(hour_int), 2) + clock_string
    # Combine to form full time string
    time_string = "Posted <b>" + day + " " + month + " " + year\
                + " - " + clock_string + "</b>"
    # Return the time string
    return time_string

def is_image_extension(extension:str=None) -> bool:
    """
    Returns whether a given file extension is for an image file.

    :param extension: Given file extension, defaults to None
    :type extension: str, optional
    :return: Whether file extension is for an image file.
    :rtype: bool
    """
    if (extension == ".jpg"
            or extension == ".jpeg"
            or extension == ".png"
            or extension == ".gif"
            or extension == ".svg"
            or extension == ".webp"
            or extension == ".apng"
            or extension == ".avif"
            or extension == ".jfif"
            or extension == ".pjpeg"
            or extension == ".pjp"):
        return True
    return False

def get_text_media_html(dvk:Dvk=None) -> str:
    """
    Returns an HTML tag that contains embeded text found in the linked text media file for a given Dvk.

    :param dvk: Dvk to get media file and text from, defaults to None
    :type dvk: Dvk, optional
    :return: HTML tag that contains the text for a given Dvk
    :rtype: str
    """
    # Return empty string if parameters are invalid
    if dvk is None or dvk.get_title() is None or dvk.get_media_file() is None:
        return ""
    media_tag = ""
    media_file = dvk.get_media_file()
    print(media_file)
    extension = get_extension(media_file)
    # Read the text file linked by the Dvk
    try:
        with open(media_file, encoding="utf-8") as f:
            contents = f.read()
    except Exception:
        try:
            with open(media_file, encoding="iso-8859-1") as f:
                contents = f.read()
        except Exception:
            return ""
    # Modify the contents depending on the type of text
    if extension == ".txt":
        # Add escape characters to standard text
        contents = add_escapes(contents)
        contents = contents.replace("&#10;", "<br/>")
    else:
        # Remove unnecessary tags from HTML text
        contents = contents.replace("<!DOCTYPE html>", "")
        contents = contents.replace("<html>", "").replace("</html>", "")
    # Create header with the Dvk title
    title = add_escapes(dvk.get_title())
    attr = [["id", "dvk_text_header"], ["class", "dvk_padded"]]
    header = create_html_tag("div", attr, f"<b>{title}</b>", False)
    # Create div container for the media text
    attr = [["id", "dvk_text_container"], ["class", "dvk_padded"]]
    text_div = create_html_tag("div", attr, contents)
    # Combine text and header into a media tag
    attr = [["id", "dvk_text_media"], ["class", "dvk_info"]]
    media_tag = create_html_tag("div", attr, list_to_lines([header, text_div]))
    # Return the completed media tag
    return media_tag

def get_media_html(dvk:Dvk=None) -> str:
    """
    Returns an HTML tag that contains the media file(s) for a given Dvk.

    :param dvk: Dvk to get media file(s) from, defaults to None
    :type dvk: Dvk, optional
    :return: HTML tag that displays the media file for a given Dvk
    :rtype: str
    """
    # Return empty string if parameters are invalid
    if dvk is None or dvk.get_title() is None or dvk.get_media_file() is None:
        return ""
    media_tag = ""
    use_secondary = True
    media_file = dvk.get_media_file()
    extension = get_extension(media_file)
    if is_image_extension(extension):
        # If media file is an image, create an HTML img tag
        attr = [["id", "dvk_image"],
                    ["src", get_file_as_url(media_file)],
                    ["alt", add_escapes(dvk.get_title())]]
        media_tag = create_html_tag("img", attr)
        use_secondary = False
    elif extension == ".txt" or extension == ".html" or extension == ".htm":
        media_tag = get_text_media_html(dvk)
    elif extension == ".pdf":
        # If media file is a PDF, create an HTML iframe
        attr = [["id", "dvk_pdf"], ["src", get_file_as_url(media_file)]]
        media_tag = create_html_tag("iframe", attr, "", False)
        use_secondary = False
    # Add secondary file if available and relevant
    secondary = dvk.get_secondary_file()
    if use_secondary and secondary is not None and is_image_extension(get_extension(secondary)):
        attr = [["id", "dvk_image"],
                    ["src", get_file_as_url(secondary)],
                    ["alt", add_escapes(dvk.get_title())]]
        media_tag = list_to_lines([create_html_tag("img", attr), media_tag])
    # Returns the media tag
    return media_tag

def get_dvk_header_html(dvk:Dvk=None) -> str:
    """
    Returns dvk_header HTML tag for a given Dvk.
    Contains Dvk's title, artist(s), and publication time.

    :param dvk: Dvk to get info from, defaults to None
    :type dvk: Dvk, optional
    :return: Header tag for the given Dvk
    :rtype: str
    """
    # Return empty string if parameters are invalid
    if dvk is None or dvk.get_title() is None or dvk.get_artists() == []:
        return ""
    # Create title tag
    title_tag = "<b>" + add_escapes(dvk.get_title()) + "</b>"
    title_tag = create_html_tag("div", [["id","dvk_title"]], title_tag, False)
    # Create published tag
    pub_tag = "By <b>" + list_to_string(dvk.get_artists(), True, 1)\
                + "</b>, " + get_time_string(dvk)
    pub_tag = create_html_tag("div", [["id", "dvk_pub"]], pub_tag, False)
    # Combine into header tag
    attr = [["id", "dvk_header"], ["class", "dvk_padded"]]
    header = create_html_tag("div", attr, title_tag + "\n" + pub_tag)
    # Return dvk_header tag
    return header

def get_dvk_info_html(dvk:Dvk=None) -> str:
    """
    Returns HTML containing the main Dvk info.
    Includes the title, artist(s), time published, and description.

    :param dvk: Dvk to get info from, defaults to None
    :type dvk: Dvk, optional
    :return: HTML containing main Dvk info.
    :rtype: str
    """
    # Create the dvk_header tag
    header_tag = get_dvk_header_html(dvk)
    # Return empty string if header is empty
    if header_tag == "":
        return ""
    # Create div to hold the description
    desc_tag = ""
    attr = [["id", "dvk_description"], ["class", "dvk_padded"]]
    description = dvk.get_description()
    if description is None:
        desc_tag = create_html_tag("div", attr, "<i>No Description</i>")
    else:
        desc_tag = create_html_tag("div", attr, description)
    # Combine into larger dvk_info_base tag
    attr = [["id", "dvk_info_base"], ["class", "dvk_info"]]
    info = create_html_tag("div", attr, header_tag + "\n" + desc_tag)
    # Return the dvk_info_base tag
    return info

def get_tag_info_html(dvk:Dvk=None) -> str:
    """
    Returns an HTML block containing the web_tags for a given Dvk.

    :param dvk: Dvk to get web_tags from.
    :type dvk: Dvk, optional
    :return: HTML block containing web_tags
    :rtype: str
    """
    # Return empty string if there are no tags
    if dvk is None or dvk.get_web_tags() == []:
        return ""
    # Create web_tag_header
    attr = [["id", "dvk_web_tag_header"], ["class", "dvk_padded"]]
    wt_header = create_html_tag("b", None, "Web Tags", False)
    wt_header = create_html_tag("div", attr, wt_header, False)
    # Create web_tag_elements
    wt_elements = []
    attr = [["class", "dvk_tag"]]
    web_tags = dvk.get_web_tags()
    for tag in web_tags:
        element = create_html_tag("span", attr, add_escapes(tag), False)
        wt_elements.append(element)
    # Create web_tag_container
    attr = [["id", "dvk_tags"], ["class", "dvk_padded"]]
    wt_container = create_html_tag("div", attr, list_to_lines(wt_elements))
    # Create tag info container
    attr = [["id", "dvk_tag_info"], ["class", "dvk_info"]]
    ti = create_html_tag("div", attr, wt_header + "\n" + wt_container)
    return ti

def get_page_link_html(dvk:Dvk=None) -> str:
    """
    Returns an HTML tag including links to all the URLs contained in the Dvk.
    Contains the Page URL as well as direct media and and secondary media URLs.

    :param dvk: Dvk to get URLs from, defaults to None
    :type dvk: Dvk, optional
    :return: HTML tag containing links to the Dvk's media
    :rtype: str
    """
    links = []
    cls = ["class", "dvk_link"]
    # Return empty string if Dvk is invalid
    if dvk is None:
        return ""
    # Get page URL link
    page = dvk.get_page_url()
    if page is not None:
        link = create_html_tag("a", [cls, ["href", page]], "Page URL", False)
        links.append(link)
    # Get direct URL link
    direct = dvk.get_direct_url()
    if direct is not None:
        link = create_html_tag("a", [cls, ["href", direct]], "Direct URL", False)
        links.append(link)
    # Get secondary URL link
    secondary = dvk.get_secondary_url()
    if secondary is not None:
        link = create_html_tag("a", [cls, ["href", secondary]], "Secondary URL", False)
        links.append(link)
    # Set the appropriate attributes for the number of links used
    if len(links) == 3:
        attr = [["id", "dvk_page_links"], ["class", "dvk_three_grid"]]
    elif len(links) == 2:
        attr = [["id", "dvk_page_links"], ["class", "dvk_two_grid"]]
    elif len(links) == 1:
        attr = [["id", "dvk_page_links"], ["class", "dvk_one_grid"]]
    else:
        # Return empty string if no links are present
        return ""
    # Combine links into an HTML tag
    return create_html_tag("div", attr, list_to_lines(links))

def get_navbar_html(prev_path:str=None, next_path:str=None) -> str:
    """
    Creates a navbar for navigating to other Dvk HTML files.

    :param prev_path: Path of the previous Dvk HTML, defaults to None
    :type prev_path: str, optional
    :param next_path: Path of the next Dvk HTML, defaults to None
    :type next_path: str, optional
    :return: HTML tag for the navbar
    :rtype: str
    """
    # Return empty string if no prev or next paths are given
    if prev_path is None and next_path is None:
        return ""
    # Get link to previous Dvk HTML
    prev_tag = create_html_tag("span", [["class", "dvk_muted_link"]], "&lt; PREV", False)
    if prev_path is not None:
        attr = [["class", "dvk_link"], ["href", get_file_as_url(prev_path)]]
        prev_tag = create_html_tag("a", attr, "&lt; PREV", False)
    # Get link to previous Dvk HTML
    next_tag = create_html_tag("span", [["class", "dvk_muted_link"]], "NEXT &gt;", False)
    if next_path is not None:
        attr = [["class", "dvk_link"], ["href", get_file_as_url(next_path)]]
        next_tag = create_html_tag("a", attr, "NEXT &gt;", False)
    # Combine into one div tag
    attr = [["id", "dvk_navbar"], ["class", "dvk_two_grid"]]
    navbar_tag = create_html_tag("div", attr, list_to_lines([prev_tag, next_tag]))
    return navbar_tag

def create_css(directory:str=None) -> str:
    """
    Creates a CSS file for styling DVK HTML.

    :param directory: Directory to save the CSS file, defaults to None
    :type directory: str, optional
    :return: Path to the written CSS file
    :rtype: str
    """
    if directory is None or not isdir(directory) or not exists(directory):
        return ""
    # Color variables
    pad_space = 6
    border_width = "1px"
    base_font_size = "16px"
    large_font_size = "24px"
    portrait_width_size = "1000px"
    info_color = "rgb(60, 60, 60)"
    tag_color = "rgb(80,80,80)"
    text_color = "rgb(250,250,250)"
    header_color = "rgb(40,40,40)"
    border_color = "rgb(100,100,100)"
    background_color = "rgb(30,30,30)"
    link_color = "rgb(60,135,200)"
    link_hover_color = "rgb(95,160,210)"
    link_active_color = "rgb(240,45,85)"
    # Set the default background color and font
    css = ["body {"]
    css.append("    background-color: " + background_color + ";")
    css.append("    font-family: Arial, sans-serif;")
    css.append("    font-size:" + base_font_size + ";")
    css.append("}")
    # Set the default text color
    css.append("")
    css.append("div {")
    css.append("    color: " + text_color + ";")
    css.append("}")
    # Set the title font size
    css.append("")
    css.append("#dvk_title, #dvk_text_header {")
    css.append("    font-size: " + large_font_size + ";")
    css.append("}")
    # Set style for links
    css.append("")
    css.append("a {")
    css.append("    color: " + link_color + ";")
    css.append("    text-decoration: none;")
    css.append("}")
    css.append("")
    css.append("a:active {")
    css.append("    color: " + link_active_color + ";")
    css.append("}")
    css.append("a:hover {")
    css.append("    color: " + link_hover_color + ";")
    css.append("}")
    # Set the default padding
    css.append("")
    css.append(".dvk_padded, .dvk_tag, .dvk_link, .dvk_muted_link {")
    css.append("    padding-top: " + str(pad_space) + "px;")
    css.append("    padding-bottom: " + str(pad_space) + "px;")
    css.append("    padding-left: " + str(pad_space) + "px;")
    css.append("    padding-right: " + str(pad_space) + "px;")
    css.append("}")
    # Set the default dvk_info style
    css.append("")
    css.append(".dvk_info {")
    css.append("    background-color: " + info_color + ";")
    css.append("    border-style: solid;")
    css.append("    border-width: " + border_width + ";")
    css.append("    border-color: " + border_color + ";")
    css.append("    margin-top: " + str(pad_space) + "px;")
    css.append("    margin-bottom: " + str(pad_space) + "px;")
    css.append("    margin-left: 0px;")
    css.append("    margin-right: 0px;")
    css.append("}")
    # Set the header style
    css.append("")
    css.append("#dvk_header, #dvk_web_tag_header, #dvk_text_header {")
    css.append("    background-color: " + header_color + ";")
    css.append("}")
    # Set the tag style
    css.append("")
    css.append(".dvk_tag {")
    css.append("    display: inline-block;")
    css.append("    background-color: " + tag_color + ";")
    css.append("    margin-top: 0px;")
    css.append("    margin-left: 0px;")
    css.append("    margin-bottom: " + str(pad_space) + "px;")
    css.append("    margin-right: " + str(pad_space) + "px;")
    css.append("}")
    css.append("")
    css.append("#dvk_tags {")
    css.append("    padding-bottom: 0px;")
    css.append("    padding-right: 0px;")
    css.append("}")
    # Set style for dvk_links
    css.append("")
    css.append(".dvk_link, .dvk_muted_link {")
    css.append("    text-align: center;")
    css.append("    color: " + text_color + ";")
    css.append("    background-color: " + info_color + ";")
    css.append("    display: block;")
    css.append("    border-style: solid;")
    css.append("    border-width: " + border_width + ";")
    css.append("    border-color: " + border_color + ";")
    css.append("}")
    css.append("")
    css.append(".dvk_link:hover {")
    css.append("    color: " + text_color + ";")
    css.append("    background-color: " + tag_color + ";")
    css.append("}")
    # Set style for the page links
    css.append("")
    css.append("#dvk_page_links {")
    css.append("    display: grid;")
    css.append("    grid-column-gap: " + str(pad_space) + "px;")
    css.append("    grid-row-gap: 0px;")
    css.append("}")
    css.append("")
    css.append(".dvk_four_grid {")
    css.append("    grid-template-columns: 25% 25% 25% 25%;")
    css.append("    margin-right: 0px;")
    css.append("}")
    css.append("")
    css.append(".dvk_three_grid {")
    css.append("    grid-template-columns: 33% 34% 33%;")
    css.append("    margin-right: " + str(pad_space*2) + "px;")
    css.append("}")
    css.append("")
    css.append(".dvk_two_grid {")
    css.append("    grid-template-columns: 50% 50%;")
    css.append("    margin-right: 0px;")
    css.append("}")
    css.append("")
    css.append(".dvk_one_grid {")
    css.append("    grid-template-columns: auto;")
    css.append("    margin-right: 0px;")
    css.append("}")
    # Set style for the navbar
    css.append("")
    css.append("#dvk_navbar {")
    css.append("    display: grid;")
    css.append("    grid-column-gap: " + str(pad_space) + "px;")
    css.append("    grid-row-gap: 0px;")
    css.append("    margin-top: " + str(pad_space) + "px;")
    css.append("}")
    # Set style for muted links
    css.append("")
    css.append(".dvk_muted_link {")
    css.append("    color: " + border_color + ";")
    css.append("    background-color: " + header_color + ";")
    css.append("    border-color: " + info_color + ";")
    css.append("}")
    # Set style for image media
    css.append("")
    css.append("#dvk_image {")
    css.append("    display: block;")
    css.append("    margin-left: auto;")
    css.append("    margin-right: auto;")
    css.append("    margin-top: 0px;")
    css.append("    margin-bottom: 0px;")
    css.append("    max-width: 100%;")
    css.append("    max-height: 100%;")
    css.append("    width: auto;")
    css.append("    height: auto;")
    css.append("}")
    # Set style for pdf media
    css.append("")
    css.append("#dvk_pdf {")
    css.append("    display: block;")
    css.append("    margin-left: auto;")
    css.append("    margin-right: auto;")
    css.append("    margin-top: 0px;")
    css.append("    margin-bottom: 0px;")
    css.append("    width: 98%;")
    css.append("    height: 125vh;")
    css.append("}")
    # Set style for text media
    css.append("")
    css.append("#dvk_text_media {")
    css.append("    display: block;")
    css.append("    margin-left: auto;")
    css.append("    margin-right: auto;")
    css.append(f"    max-width: {portrait_width_size};")
    css.append("}")
    # Write CSS File
    css_file = abspath(join(directory, "dvk_style.css"))
    with open(css_file, "w") as out_file:
        out_file.write(list_to_lines(css))
    if not exists(css_file):
        return ""
    return css_file

def get_dvk_html(dvk:Dvk=None,
                css:str=None,
                prev_path:str=None,
                next_path:str=None) -> str:
    """
    Returns HTML page with all the info for a given Dvk file.

    :param dvk: Dvk to get info from, defaults to None
    :type dvk: Dvk, optional
    :param css: Path of CSS file for styling HTML, defaults to None
    :type css: str, optional
    :param prev_path: Path of the previous Dvk HTML in navbar, defaults to None
    :type prev_path: str, optional
    :param next_path: Path of the next Dvk HTML in navbar, defaults to None
    :type next_path: str, optional
    :return: HTML containing Dvk info
    :rtype: str
    """
    # Return empty string if dvk is invalid
    if dvk is None or css is None or dvk.get_title() is None:
        return ""
    # Create HTML head
    attr = [["rel", "stylesheet"], ["type", "text/css"], ["href", abspath(css)]]
    link = create_html_tag("link", attr)
    title = create_html_tag("title", None, add_escapes(dvk.get_title()), False)
    charset = create_html_tag("meta", [["charset", "UTF-8"]])
    head = create_html_tag("head", None, list_to_lines([link, title, charset]))
    # Create HTML media tag
    media = get_media_html(dvk)
    # Creath dvk_navbar tag
    dvk_navbar = get_navbar_html(prev_path, next_path)
    # Create dvk_info_tag
    dvk_info = get_dvk_info_html(dvk)
    # Create tag info HTML tag
    tag_info = get_tag_info_html(dvk)
    # Create page link tag
    page_links = get_page_link_html(dvk)
    # Combine into dvk_content tag
    content = list_to_lines(clean_list([media, dvk_navbar, dvk_info, tag_info, page_links]))
    dvk_content = create_html_tag("div", [["id", "dvk_content"]], content)
    # Combine into final HTML
    html = head + "\n" + create_html_tag("body", None, dvk_content)
    html = "<!DOCTYPE html>\n" + create_html_tag("html", None, html)
    # Return HTML
    return html

def write_dvk_html(dvk:Dvk=None,
                   filename:str=None,
                   prev_path:str=None,
                   next_path:str=None,
                   delete:bool=True) -> str:
    """
    Creates an HTML file from Dvk info.

    :param dvk: Dvk to get info from, defaults to None
    :type dvk: Dvk, optional
    :param filename: Filename of the HTML to save, defaults to None
    :type filename: str, optional
    :param prev_path: Path of the previous Dvk HTML in navbar, defaults to None
    :type prev_path: str, optional
    :param next_path: Path of the next Dvk HTML in navbar, defaults to None
    :type next_path: str, optional
    :param delete: Whether to delete the contents of temp directory before writing, defaults to False
    :type delete: bool, optional
    :return: Path of the written HTML file
    :rtype: str
    """
    # Return empty string if parameters are invalid
    if dvk is None or filename is None:
        return ""
    # Get the filename for the dvk
    temp_dir = get_temp_directory(delete)
    html_file = abspath(join(temp_dir, filename))
    # Get HTML for the given Dvk
    css_file = create_css(temp_dir)
    html = get_dvk_html(dvk,
                css=css_file,
                prev_path=prev_path,
                next_path=next_path)
    if html == "":
        return ""
    # Write html to disk
    with open(html_file, "w") as out_file:
        out_file.write(html)
    if not exists(html_file):
        return ""
    # Return the path to the html file
    return html_file

def write_dvk_html_list(dvks:List[Dvk]=None, delete:bool=True) -> List[str]:
    """
    Writes HTML files for a list of Dvks.
    Each Dvk HTML file links to next/previous HTMLs in the navbar

    :param dvks: List of Dvks to create HTMLs from, defaults to None
    :type dvks: list[Dvk], optional
    :param delete: Whether to delete temp directory contents before writing, defaults to True
    :type delete: bool, optional
    :return: List of paths to the generated HTML files
    :rtype: list[str]
    """
    # Return empty list if list of Dvks is invalid
    if dvks is None:
        return []
    # Get the temporary directory
    temp_dir = get_temp_directory(delete)
    # Get HTML for each Dvk
    size = len(dvks)
    htmls = []
    for i in range(0, size):
        # Get previous HTML to link
        prev_path = None
        if i > 0:
            prev_path = abspath(join(temp_dir, str(i-1) + ".html"))
        # Get the next HTML to link
        next_path = None
        if i < (size-1):
            next_path = abspath(join(temp_dir, str(i+1) + ".html"))
        # Write the HTML file
        html = write_dvk_html(dvks[i],
                    filename=str(i) + ".html",
                    prev_path=prev_path,
                    next_path=next_path,
                    delete=False)
        htmls.append(html)
    # Return HTML paths
    return htmls

def main():
    """
    Sets up parser for creating and opening HTML files from DVK.
    """
    parser = ArgumentParser()
    parser.add_argument(
        "dvk",
        help="DVK file to open as an HTML file.",
        type=str)
    parser.add_argument(
        "-l",
        "--load_directory",
        help="Also creates and links HTML files for the whole parent directory",
        action="store_true")
    args = parser.parse_args()
    dvk = Dvk(abspath(args.dvk))
    if dvk is not None and dvk.get_title() is not None:
        if not args.load_directory:
            # Write single HTML file
            html = write_dvk_html(dvk, "dvk")
            if not html == "":
                web_open(get_file_as_url(abspath(html)))
            else:
                color_print("Failed writing HTML", "r")
        else:
            # Write HTML files for the whole directory
            dvk_handler = DvkHandler()
            parent = join(dvk.get_dvk_file(), pardir)
            dvk_handler.read_dvks(parent, False)
            # Get list of all dvks in the parent directory
            dvk_handler.sort_dvks("a")
            dvks = []
            size = dvk_handler.get_size()
            for i in range(0, size):
                dvks.append(dvk_handler.get_dvk(i))
            # Create HTML files
            htmls = write_dvk_html_list(dvks, True)
            # Open Dvk HTML
            index = dvk_handler.get_dvk_by_id(dvk.get_dvk_id())
            web_open(get_file_as_url(abspath(htmls[index])))
    else:
        color_print("Invalid Dvk", "r")

if __name__ == "__main__":
    main()
