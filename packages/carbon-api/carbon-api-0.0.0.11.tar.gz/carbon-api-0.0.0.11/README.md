# Carbon

> A star ⭐ from you means a lot

Create beautiful carbon code images using python or terminal.

This is an unofficial asynchronous python wrapper for carbon.now.sh which can be also be used inside cli.

## Installation

### PyPI (recommended)

```shell
pip install carbon-api
```

### Directly from Source

```shell
git clone https://github.com/StarkBotsIndustries/Carbon

cd Carbon

python setup.py install
```

## Example

![Example Carbon Image](assets/carbon.png)

## Usage

### Using as an Asynchronous Library

```python
import asyncio
from carbon import Carbon

client = Carbon()


async def main():
    img = await client.create("Your code here")
    print(img)


asyncio.run(main())
```

## Options

You can pass globally usable options' values to `Carbon` class

```python
from carbon import Carbon

client = Carbon(
    downloads_dir=os.getcwd(),  # Defaults to current directory
    colour="rgba(171, 184, 195, 1)",  # Hex or rgba color
    shadow=True,  # Turn on/off shadow
    shadow_blur_radius="68px",
    shadow_offset_y="20px",
    export_size="2x",  # resolution of exported image, e.g. 1x, 3x
    font_size="14px",
    font_family= "Hack",  # font family, e.g. JetBrains Mono, Fira Code.
    first_line_number=1,
    language="auto",  # programing language for properly highlighting
    line_numbers=False,  # turn on/off, line number
    horizontal_padding="56px",
    vertical_padding="56px",
    theme="seti",  # code theme
    watermark=False,  # turn on/off watermark
    width_adjustment=True,  # turn on/off width adjustment
    window_controls= True,  # turn on/off window controls
    window_theme=None
)
```

Same options are also available in `Carbon.create` method, which override the global options.

You can also specify the file name to the create method. Relative Path to the image will be returned by the function.

```python
path = client.create(file="my-code.png")  # Path will be downloads_dir/file 
print(path)
```

### Using CLI

```shell
$ carbon-app

Create beautiful carbon code images using python or terminal

Options:
  -v, --version         check the current version installed
  -f FILE, --file FILE  pass file path to read code from
  -c CODE, --code CODE  pass some code to make carbon

Enjoy the program :)

```

You can pass the file path using the file argument.

```shell
carbon-app --file file_path
```

or simply

```shell
carbon-app -f file_path
```

You can also directly pass code (not recommended)

```shell
carbon-app --code your_code_here
```

or simply

```shell
carbon-app -c your_code_here
```

CLI is in beta version therefore other options aren't available currently.

## Credits

- [cyberboysumanjay](https://github.com/cyberboysumanjay) for [Carbon-API](https://github.com/cyberboysumanjay/Carbon-API).

## Community and Support

Telegram Channel - [StarkBots](https://t.me/StarkBots)

Telegram Chat - [StarkBotsChat](https://t.me/StarkBotsChat)

## Copyright and License

- Copyright (C) 2022 **Stark Bots** <<https://github.com/StarkBotsIndustries>>

- Licensed under the terms of [GNU Lesser General Public License v3 or later (LGPLv3+)](https://github.com/StarkBotsIndustries/Carbon/blob/master/LICENSE)
