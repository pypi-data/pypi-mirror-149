# ASCII Art

Create amazing ASCII arts on-the-fly with `asciify-it` Python package!

## Features
- Algorithm for image transformation into an ASCII art!
- Python library `asciify` with command line interface (powered by `click`)
- `Flask` server application
- Deployed on [Heroku](https://web-asciify.herokuapp.com)

## Dependencies
- click
- nptyping
- numpy
- Pillow
- tqdm

## Interface draft
- можно будет пикать язык веб-сервиса
- примерный вариант вызова из командной строки
`$ asciify mylittlepony.png -w 45 -h 43 -o result.txt -f path/to/arial.ttf -s 48 -q`
- на сервере будет окошко для работы с картинкой

![Здесь должна быть картинка](misc/server_interface.png "Вот так это будет выглядеть на серваке")

## Authors
- [AArtur](https://gitlab.com/AAArtur)
- [Mathematician2000](https://gitlab.com/Mathematician2000)
