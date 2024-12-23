import flet as ft
from ui.styles import AppStyles

class MessageBubble(ft.Container):
    def __init__(self, message: str, is_user: bool):
        super().__init__()
        self.padding = 10
        self.border_radius = 10
        self.bgcolor = ft.Colors.BLUE_700 if is_user else ft.Colors.GREY_700
        self.alignment = ft.alignment.center_right if is_user else ft.alignment.center_left
        self.margin = ft.margin.only(
            left=50 if is_user else 0,
            right=0 if is_user else 50,
            top=5,
            bottom=5
        )
        
        self.content = ft.Column(
            controls=[
                ft.Text(
                    value=message,
                    color=ft.Colors.WHITE,
                    size=16,
                    selectable=True,
                    weight=ft.FontWeight.W_400
                )
            ],
            tight=True
        )


class ModelSelector(ft.Dropdown):
    def __init__(self, models: list):
        super().__init__()
        
        # Применяем стили
        for key, value in AppStyles.MODEL_DROPDOWN.items():
            setattr(self, key, value)
            
        self.label = None  # Убираем лейбл
        self.hint_text = "Выбор модели"
        self.options = [
            ft.dropdown.Option(
                key=model['id'],
                text=model['name']
            ) for model in models
        ]
        self.all_options = self.options.copy()
        self.value = models[0]['id'] if models else None
        
        # Создаем поле поиска
        self.search_field = ft.TextField(
            on_change=self.filter_options,
            hint_text="Поиск модели",
            **AppStyles.MODEL_SEARCH_FIELD
        )

    def filter_options(self, e):
        search_text = self.search_field.value.lower() if self.search_field.value else ""
        if not search_text:
            self.options = self.all_options
        else:
            self.options = [
                opt for opt in self.all_options
                if search_text in opt.text.lower() or search_text in opt.key.lower()
            ]
        e.page.update()

