#!/usr/bin/env python3

from dvk_archive.main.color_print import color_print
from dvk_archive.main.web.bs_connect import download
from dvk_archive.main.web.bs_connect import get_last_modified
from dvk_archive.main.processing.list_processing import clean_list
from dvk_archive.main.processing.string_processing import get_filename
from dvk_archive.main.processing.string_processing import get_extension
from dvk_archive.main.processing.string_processing import pad_num
from dvk_archive.main.processing.string_processing import remove_whitespace
from dvk_archive.main.processing.html_processing import add_escapes_to_html
from filetype import guess
from json import dump, load
from os import listdir, pardir, rename, remove
from os.path import abspath, basename, exists, isdir, join
from random import seed, randint
from shutil import move
from traceback import print_exc
from typing import List

def dictadd(dictionary:dict=None,
                key:str=None,
                value=None,
                default=None) -> dict:
    """
    Adds a key pair to a dict if not already the default value.

    :param dictionary: Dict to add values to, defaults to None
    :type dictionary: dict, optional
    :param key: Name of the key to assign a value, defaults to None
    :type key: str, optional
    :param value: Value to assign to the key pair, defaults to None
    :type value: any, optional
    :param default: Defalt value of the given key, defaults to None
    :type default: any, optional
    :return: Dict with the value added, if necessary
    :rtype: dict
    """
    # Return dict if parameters are invalid
    if dictionary is None or key is None:
        return dictionary
    # Add value to dict if not default
    my_dict = dictionary
    if not value == default:
        my_dict[key] = value
    return my_dict

def dictget(dictionary:dict=None, key:str=None, default=None):
    """
    Returns the value for a key in a given dictionary.
    Returns a default value if the given key is not found

    :param dictionary: Dictionary to search for key within, defaults to None
    :type dictionary: dict, optional
    :param key: Key to read value from, defaults to None
    :type key: str, optional
    :param default: Default value to return if key is not found, defaults to None
    :type default: Any, optional
    :return: Value of the given key in the dictionary
    :rtype: Any
    """
    try:
        value = dictionary[key]
        return value
    except:
        return default

