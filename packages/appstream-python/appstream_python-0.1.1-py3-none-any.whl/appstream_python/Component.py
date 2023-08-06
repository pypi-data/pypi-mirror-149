from platform import release
from .StandardConstants import *
from typing import Optional
from lxml import etree
import datetime


class TranslateableTag:
    def __init__(self) -> None:
        self._text = ""
        self._translations: dict[str, str] = {}

    def get_default_text(self) -> str:
        """Returns the untranslated text"""
        return self._text

    def set_default_text(self, text: str) -> None:
        """Sets the untranslated text"""
        self._text = text

    def get_translated_text(self, lang: str) -> Optional[str]:
        """Returns the translated text"""
        return self._translations.get(lang, None)

    def set_translated_text(self, lang: str, text: str) -> None:
        """Sets the translated text"""
        self._translations[lang] = text

    def get_aviable_languages(self) -> list[str]:
        """Returns a list with all languages of the tag"""
        return list(self._translations.keys())

    def load_tags(self, tag_list: list[etree.Element]) -> None:
        """Load a list of Tags"""
        for i in tag_list:
            if i.get("{http://www.w3.org/XML/1998/namespace}lang") is None:
                self._text = i.text
            else:
                self._translations[i.get("{http://www.w3.org/XML/1998/namespace}lang")] = i.text

    def write_tags(self, parent_tag: etree.Element, tag_name: str) -> None:
        """Writes a Tag"""
        default_tag = etree.SubElement(parent_tag, tag_name)
        default_tag.text = self._text

        for key, value in self._translations.items():
            translation_tag = etree.SubElement(parent_tag, tag_name)
            translation_tag.set("{http://www.w3.org/XML/1998/namespace}lang", key)
            translation_tag.text = value

    def clear(self):
        """Resets all data"""
        self._text = ""
        self._translations.clear()

    def __repr__(self) -> str:
        return f"<TranslateableTag default='{self._text}'>"


class TranslateableList:
    def __init__(self) -> None:
        self.default_list = []
        self.translated_lists = {}

    def get_default_list(self) -> list[str]:
        "Returns a list with the defualt items"
        return self.default_list

    def load_tag(self, tag: etree.Element):
        """Loads a Tag"""
        if tag.get("{http://www.w3.org/XML/1998/namespace}lang") is None:
            for i in tag.getchildren():
                if i.get("{http://www.w3.org/XML/1998/namespace}lang") is None:
                    self.default_list.append(i.text)
                else:
                    if i.get("{http://www.w3.org/XML/1998/namespace}lang") not in self.translated_lists:
                        self.translated_lists[i.get("{http://www.w3.org/XML/1998/namespace}lang")] = []
                    self.translated_lists[i.get("{http://www.w3.org/XML/1998/namespace}lang")].append(i.text)
        else:
            if tag.get("{http://www.w3.org/XML/1998/namespace}lang") not in self.translated_lists:
                self.translated_lists[tag.get("{http://www.w3.org/XML/1998/namespace}lang")] = []
            for i in tag.getchildren():
                self.translated_lists[tag.get("{http://www.w3.org/XML/1998/namespace}lang")].append(i.text)

    def write_all_tag(self, parent_tag: etree.Element, tag_name: str) -> None:
        for i in range(len(self.default_list)):
            default_tag = etree.SubElement(parent_tag, tag_name)
            default_tag.text = self.default_list[i]

    def clear(self):
        """Resets all data"""
        self.default_list.clear()
        self.translated_lists.clear()


class DescriptionItem:
    def get_type(self) -> str:
        return "none"

    def load_tags(self, tag_list: list[etree.Element]) -> None:
        raise NotImplementedError

    def get_tags(self, parent_tag: etree.Element) -> None:
        raise NotImplementedError()


