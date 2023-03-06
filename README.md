# new shvatka bot

[![wakatime](https://wakatime.com/badge/github/bomzheg/ShvatkaBot.svg)](https://wakatime.com/badge/github/bomzheg/ShvatkaBot)

Движок для ночной поисковой игры [Схватка](https://ru.wikipedia.org/wiki/%D0%A1%D1%85%D0%B2%D0%B0%D1%82%D0%BA%D0%B0_(%D0%B8%D0%B3%D1%80%D0%B0)) (похожа на Дозоры, Энакунтер)

Позволяет проводить планировать и проводить игры.

Core-функционал: 
- редактор сценария игры, 
- управление подготовкой к игре, 
- формирование команды капитаном, 
- назначение заместителей капитана с разными полномочиями, 
- сборка заявок на игру, 
- проведение игры, 
- информирование организаторов о ходе игры, 
- формирование результатов игры, 
- сохранение статистики прошедших игр


## Как запустить:
```shell
poetry build
pip install ./dist/shvatka-0.1.0-py3-none-any.whl
export BOT_PATH=$PWD
shvatka-tgbot
```
