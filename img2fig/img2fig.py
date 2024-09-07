from markdown import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import ImageInlineProcessor, IMAGE_LINK_RE
from markdown.extensions.attr_list import AttrListTreeprocessor
from xml.etree import ElementTree as etree
import re


class Img2FigProcessor(ImageInlineProcessor):

    def __init__(
        self,
        pattern: str,
        md: Markdown | None = None,
        source_attr: str = "title",
        remove_attr: bool = True,
        force_convert: bool = True,
        empty_as_none: bool = True,
    ):
        super().__init__(pattern, md)
        if source_attr not in ["title", "alt"]:
            raise ValueError(f"Invalid source_attr '{source_attr}'")
        self.source_attr: str = source_attr
        self.another_attr: str = "alt" if source_attr == "title" else "title"
        self.remove_attr: bool = remove_attr
        self.force_convert: bool = force_convert
        self.empty_as_none: bool = empty_as_none

    def handleMatch(
        self, m: re.Match[str], data: str
    ) -> tuple[etree.Element | None, int | None, int | None]:
        """![alt](src "title") -> <figure>"""
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None
        alt: str = self.unescape(text)

        src, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        caption: str | None
        another: str | None
        if self.source_attr == "title":
            caption = title
            another = alt
        elif self.source_attr == "alt":
            caption = alt
            another = title
        else:
            assert False

        if self.empty_as_none:
            if caption == "":
                caption = None

        if caption is None and not self.force_convert:
            return None, None, None

        figure = etree.Element("figure")
        img = etree.SubElement(figure, "img")
        img.set("src", src)
        if another is not None:
            img.set(self.another_attr, another)
        if caption is not None and not self.remove_attr:
            img.set(self.source_attr, caption)

        if caption is not None:
            figcaption = etree.SubElement(figure, "figcaption")
            figcaption.text = caption

        # ======== From evidlo/markdown_captions ========

        # if attr_list is enabled, put '{: xxx}' inside <figure> at end
        # so attr_list will see it
        if "attr_list" in self.md.treeprocessors:
            # find attr_list curly braces
            curly = re.match(AttrListTreeprocessor.BASE_RE, data[index:])
            if curly:
                figure[-1].tail = "\n"
                figure[-1].tail += curly.group()
                # remove original '{: xxx}'
                index += curly.end()

        return figure, m.start(0), index


class Img2FigExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            "source_attr": [
                "title",
                "Use 'title' or 'alt' attribute as the caption.",
            ],
            "remove_attr": [
                True,
                "Remove the alt/title attribute after conversion.",
            ],
            "force_convert": [
                True,
                "Convert all <img> to <figure>, missing alt/title will cause a <figure> without <figcaption>. If false, img will be left as is.",
            ],
            "empty_as_none": [
                True,
                "Treat empty alt/title as if they don't exist",
            ],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            Img2FigProcessor(
                IMAGE_LINK_RE,
                md,
                source_attr=self.getConfig("source_attr"),
                remove_attr=self.getConfig("remove_attr"),
                force_convert=self.getConfig("force_convert"),
                empty_as_none=self.getConfig("empty_as_none"),
            ),
            "img2fig",
            151.2374,
        )


def makeExtension(**kwargs) -> Img2FigExtension:
    return Img2FigExtension(**kwargs)