class DescriptionParagraph(DescriptionItem):
    def __init__(self) -> None:
        self.content = TranslateableTag()
        """The Text of the Paragraph"""

    def get_type(self) -> str:
        return "paragraph"

    def load_tags(self, tag_list: list[etree.Element]) -> None:
        self.content.load_tags(tag_list)

    def get_tags(self, parent_tag: etree.Element) -> None:
        self.content.write_tags(parent_tag, "p")


class DescriptionList(DescriptionItem):
    def __init__(self, list_type: str) -> None:
        self._list_type = list_type

        self.content: TranslateableList = TranslateableList()
        "The list"

    def get_type(self) -> str:
        if self.list_type == "ul":
            return "unordered-list"
        else:
            return "ordered-list"

    def load_tags(self, tag_list: list[etree.Element]) -> None:
        self.content.load_tag(tag_list)

    def get_tags(self, parent_tag: etree.Element) -> None:
        self.content.write_all_tag(parent_tag, self._list_type)


class Description:
    def __init__(self) -> None:
        self.items: list[DescriptionItem] = []
        """All Description Items"""

    def load_tags(self, tag: etree.Element):
        paragraph_list: list[etree.Element] = []
        for i in tag.getchildren():
            if i.tag == "p":
                if i.get("{http://www.w3.org/XML/1998/namespace}lang") is not None:
                    paragraph_list.append(i)
                else:
                    if len(paragraph_list) != 0:
                        paragraph_item = DescriptionParagraph()
                        paragraph_item.load_tags(paragraph_list)
                        self.items.append(paragraph_item)
                    paragraph_list.clear()
                    paragraph_list.append(i)
            else:
                if len(paragraph_list) != 0:
                    paragraph_item = DescriptionParagraph()
                    paragraph_item.load_tags(paragraph_list)
                    self.items.append(paragraph_item)

                list_item = DescriptionList(i.tag)
                list_item.load_tags(i)
                self.items.append(list_item)

        if len(paragraph_list) != 0:
            paragraph_item = DescriptionParagraph()
            paragraph_item.load_tags(paragraph_list)
            self.items.append(paragraph_item)

    def get_tags(self, parent_tag: etree.Element):
        description_tag = etree.SubElement(parent_tag, "description")
        for i in self.items:
            i.get_tags(description_tag)


class Release:
    def __init__(self) -> None:
        self.version: str = ""
        "The version"

        self.date: Optional[datetime.date]
        "The date"

    def load_tag(self, tag: etree.Element):
        "Loads a release tag"

        self.version = tag.get("version") or ""

        try:
            self.date = datetime.date.fromisoformat(tag.get("date"))
        except Exception:
            pass

        try:
            self.date = datetime.date.fromtimestamp(int(tag.get("timestamp")))
        except Exception:
            pass


