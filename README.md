## Установка зависимостей


Входим в venv
```bash

$ ./.venv/Scripts/Activate.ps1  

```

Установка
```bash
$ pip install -r requirements.txt  
```

## Запуск
Перед выполнением убедитесь, что вы создали **.env** на основе **.env.example**.

```bash
python -m app
```

## Тесты
Запуск в виртуальной среде
```bash
$ pytest
```