class Dvk:

    def __init__(self, dvk_file:str=None):
        """
        Initializes the Dvk object by loading from a given DVK file.
        If dvk_file is None, creates an empty Dvk object.

        :param dvk_file: Given DVK file path, defaults to None
        :type dvk_file: str, optional
        """
        self.set_dvk_file()
        self.clear_dvk()
        if dvk_file is not None:
            self.set_dvk_file(dvk_file)
            self.read_dvk()
        
    def clear_dvk(self):
        """
        Clears all Dvk fields to their default values.
        """
        self.set_dvk_id()
        self.set_title()
        self.set_artists()
        self.set_time()
        self.set_web_tags()
        self.set_description()
        self.set_page_url()
        self.set_direct_url()
        self.set_secondary_url();
        self.set_media_file()
        self.set_secondary_file()
        self.set_favorites()
        self.set_single()
        self.set_next_id()
        self.set_prev_id()
        self.set_sequence_title()
        self.set_section_title()
        self.set_sequence_number()
        self.set_sequence_total()

    def can_write(self) -> bool:
        """
        Returns whether the Dvk object can be written.
        Returns False if Dvk doesn't contain necessary info.

        :return: Whether the Dvk object can be written.
        :rtype: bool
        """
        if (self.get_dvk_file() is None
                or self.get_dvk_id() is None
                or self.get_title() is None
                or self.get_artists() == []
                or self.get_page_url() is None
                or self.get_media_file() is None):
            return False
        return True

    def write_dvk(self):
        """
        Writes the Dvk object parameters to dvk_file
        """
        # Check if Dvk oject contains all necessary info.
        if self.can_write():
            # Create dict for the DVK file identifiers.
            dvk_data = dict()
            dvk_data["file_type"] = "dvk"
            dvk_data["id"] = self.get_dvk_id()
            # Create dict for the basic DVK info.
            dvk_info = dict()
            dvk_info = dictadd(dvk_info, "title", self.get_title(), None)
            dvk_info = dictadd(dvk_info, "artists", self.get_artists(), [])
            dvk_info = dictadd(dvk_info, "time", self.get_time(), "0000/00/00|00:00")
            dvk_info = dictadd(dvk_info, "web_tags", self.get_web_tags(), [])
            dvk_info = dictadd(dvk_info, "description", self.get_description(), None)
            # Create dict for info about where media was downloaded from.
            dvk_web = dict()
            dvk_web = dictadd(dvk_web, "page_url", self.get_page_url(), None)
            dvk_web = dictadd(dvk_web, "direct_url", self.get_direct_url(), None)
            dvk_web = dictadd(dvk_web, "secondary_url", self.get_secondary_url(), None)
            # Create dict for info about where media is stored on disk.
            dvk_file_dict = dict()
            if self.get_media_file() is not None:
                dvk_file_dict["media_file"] = basename(self.get_media_file())
            if self.get_secondary_file() is not None:
                dvk_file_dict["secondary_file"] = basename(self.get_secondary_file())
            # Create dict for info about how the Dvk was downloaded
            dvk_download = dict()
            dvk_download = dictadd(dvk_download, "favorites", self.get_favorites(), [])
            dvk_download = dictadd(dvk_download, "is_single", self.is_single(), False)
            # Create dict for info about how the Dvk fits in a sequence
            dvk_seq = dict()
            dvk_seq = dictadd(dvk_seq, "next_id", self.get_next_id(), None)
            dvk_seq = dictadd(dvk_seq, "prev_id", self.get_prev_id(), None)
            dvk_seq = dictadd(dvk_seq, "seq_title", self.get_sequence_title(), None)
            dvk_seq = dictadd(dvk_seq, "section_title", self.get_section_title(), None)
            dvk_seq = dictadd(dvk_seq, "seq_total", self.get_sequence_total(), 1)
            dvk_seq = dictadd(dvk_seq, "seq_num", self.get_sequence_number(), 0)
            # Create dict to combine all Dvk info.
            dvk_data = dictadd(dvk_data, "info", dvk_info, dict())
            dvk_data = dictadd(dvk_data, "web", dvk_web, dict())
            dvk_data = dictadd(dvk_data, "file", dvk_file_dict, dict())
            dvk_data = dictadd(dvk_data, "download", dvk_download, dict())
            dvk_data = dictadd(dvk_data, "sequence", dvk_seq, dict())
            # Write dvk_data dict to a DVK(JSON) file.
            try:
                with open(self.get_dvk_file(), "w") as out_file:
                    dump(dvk_data, out_file, indent=4, separators=(",", ": "))
            except IOError as e:
                color_print("File error: " + str(e), "r")

    def write_media(self, get_time:bool=False):
        """
        Writes the Dvk object, as well as downloading associated media.
        Downloads from direct_url and secondary_url.
        Writes to media_file and secondary_file.

        :param get_time: Whether to get time from the media page, defaults to False
        :type get_time: bool, optional
        """
        headers = ""
        self.write_dvk()
        if exists(self.get_dvk_file()):
            headers = download(self.get_direct_url(), self.get_media_file())
            if self.get_direct_url().startswith("data:"):
                self.set_direct_url(None)
            # CHECK IF MEDIA DOWNLOADED
            if exists(self.get_media_file()):
                # DOWNLOAD SECONDARY FILE, IF AVAILABLE
                if self.get_secondary_url() is not None:
                    download(self.get_secondary_url(), self.get_secondary_file())
                    if self.get_secondary_url().startswith("data:"):
                        self.set_secondary_url(None)
                    # DELETE FILES IF DOWNLOAD FAILED
                    if not exists(self.get_secondary_file()):
                        remove(self.get_dvk_file())
                        remove(self.get_media_file())
            else:
                # IF DOWNLOAD FAILED, DELETE DVK
                remove(self.get_dvk_file())
        # GETS THE MODIFIED DATE FROM THE DOWNLOADED FILE
        if get_time and exists(self.get_media_file()):
            self.set_time(get_last_modified(headers))
            self.write_dvk()
        # UPDATE EXTENSTIONS
        self.update_extensions()

    def read_dvk(self):
        """
        Reads DVK info from the file referenced in dvk_file.
        """
        self.clear_dvk()
        # Read DVK file as a JSON object
        try:
            with open(self.get_dvk_file()) as in_file:
                json = load(in_file)
                # Check if file is a proper DVK file.
                if json["file_type"] == "dvk":
                    # Get DVK ID.
                    self.set_dvk_id(dictget(json, "id", None))
                    # Get basic DVK info.
                    dvk_info = dictget(json, "info", None)
                    self.set_title(dictget(dvk_info, "title", None))
                    self.set_artists(dictget(dvk_info, "artists", []))
                    self.set_time(dictget(dvk_info, "time", None))
                    self.set_web_tags(dictget(dvk_info, "web_tags", []))
                    self.set_description(dictget(dvk_info, "description", None))
                    # Get DVK web info.
                    dvk_web = dictget(json, "web", None)
                    self.set_page_url(dictget(dvk_web, "page_url", None))
                    self.set_direct_url(dictget(dvk_web, "direct_url", None))
                    self.set_secondary_url(dictget(dvk_web, "secondary_url", None))
                    # Get DVK file info.
                    dvk_file_dict = dictget(json, "file", None)
                    file = dictget(dvk_file_dict, "media_file", None)
                    self.set_media_file(file)
                    file = dictget(dvk_file_dict, "secondary_file", None)
                    self.set_secondary_file(file)
                    # Get DVK download info.
                    dvk_download = dictget(json, "download", None)
                    self.set_favorites(dictget(dvk_download, "favorites", []))
                    self.set_single(dictget(dvk_download, "is_single", False))
                    # Get DVK sequence info.
                    dvk_sequence = dictget(json, "sequence", None)
                    self.set_next_id(dictget(dvk_sequence, "next_id", None))
                    self.set_prev_id(dictget(dvk_sequence, "prev_id", None))
                    self.set_sequence_title(dictget(dvk_sequence, "seq_title", None))
                    self.set_section_title(dictget(dvk_sequence, "section_title", None))
                    self.set_sequence_total(dictget(dvk_sequence, "seq_total", 1))
                    self.set_sequence_number(dictget(dvk_sequence, "seq_num", 0))
        except:
            color_print("Error reading DVK file: " + self.get_dvk_file(), "r")
            print_exc()
            self.clear_dvk()

    def set_dvk_file(self, dvk_file:str=None):
        """
        Sets the DVK file.

        :param dvk_file: Path of the DVK file, defaults to None
        :type dvk_file: str, optional
        """
        self.dvk_file = dvk_file

    def get_dvk_file(self) -> str:
        """
        Returns path for the DVK file.

        :return: DVK file path
        :rtype: str
        """
        return self.dvk_file

    def set_dvk_id(self, dvk_id:str=None):
        """
        Sets the Dvk ID.

        :param dvk_id: Dvk ID, defaults to None
        :type dvk_id: str, optional
        """
        try:
            self.dvk_id = remove_whitespace(dvk_id.upper())
            if self.dvk_id == "":
                self.dvk_id = None
        except AttributeError:
            self.dvk_id = None            

    def get_dvk_id(self) -> str:
        """
        Returns the Dvk ID.

        :return: Dvk ID
        :rtype: str
        """
        return self.dvk_id

    def set_title(self, title:str=None):
        """
        Sets the Dvk title.

        :param title: Dvk title, defaults to None
        :type title: str, optional
        """
        self.title = title
        if self.title is not None:
            self.title = remove_whitespace(self.title)

    def get_title(self) -> str:
        """
        Returns the Dvk title.

        :return: Dvk title
        :rtype: str
        """
        return self.title

    def set_artist(self, artist:str=None):
        """
        Sets the Dvk artists variable for a single artist.

        :param artist: Dvk artist, defaults to None
        :type artist: str, optional
        """
        self.set_artists([artist])

    def set_artists(self, artists:List[str]=None):
        """
        Sets the Dvk artists.

        :param artists: Dvk artists, defaults to None
        :type artists: list[str], optional
        """
        # Sort artists as well as removing duplicates
        array = sorted(clean_list(artists, True), key=str.casefold)
        self.artists = array
            

    def get_artists(self) -> List[str]:
        """
        Returns the Dvk artists.

        :return: Dvk artists
        :rtype: list[str]
        """
        return self.artists

    def set_time_int(
            self,
            year:int=0,
            month:int=0,
            day:int=0,
            hour:int=0,
            minute:int=0):
        """
        Sets the time published for the Dvk.
        Defaults to value 0000/00/00|00:00 if invalid.

        :param year: Year published (1-9999), defaults to 0
        :type year: int, optional
        :param month: Month published (1-12), defaults to 0
        :type month: int, optional
        :param day: Day published (1-31), defaults to 0
        :type day: int, optional
        :param hour: Hour published (0-23), defaults to 0
        :type hour: int, optional
        :param minute: Minute published (0-59), defaults to 0
        :type minute: int, optional
        """
        # Check if time is valid.
        if (year < 1
                or year > 9999
                or month < 1
                or month > 12
                or day < 1
                or day > 31
                or hour < 0
                or hour > 23
                or minute < 0
                or minute > 59):
            # If time is invalid, set empty publication date.
            self.time = "0000/00/00|00:00"
        else:
            # Pad times with zeros if necessary.
            year_str = pad_num(str(year), 4)
            month_str = pad_num(str(month), 2)
            day_str = pad_num(str(day), 2)
            hour_str = pad_num(str(hour), 2)
            minute_str = pad_num(str(minute), 2)
            # Combine to make time string.
            self.time = year_str + "/" + month_str + "/" + day_str + "|" + hour_str + ":" + minute_str

    def set_time(self, time_str:str=None):
        """
        Sets the time published for the Dvk.
        Defaults to value 0000/00/00|00:00 if invalid.

        :param time_str: Time string formatted YYYY/MM/DD|hh:mm, defaults to None
        :type time_str: str, optional
        """
        # If time string is not in the proper format, set empty date
        if time_str is None or not len(time_str) == 16:
            self.time = "0000/00/00|00:00"
        else:
            try:
                # Extract values from the time string.
                year = int(time_str[0:4])
                month = int(time_str[5:7])
                day = int(time_str[8:10])
                hour = int(time_str[11:13])
                minute = int(time_str[14:16])
                self.set_time_int(year, month, day, hour, minute)
            except ValueError:
                # If any values failed to extract, set empty date
                self.time = "0000/00/00|00:00"

    def get_time(self) -> str:
        """
        Returns the time published for the Dvk.
        Formatted YYYY/MM/DD|hh:mm

        :return: Dvk's time published
        :rtype: str
        """
        return self.time

    def set_web_tags(self, web_tags:List[str]=None):
        """
        Sets Dvk web tags.

        :param web_tags: Dvk web tags, defaults to None
        :type web_tags: list[str], optional
        """
        self.web_tags = clean_list(web_tags, True)

    def get_web_tags(self) -> List[str]:
        """
        Returns Dvk web tags.

        :return: Dvk web tags
        :rtype: list[str]
        """
        return self.web_tags

    def set_description(self, description:str=None):
        """
        Sets the Dvk description.

        :param description: Dvk description, defaults to None
        :type description: str, optional
        """
        self.description = add_escapes_to_html(remove_whitespace(description))
        if self.description == "":
            self.description = None

    def get_description(self) -> str:
        """
        Returns the Dvk description.

        :return: Dvk description
        :rtype: str
        """
        return self.description

    def set_page_url(self, page_url:str=None):
        """
        Sets the Dvk page URL.

        :param page_url: Page URL, defaults to None
        :type page_url: str, optional
        """
        self.page_url = page_url
        if self.page_url == "":
            self.page_url = None

    def get_page_url(self) -> str:
        """
        Returns the Dvk page URL.

        :return: Page URL
        :rtype: str
        """
        return self.page_url

    def set_direct_url(self, direct_url:str=None):
        """
        Sets the direct media URL.

        :param direct_url: Direct media URL, defaults to None
        :type direct_url: str, optional
        """
        self.direct_url = direct_url
        if self.direct_url == "":
            self.direct_url = None

    def get_direct_url(self) -> str:
        """
        Returns the direct media URL.

        :return: Direct media URL
        :rtype: str
        """
        return self.direct_url

    def set_secondary_url(self, secondary_url:str=None):
        """
        Sets the direct secondary media URL.

        :param secondary_url: Direct secondary media URL, defaults to None
        :type secondary_url: str, optional
        """
        self.secondary_url = secondary_url
        if self.secondary_url == "":
            self.secondary_url = None

    def get_secondary_url(self) -> str:
        """
        Returns the direct secondary media URL.

        :return: Direct secondary media URL
        :rtype: str
        """
        return self.secondary_url

    def set_media_file(self, filename:str=None):
        """
        Sets the associated media file for the Dvk object.
        Assumes media is in the same directory as dvk_file.

        :param filename: Filename for the associated media, defaults to None
        :type filename: str, optional
        """
        self.media_file = filename
        if self.media_file == "":
            self.media_file = None

    def get_media_file(self) -> str:
        """
        Returns the Dvk's associated media file path.

        :return: Associated media file path
        :rtype: str
        """
        try:
            parent = abspath(join(abspath(self.get_dvk_file()), pardir))
            if not exists(parent):
                return None
            return abspath(join(parent, self.media_file))
        except:
            return None

    def set_secondary_file(self, filename:str=None):
        """
        Sets the associated secondary media file for the Dvk object.
        Assumes media is in the same directory as dvk_file.

        :param filename: Filename for the secondary associated media, defaults to None
        :type filename: str, optional
        """
        self.secondary_file = filename
        if self.secondary_file == "":
            self.secondary_file = None

    def get_secondary_file(self) -> str:
        """
        Returns the Dvk's associated secondary media file path.

        :return: Associated seconsary media file path
        :rtype: str
        """
        try:
            parent = abspath(join(abspath(self.get_dvk_file()), pardir))
            if not exists(parent):
                return None
            return abspath(join(parent, self.secondary_file))
        except:
            return None

    def set_favorites(self, favorites:List[str]=None):
        """
        Sets a list of artists that favorited this media online.

        :param favorites: List of favorites artists, defaults to None
        :type favorites: list[str], optional
        """
        # GET LEGACY FAVORITES FROM WEB TAGS
        index = 0
        array = []
        tags = self.get_web_tags()
        while index < len(tags):
            lower = tags[index].lower()
            if lower.startswith("favorite:"):
                array.append(tags[index][9:])
                del tags[index]
                index -= 1
            # INCREMENT INDEX
            index += 1
        self.set_web_tags(tags)
        # ADD GIVEN FAVORITES
        if favorites is not None:
            array.extend(favorites)
        # SORTS FAVORITES AND REMOVES DUPLICATES
        array = sorted(clean_list(array), key=str.casefold)
        self.favorites = array

    def get_favorites(self) -> List[str]:
        """
        Returns list of artists that favorited this media online.

        :return: List of favorites artists
        :rtype: list[str]
        """
        return self.favorites

    def set_single(self, single:bool=False):
        """
        Sets whether the Dvk's media was downloaded as a single file.

        :param single: Whether the Dvk is a single file, defaults to False
        :type single: bool, optional
        """
        # GET LEGACY SINGLE TAG FROM WEB TAGS
        index = 0
        r_single = False
        tags = self.get_web_tags()
        while index < len(tags):
            lower = tags[index].lower()
            if lower == "dvk:single":
                r_single = True
                del tags[index]
                index -= 1
            index += 1
        self.set_web_tags(tags)
        # USE GIVEN SINGLE VALUE IF NOT OVERWRITTEN BY LEGACY TAG
        if not r_single:
            r_single = single
        self.single = r_single

    def is_single(self) -> bool:
        """
        Returns whether the Dvk's media was downloaded as a single file.

        :return: Whether Dvk is a single file
        :rtype: bool
        """
        return self.single

    def set_next_id(self, next_id:str=None):
        """
        Sets the next ID in a media sequence.

        :param next_id: Next ID in the sequnce, defaults to None
        :type next_id: str, optional 
        """
        self.next_id = next_id

    def get_next_id(self) -> str:
        """
        Returns the next ID in a media sequence.

        :return: Next ID in the sequence
        :rtype: str
        """
        return self.next_id

    def set_prev_id(self, prev_id:str=None):
        """
        Sets the previous ID in a media sequence.

        :param prev_id: Previous ID in the sequnce, defaults to None
        :type prev_id: str, optional 
        """
        self.prev_id = prev_id

    def get_prev_id(self) -> str:
        """
        Returns the previous ID in a media sequence.

        :return: Previous ID in the sequence
        :rtype: str
        """
        return self.prev_id

    def set_first(self):
        """
        Sets Dvk to be the first of a sequence.
        Adds marker to prev_id indicating there are no previous Dvks.
        """
        self.set_prev_id("non")

    def is_first(self) -> bool:
        """
        Returns whether Dvk is the first in a sequence.

        :return: Whether Dvk is the first in a sequence.
        :rtype: bool
        """
        if self.get_prev_id() == "non":
            return True
        return False

    def set_last(self):
        """
        Sets Dvk to be the last of a sequence.
        Adds marker to next_id indicating there are no next Dvks.
        """
        self.set_next_id("non")

    def is_last(self) -> bool:
        """
        Returns whether Dvk is the last in a sequence.

        :return: Whether Dvk is the last in a sequence.
        :rtype: bool
        """
        if self.get_next_id() == "non":
            return True
        return False

    def set_sequence_title(self, seq_title:str=None):
        """
        Sets the title of the sequence Dvk is part of.

        :param seq_title: Sequence title, defaults to None
        :type seq_title: str, optional
        """
        self.seq_title = remove_whitespace(seq_title)
        if self.seq_title == "":
            self.seq_title = None

    def get_sequence_title(self) -> str:
        """
        Returns the sequence title for the Dvk.

        :return: Sequence title
        :rtype: str
        """
        return self.seq_title

    def set_section_title(self, section_title:str=None):
        """
        Sets the title of the section of a sequence Dvk is part of.

        :param section_title: Section title, defaults to None
        :type section_title: str, optional
        """
        self.section_title = remove_whitespace(section_title)
        if self.section_title == "":
            self.section_title = None

    def get_section_title(self) -> str:
        """
        Returns the section title for the Dvk.

        :return: Section title
        :rtype: str
        """
        return self.section_title

    def set_sequence_number(self, seq_num:int=0):
        """
        Sets the number indicating where the Dvk is in a sequence.

        :param seq_num: Sequence number, defaults to 0
        :type seq_num: int, optional
        """
        if seq_num < 1 or seq_num > self.get_sequence_total():
            self.sequence_number = 0
        else:
            self.sequence_number = seq_num

    def get_sequence_number(self) -> int:
        """
        Returns the number indicating where the Dvk is in a sequence.

        :return: Sequence number
        :rtype: int
        """
        return self.sequence_number

    def set_sequence_total(self, seq_total:int=1):
        """
        Sets the total number of files in the sequence the Dvk is part of.

        :param seq_total: Total number of files in the sequence, defaults to 1
        :type seq_total: int, optional
        """
        if seq_total < 2:
            self.sequence_total = 1
        else:
            self.sequence_total = seq_total

    def get_sequence_total(self) -> int:
        """
        Gets the total number of files in the sequence the Dvk is part of.

        :return: Total number of files in the sequence
        :rtype: int
        """
        return self.sequence_total

    def get_filename(self, directory:str=None, secondary:bool=False) -> str:
        """
        Returns a filename for the Dvk based on title and id.
        Doesn't include extension.

        :param directory: Dirctory in which DVK will be saved, defaults to None
        :type directory: str, optional
        :param secondary: Whether to get name for a secondary file, defaults to False
        :type secondary: bool, optional
        """
        if (directory is None
                    or not exists(directory)
                    or self.get_artists() == []
                    or self.get_title() is None
                    or self.get_dvk_id() is None):
            return ""
        # Get old dvk filename
        try:
            old = basename(self.get_dvk_file())
            old = old[:len(old)-4].lower()
        except:
            old = None
        # Get extension
        if secondary and self.get_secondary_url() is not None:
            ext = get_extension(self.get_secondary_url())
        elif not secondary and self.get_direct_url is not None:
            ext = get_extension(self.get_direct_url())
        else:
            ext = ""
        # Get list of files in the directory
        paths = listdir(directory)
        for i in range(0, len(paths)):
            paths[i] = paths[i].lower()
        # Get default filename
        filename = get_filename(self.get_title())
        if (self.get_sequence_total() > 1
                    and self.get_sequence_number() > 0
                    and self.get_sequence_title() is not None):
            # Set special filename if part of a sequence
            pad = len(str(self.get_sequence_total()))
            if pad == 1:
                pad = 2
            padded = pad_num(str(self.get_sequence_number()), pad)
            filename = padded + " " + get_filename(self.get_sequence_title())
            # Add section title if applicable
            if self.get_section_title() is not None:
                filename = filename + " - " + get_filename(self.get_section_title())
        # Use different scheme if filename already exists
        lower = filename.lower()
        if not lower == old and (lower + ".dvk" in paths or lower + ext in paths):
            filename = filename + " - " + self.get_artists()[0]
            lower = filename.lower()
            seed(self.get_dvk_id())
            while lower + ".dvk" in paths or lower + ext in paths:
                ver = str(randint(1, 9999))
                filename = get_filename(self.get_title()) + "_V" + ver
                lower = filename.lower()
        # Add suffix if for a secondary file
        if secondary:
            filename = filename + "_S"
        return filename

    def rename_files(self, filename:str=None, secondary:str=None):
        """
        Renames the DVK file and its associated media files.
        Retains all media file extensions.

        :param filename: Main filename to use when renaming, defaults to None
        :type filename: str, optional
        :param secondary: Filename to use for secondary media, defaults to None
        :type secondary: str, optional
        """
        # RENAME DVK FILE
        remove(self.get_dvk_file())
        parent = abspath(join(self.get_dvk_file(), pardir))
        file = join(parent, filename + ".dvk")
        self.set_dvk_file(file)
        # RENAME MEDIA FILE
        if not self.get_media_file() is None:
            from_file = self.get_media_file()
            to_file = filename + get_extension(basename(from_file))
            to_file = abspath(join(parent, to_file))
            # CHECK IF RENAME IS NEEDED
            if not basename(from_file) == to_file:
                try:
                    # RENAME TO TEMPORARY FILE
                    self.set_media_file("xXTeMpPrImXx.tmp")
                    rename(from_file, self.get_media_file())
                    # RENAME TO FINAL FILENAME
                    from_file = self.get_media_file()
                    self.set_media_file(to_file)
                    rename(from_file, self.get_media_file())
                except OSError as e:
                    self.set_media_file(to_file)
        # RENAME SECONDARY MEDIA FILE
        if not self.get_secondary_file() is None:
            from_file = self.get_secondary_file()
            to_file = secondary + get_extension(basename(from_file))
            to_file = abspath(join(parent, to_file))
            # CHECK IF RENAME IS NEEDED
            if not basename(from_file) == to_file:
                try:
                    # RENAME TO TEMPORARY FILE
                    self.set_secondary_file("xXTeMpSeCoNdXx.tmp")
                    rename(from_file, self.get_secondary_file())
                    # RENAME TO FINAL FILENAME
                    from_file = self.get_secondary_file()
                    self.set_secondary_file(to_file)
                    rename(from_file, to_file)
                except:
                    self.set_secondary_file(to_file)
        # REWRITE DVK FILE
        self.write_dvk()

    def delete_dvk(self):
        """
        Deletes the Dvk file and any linked media.
        """
        # Delete main Dvk file
        file = self.get_dvk_file()
        if file is not None and exists(file):
            remove(file)
        # Delete media file
        file = self.get_media_file()
        if file is not None and exists(file):
            remove(file)
        # Delete secondary media file
        file = self.get_secondary_file()
        if file is not None and exists(file):
            remove(file)

    def move_dvk(self, directory:str=None):
        """
        Moves DVK file and associated media to the given directory.

        :param directory: Directory to move files into, defauts to None
        :type directory: str, optional
        """
        # CHECK DIRECTORY IS VALID
        if directory is not None and exists(directory) and isdir(directory):
            # GET MEDIA FILES
            file = self.get_dvk_file()
            media = self.get_media_file()
            second = self.get_secondary_file()
            # CHANGE DVK FILE DIRECTORY
            filename = basename(file)
            self.set_dvk_file(join(directory, filename))
            try:
                # MOVE MEDIA FILE
                if media is not None and exists(media):
                    filename = basename(media)
                    self.set_media_file(filename)
                    move(media, self.get_media_file())
                # MOVE SECONDARY FILE
                if second is not None and exists(second):
                    filename = basename(second)
                    self.set_secondary_file(filename)
                    move(second, self.get_secondary_file())
                # MOVE DVK FILE
                if exists(file):
                    remove(file)
                self.write_dvk()
            except:
                self.set_dvk_file(file)

    def update_extensions(self):
        """
        Updates media file extensions to mach magic number file type.
        """
        if exists(self.get_dvk_file()):
            # GET PARENT DIRECTORY
            parent = abspath(join(self.get_dvk_file(), pardir))
            # MAIN MEDIA FILE
            media_file = self.get_media_file()
            if media_file is not None and exists(media_file):
                filename = basename(media_file)
                ext = get_extension(filename)
                filename = filename[: len(filename) - len(ext)]
                # DETERMINE ACTUAL FILE TYPE
                filetype = guess(self.get_media_file())
                if filetype is not None:
                    filename = filename + "." + filetype.extension
                    media_file = abspath(join(parent, filename))
                # RENAME FILES
                if not self.get_media_file() == media_file:
                    rename(self.get_media_file(), media_file)
                    self.set_media_file(basename(media_file))
            # MAIN SECONDARY FILE
            secondary_file = self.get_secondary_file()
            if secondary_file is not None and exists(secondary_file):
                filename = basename(secondary_file)
                ext = get_extension(filename)
                filename = filename[: len(filename) - len(ext)]
                # DETERMINE ACTUAL FILE TYPE
                filetype = guess(self.get_secondary_file())
                if filetype is not None:
                    filename = filename + "." + filetype.extension
                    secondary_file = abspath(join(parent, filename))
                # RENAME FILES
                if not self.get_secondary_file() == secondary_file:
                    rename(self.get_secondary_file(), secondary_file)
                    self.set_secondary_file(basename(secondary_file))
            # WRITE DVK
            self.write_dvk()