class AppstreamComponent:
    def __init__(self) -> None:
        self.id: str = ""
        "The component ID"

        self.type: str = "desktop"
        "The type"

        self.name: TranslateableTag = TranslateableTag()
        "The component name"

        self.developer_name: TranslateableTag = TranslateableTag()
        "The developer name"

        self.summary: TranslateableTag = TranslateableTag()
        "The component summary"

        self.description: Description = Description()
        "The description"

        self.metadata_license: str = ""
        "The metadata license"

        self.project_license: str = ""
        "The project license"

        self.urls: dict[str, str] = {}
        "The URLs"

        self.oars: dict[str, str] = {}
        "The content rating"

        self.categories: list[str] = []
        "The categories"

        self.provides: dict[str, str] = {}
        "The provides. The content of the depracted mimetype tag goes intp provides['mimetype']"

        for i in PROVIDES_TYPES:
            self.provides[i] = []

        self.releases: list[Release] = []
        "The releases"

        self.project_group: Optional[str] = None
        "The project group"

        self.translation: list[dict[str, str]] = []
        "The translations"

        self.languages: dict[str, int] = {}
        "The languages"

        self.keywords: TranslateableList = TranslateableList()
        "The Keywords"

        self.kudos: list[str] = []
        "The Kudos"

        self.update_contact: Optional[str] = None
        "The update contact"

        self.extends: list[str] = []
        "The extends tag for addons"

    def clear(self) -> None:
        """Resets the Component"""
        self.id = ""
        self.type = "desktop"
        self.name.clear()
        self.developer_name.clear()
        self.summary.clear()
        self.description.items.clear()
        self.metadata_license = ""
        self.project_license = ""
        self.categories.clear()
        self.urls.clear()
        self.oars.clear()
        self.provides.clear()
        self.releases.clear()
        self.project_group = None
        self.translation.clear()
        self.languages.clear()
        self.keywords.clear()
        self.kudos.clear()
        self.update_contact = None
        self.extends.clear()

        for i in PROVIDES_TYPES:
            self.provides[i] = []

    def get_aviable_languages(self) -> list[str]:
        "Returns a list with all aviable languages of the Component"
        lang_list = self.name.get_aviable_languages() + self.summary.get_aviable_languages() + self.developer_name.get_aviable_languages()
        return list(set(lang_list))

    def parse_component_tag(self, tag: etree._ElementTree) -> None:
        self.id = tag.find("id").text

        try:
            self.type = tag.xpath("/component")[0].get("type")
        except IndexError:
            self.type = tag.get("type")

        self.name.load_tags(tag.findall("name"))

        self.developer_name.load_tags(tag.findall("developer_name"))

        self.summary.load_tags(tag.findall("summary"))

        description_tag = tag.find("description")
        if description_tag is not None:
            self.description.load_tags(description_tag)

        metadata_license_tag = tag.find("metadata_license")
        if metadata_license_tag is not None:
            self.metadata_license = metadata_license_tag.text

        project_license_tag = tag.find("project_license")
        if project_license_tag is not None:
            self.project_license = project_license_tag.text

        categories_tag = tag.find("categories")
        if categories_tag is not None:
            for i in categories_tag.findall("category"):
                self.categories.append(i.text)

        for i in tag.findall("url"):
            if i.get("type") in URL_TYPES:
                self.urls[i.get("type")] = i.text

        oars_tag = tag.find("content_rating")
        if oars_tag is not None:
            for i in oars_tag.findall("content_attribute"):
                if i.get("id") in OARS_ATTRIBUTE_TYPES and i.text in OARS_VALUE_TYPES:
                    self.oars[i.get("id")] = i.text

        categories_tag = tag.find("categories")
        if categories_tag is not None:
            for i in categories_tag.findall("category"):
                self.categories.append(i.text)

        provides_tag = tag.find("provides")
        if provides_tag is not None:
            for i in provides_tag.getchildren():
                if i.tag in PROVIDES_TYPES:
                    self.provides[i.tag].append(i.text)

        # For backwards compatibility. See: https://www.freedesktop.org/software/appstream/docs/chap-Metadata.html#tag-mimetypes
        mimetypes_tag = tag.find("mimetypes")
        if mimetypes_tag is not None:
            for i in mimetypes_tag.findall("mimetype"):
                self.provides["mediatype"].append(i.text)

        releases_tag = tag.find("releases")
        if releases_tag is not None:
            for i in releases_tag.findall("release"):
                release_object = Release()
                release_object.load_tag(i)
                self.releases.append(release_object)

        project_group_tag = tag.find("project_group")
        if project_group_tag is not None:
            self.project_group = project_group_tag.text

        for i in tag.findall("translation"):
            trans_dict = {}
            trans_dict["type"] = i.get("type")
            trans_dict["value"] = i.text
            self.translation.append(trans_dict)

        languages_tag = tag.find("languages")
        if languages_tag is not None:
            for i in languages_tag.findall("lang"):
                try:
                    self.languages[i.text] = int(i.get("percentage") or 100)
                except ValueError:
                    pass

        for i in tag.findall("keywords"):
            self.keywords.load_tag(i)

        kudos_tag = tag.find("kudos")
        if kudos_tag is not None:
            for i in kudos_tag.findall("kudo"):
                self.kudos.append(i.text)

        update_contact_tag = tag.find("update_contact")
        if update_contact_tag is not None:
            self.update_contact = update_contact_tag.text

        for i in tag.findall("extends"):
            self.extends.append(i.text)

    def load_file(self, path: str) -> None:
        """Load a appdata.xml or metainfo.xml file"""
        root = etree.parse(path)
        self.parse_component_tag(root)

    def get_component_tag(self) -> etree.Element:
        tag = etree.Element("component")
        tag.set("type", self.type)

        id_tag = etree.SubElement(tag, "id")
        id_tag.text = self.id

        self.name.write_tags(tag, "name")

        self.developer_name.write_tags(tag, "developer_name")

        self.summary.write_tags(tag, "summary")

        self.description.get_tags(tag)

        metadata_license_tag = etree.SubElement(tag, "metadata_license")
        metadata_license_tag.text = self.metadata_license

        project_license_tag = etree.SubElement(tag, "project_license")
        project_license_tag.text = self.project_license

        for key, value in self.urls.items():
            if key in URL_TYPES:
                url_tag = etree.SubElement(tag, "url")
                url_tag.set("type", key)
                url_tag.text = value

        oars_tag = etree.SubElement(tag, "content_rating")
        oars_tag.set("type", "oars-1.1")
        for key, value in self.oars.items():
            if key in OARS_ATTRIBUTE_TYPES and value in OARS_VALUE_TYPES:
                single_oars_tag = etree.SubElement(oars_tag, "content_attribute")
                single_oars_tag.set("id", key)
                single_oars_tag.text = value

        if len(self.categories) > 0:
            categories_tag = etree.SubElement(tag, "categories")
            for i in self.categories:
                single_categorie_tag = etree.SubElement(categories_tag, "category")
                single_categorie_tag.text = i

        provides_tag = etree.SubElement(tag, "provides")
        for key, value in self.provides.items():
            if key not in PROVIDES_TYPES:
                continue
            for i in value:
                single_provides_tag = etree.SubElement(provides_tag, key)
                single_provides_tag.text = i
        # Don't write empty provides tag
        if len(provides_tag.getchildren()) == 0:
            tag.remove(provides_tag)

        if self.project_group:
            project_group_tag = etree.SubElement(tag, "project_group")
            project_group_tag.text = self.project_group

        for i in self.translation:
            translation_tag = etree.SubElement(tag, "translation")
            translation_tag.set("type", i["type"])
            translation_tag.text = i["value"]

        if len(self.languages) > 0:
            languages_tag = etree.SubElement(tag, "languages")
            for key, value in self.languages.items():
                single_language_tag = etree.SubElement(languages_tag, "lang")
                single_language_tag.set("percentage", str(value))
                single_language_tag.text = key

        if len(self.kudos) > 0:
            kudos_tag = etree.SubElement(tag, "kudos")
            for i in self.kudos:
                single_kudos_tag = etree.SubElement(kudos_tag, "kudo")
                single_kudos_tag.text = i

        if self.update_contact:
            update_contact_tag = etree.SubElement(tag, "update_contact")
            update_contact_tag.text = self.update_contact

        for i in self.extends:
            extends_tag = etree.SubElement(tag, "extends")
            extends_tag.text = i

        return tag

    def get_xml_string(self) -> str:
        """Returns the XML data of the Component as string"""
        return etree.tostring(self.get_component_tag(), pretty_print=True, encoding="utf-8").decode("utf-8")

    def save_file(self, path: str) -> None:
        """Saves the Component as XML file"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(etree.tostring(self.get_component_tag(), pretty_print=True, xml_declaration=True, encoding="utf-8").decode("utf-8"))

    def __repr__(self) -> str:
        return f"<AppstreamComponent id='{self.id}'>"
