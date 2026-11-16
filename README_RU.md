# NEXIUM External v1.1.0 — стартовый проект

Это стартовый Android-проект на Python 3 + Kivy. В нём есть меню RAGE, LEGIT,
VISUALS, SKINS, MISC и CONFIGS, локальное сохранение настроек JSON и
демонстрационные элементы интерфейса.

**Важно:** проект не подключается к Standoff 2, не читает/изменяет память игры,
не реализует автоматическое наведение, стрельбу, ESP против реальных игроков
или обход античита. Разделы RAGE/LEGIT — только демонстрационные настройки.

## Сборка APK

Рекомендуется Linux или WSL2 (Buildozer не предназначен для нативной сборки
из обычной Windows CMD).

1. Установите Python 3, Java JDK, Git и системные зависимости Buildozer.
2. В каталоге проекта создайте виртуальное окружение и активируйте его.
3. Установите зависимости:

   `pip install --upgrade pip setuptools wheel`

   `pip install buildozer cython`

4. Запустите:

   `buildozer android debug`

5. APK появится в каталоге `bin/`.

При первой сборке Buildozer скачает Android SDK/NDK и Gradle — это может занять
время. Для публикации потребуется отдельная release-сборка и подпись APK.

## Запуск на компьютере для проверки UI

`pip install -r requirements.txt`
`python main.py`

Настройки сохраняются в локальный файл приложения `nexium_config.json`.
