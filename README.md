# Markdown img2fig

Convert inline markdown images to captioned figures.

Inspirated by [markdown-img2fig](https://github.com/Evidlo/markdown_captions) and [yafg](https://git.sr.ht/~ferruck/yafg).

## Installation

``` bash
pip install markdown-img2fig
```

## Usage

### Markdown module
``` python
import markdown
import img2fig

data = markdown.markdown(
    md,
    extensions=[
        img2fig.Img2FigExtension(
            source_attr="title",
            remove_attr=True,
            force_convert=True,
            empty_as_none=True,
        ),
        'attr_list',  # optional
    ]
)
```

### MkDocs `mkdocs.yml`
``` yaml
markdown_extensions:
  - img2fig:
      source_attr: title
      remove_attr: true
      force_convert: true
      empty_as_none: true
  - attr_list # optional
```

### Result
``` md
![Alt text](image.jpg "Title text"){: .someclass }
```
``` html
<figure class="someclass">
    <img alt="Alt text" src="image.jpg" />
    <figcaption>Title text</figcaption>
</figure>
```


## Options

- `source_attr` (default: 'title')<br>
  Use 'title' or 'alt' attribute as the caption.
- `remove_attr` (default: True)<br>
  Remove the alt/title attribute after conversion.
- `force_convert` (default: True)<br>
  Convert all images to figures, missing alt/title will cause figures without figcaptions.<br>
  If false, images will be left as is.
- `empty_as_none` (default: True)<br>
  Treat empty alt/title as if they don't exist.

## License

Licensed under the MIT License.
