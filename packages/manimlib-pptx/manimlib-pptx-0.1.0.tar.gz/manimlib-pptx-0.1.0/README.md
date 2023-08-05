# MANIMLIB-PPTX

A Manimlib (the one from 3b1b) addon which exports the video as a powerpoint

> See [manim-pptx](https://github.com/RythenGlyth/manim-pptx) for manim community edition

## Table of Contents

-  [Installation](#installation)
-  [Usage](#usage)
    -  [Example](#example)
-  [Contributing](#contributing)
-  [Credit](#credit)

## Installation

> ``pip install manimlib-pptx``

## Usage

To export as pptx make your scene class inherit from `PPTXScene`

You can then call `self.endSlide()` to add all animations since the last `endSlide()`.

The `endSlide` method has also two arguments:

- `loop` - loops the whole Slide.
- `autonext` - automatically advances to the next slide when the current slide is done animating
- `notes` - notes which should be displayed on the created Slide
- `shownextnotes` - show the notes of the next slide in the notes of the current slide

> Note: You need to use the `-w, --write_file` flag otherwise it will throw an error. Pull-requests are welcome.

### Example

```python
from manim_pptx import *
from manimlib import *

class TestScene(PPTXScene):
    def construct(self):

        t = Tex("Hello World!")
        self.play(Write(t, run_time=2))
        self.endSlide()
        
        c = Circle(radius=3)
        self.play(Create(c))
        d = Dot()
        d.move_to(c.get_start())
        self.play(Write(d))
        self.endSlide(autonext=True, shownextnotes=True)

        self.play(MoveAlongPath(d, c))
        self.endSlide(loop=True, notes="Next Animation displays Bye")

        self.play(*[FadeOut(m) for m in self.mobjects])

        t2 = Tex("Bye!")
        self.play(Write(t2, run_time=1))
        self.endSlide()
```

## Contribution

Feel free to contribute and create pull requests.

## Credit
Credit to both [manim-presentation](https://github.com/galatolofederico/manim-presentation) and [manim-pptx](https://github.com/yoshiask/manim-pptx) where i stole some good ideas and a bit of code