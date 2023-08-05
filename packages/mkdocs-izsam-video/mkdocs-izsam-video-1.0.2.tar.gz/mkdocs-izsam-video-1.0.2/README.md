# MkDocs IZSAM Video

This plugin is based on the Mikalai Lisitsa idea, please visit the page of the project at [https://pypi.org/project/mkdocs-video/](https://pypi.org/project/mkdocs-video/).

The plugin allows you to embed videos on the documentation pages using a simple Markdown syntax. Unlike the Mikalai Lisitsa it embeds video not in an `<iframe>` but in a `<video>` and for the moment YouTube or third parties videos embed are not allowed.

## Installation

Install the package with pip:

```bash
$ pip install mkdocs-izsam-video
```

Enable the plugin in the `mkdocs.yml` file:

```yaml
plugins:
    - mkdocs-izsam-video
```

> See how to use [MkDocs Plugins](https://www.mkdocs.org/dev-guide/plugins/#using-plugins)

## Usage

To add a video to the final documentation page, you need to use the Markdown syntax for images with a **specific name** *(hereinafter ***marker***)*.

> See how to use [Markdown syntax](https://guides.github.com/features/mastering-markdown/)

**Example:**

*content folder structure*

```
├── content
|   ├── ...
│   ├── video.md
│       └── videos
│           └── your-video.mp4
└── mkdocs.yml
```

*video.md*

Use relative paths for videos stored together with your content

```
# Video example

Lorem ipsum dolor sit amet

![type:video-tag](./videos/your-video.mp4)
```

## Configuration

### Marker

By default, the string `type:video-tag` is used as a **marker** in the Markdown syntax.

You can change this value by adding the following lines to your `mkdocs.yml`:

```yaml
plugins:
  - mkdocs-izsam-video:
      mark: "your-marker"
```

Now you can use this **marker** in the Markdown syntax:

```
![your-marker](./videos/your-video.mp4)
```

### Marker

By default, the following CSS styles are used for the `<video>` tag that is inserted into the final page:

```css
width: 100%;
```

You can change the style by adding the following lines to your mkdocs.yml:



## License

The MIT License (MIT)

Copyright (c) 2021 Alessandro De Luca

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
