import flet as ft  # Импортируем фреймворк Flet для создания UI

class AppStyles:  # Класс для централизованного хранения всех стилей приложения
    PAGE_SETTINGS = {  # Настройки главной страницы приложения
        "title": "AI Chat",  # Заголовок окна приложения
        "vertical_alignment": ft.MainAxisAlignment.CENTER,  # Вертикальное выравнивание по центру
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,  # Горизонтальное выравнивание по центру
        "padding": 20,  # Отступы от краев окна
        "bgcolor": ft.Colors.GREY_900,  # Темно-серый цвет фона
        "theme_mode": ft.ThemeMode.DARK,  # Темная тема оформления
    }

    CHAT_HISTORY = {  # Настройки для области истории чата
        "expand": True,  # Разрешаем расширение на доступное пространство
        "spacing": 10,  # Отступ между сообщениями
        "height": 400,  # Высота области чата
        "auto_scroll": True,  # Автоматическая прокрутка к новым сообщениям
        "padding": 20,  # Внутренние отступы
    }

    MESSAGE_INPUT = {  # Настройки поля ввода сообщений
        "width": 400,  # Ширина поля ввода
        "height": 50,  # Высота поля ввода
        "multiline": False,  # Однострочный режим ввода
        "text_size": 16,  # Размер шрифта
        "color": ft.Colors.WHITE,  # Цвет текста
        "bgcolor": ft.Colors.GREY_800,  # Цвет фона поля ввода
        "border_color": ft.Colors.BLUE_400,  # Цвет границы
        "cursor_color": ft.Colors.WHITE,  # Цвет курсора
        "content_padding": 10,  # Внутренние отступы
        "border_radius": 8,  # Скругление углов
        "hint_text": "Введите сообщение здесь...",  # Подсказка в пустом поле
        "shift_enter": True,  # Включение отправки по Shift+Enter
    }

    SEND_BUTTON = {  # Настройки кнопки отправки
        "text": "Отправка",  # Текст на кнопке
        "icon": ft.icons.SEND,  # Иконка отправки
        "style": ft.ButtonStyle(  # Стиль кнопки
            color=ft.Colors.WHITE,  # Цвет текста
            bgcolor=ft.Colors.BLUE_700,  # Цвет фона
            padding=10,  # Внутренние отступы
        ),
        "tooltip": "Отправить сообщение",  # Всплывающая подсказка
        "height": 40,  # Высота кнопки
        "width": 130,  # Ширина кнопки
    }

    SAVE_BUTTON = {  # Настройки кнопки сохранения
        "text": "Сохранить",  # Текст на кнопке
        "icon": ft.icons.SAVE,  # Иконка сохранения
        "style": ft.ButtonStyle(  # Стиль кнопки
            color=ft.Colors.WHITE,  # Цвет текста
            bgcolor=ft.Colors.BLUE_700,  # Цвет фона
            padding=10,  # Внутренние отступы
        ),
        "tooltip": "Сохранить диалог в файл",  # Всплывающая подсказка
        "width": 130,  # Ширина кнопки
        "height": 40,  # Высота кнопки
    }

    CLEAR_BUTTON = {  # Настройки кнопки очистки
        "text": "Очистить",  # Текст на кнопке
        "icon": ft.icons.DELETE,  # Иконка удаления
        "style": ft.ButtonStyle(  # Стиль кнопки
            color=ft.Colors.WHITE,  # Цвет текста
            bgcolor=ft.Colors.RED_700,  # Красный цвет фона
            padding=10,  # Внутренние отступы
        ),
        "tooltip": "Очистить историю чата",  # Всплывающая подсказка
        "width": 130,  # Ширина кнопки
        "height": 40,  # Высота кнопки
    }

    ANALYTICS_BUTTON = {  # Настройки кнопки аналитики
        "text": "Аналитика",  # Текст на кнопке
        "icon": ft.icons.ANALYTICS,  # Иконка аналитики
        "style": ft.ButtonStyle(  # Стиль кнопки
            color=ft.Colors.WHITE,  # Цвет текста
            bgcolor=ft.Colors.GREEN_700,  # Зеленый цвет фона
            padding=10,  # Внутренние отступы
        ),
        "tooltip": "Показать аналитику",  # Всплывающая подсказка
        "width": 130,  # Ширина кнопки
        "height": 40,  # Высота кнопки
    }

    INPUT_ROW = {  # Настройки строки ввода
        "spacing": 10,  # Отступ между элементами
        "alignment": ft.MainAxisAlignment.SPACE_BETWEEN,  # Выравнивание с распределением пространства
        "width": 920,  # Общая ширина строки
    }

    CONTROL_BUTTONS_ROW = {  # Настройки строки с кнопками управления
        "spacing": 20,  # Отступ между кнопками
        "alignment": ft.MainAxisAlignment.CENTER,  # Выравнивание по центру
    }

    CONTROLS_COLUMN = {  # Настройки колонки с элементами управления
        "spacing": 20,  # Отступ между элементами
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,  # Горизонтальное выравнивание по центру
    }

    MAIN_COLUMN = {  # Настройки главной колонки
        "expand": True,  # Разрешаем расширение
        "spacing": 20,  # Отступ между элементами
        "alignment": ft.MainAxisAlignment.CENTER,  # Вертикальное выравнивание по центру
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,  # Горизонтальное выравнивание по центру
    }

    MODEL_SEARCH_FIELD = {  # Настройки поля поиска модели
        "width": 400,  # Ширина поля
        "border_radius": 8,  # Скругление углов
        "bgcolor": ft.Colors.GREY_900,  # Цвет фона
        "border_color": ft.Colors.GREY_700,  # Цвет границы
        "color": ft.Colors.WHITE,  # Цвет текста
        "content_padding": 10,  # Внутренние отступы
        "cursor_color": ft.Colors.WHITE,  # Цвет курсора
        "focused_border_color": ft.Colors.BLUE_400,  # Цвет границы при фокусе
        "focused_bgcolor": ft.Colors.GREY_800,  # Цвет фона при фокусе
        "hint_style": ft.TextStyle(  # Стиль текста-подсказки
            color=ft.Colors.GREY_400,  # Цвет подсказки
            size=14,  # Размер шрифта
        ),
        "prefix_icon": ft.icons.SEARCH,  # Иконка поиска
        "height": 45,  # Высота поля
    }

    MODEL_DROPDOWN = {  # Настройки выпадающего списка моделей
        "width": 400,  # Ширина списка
        "height": 45,  # Высота списка
        "border_radius": 8,  # Скругление углов
        "bgcolor": ft.Colors.GREY_900,  # Цвет фона
        "border_color": ft.Colors.GREY_700,  # Цвет границы
        "color": ft.Colors.WHITE,  # Цвет текста
        "content_padding": 10,  # Внутренние отступы
        "focused_border_color": ft.Colors.BLUE_400,  # Цвет границы при фокусе
        "focused_bgcolor": ft.Colors.GREY_800,  # Цвет фона при фокусе
    }

    MODEL_SELECTION_COLUMN = {  # Настройки колонки выбора модели
        "spacing": 10,  # Отступ между элементами
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,  # Горизонтальное выравнивание по центру
        "width": 400,  # Ширина колонки
    }

    BALANCE_TEXT = {  # Настройки текста баланса
        "size": 16,  # Размер шрифта
        "color": ft.Colors.GREEN_400,  # Зеленый цвет текста
        "weight": ft.FontWeight.BOLD,  # Жирный шрифт
    }

    BALANCE_CONTAINER = {  # Настройки контейнера баланса
        "padding": 10,  # Внутренние отступы
        "bgcolor": ft.Colors.GREY_900,  # Цвет фона
        "border_radius": 8,  # Скругление углов
        "border": ft.border.all(1, ft.Colors.GREY_700),  # Граница контейнера
    }

    @staticmethod
    def set_window_size(page: ft.Page):  # Метод установки размера окна
        page.window.width = 600  # Ширина окна
        page.window.height = 800  # Высота окна
        page.window.resizable = False  # Запрет изменения размера окна
        