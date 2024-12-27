import flet as ft                                  # Фреймворк для создания UI
from api.openrouter import OpenRouterClient        # Клиент для работы с AI API
from ui.styles import AppStyles                    # Стили приложения
from ui.components import MessageBubble, ModelSelector  # UI компоненты
from utils.cache import ChatCache                  # Система кэширования
from utils.logger import AppLogger                 # Система логирования
from utils.analytics import Analytics              # Система аналитики
from utils.monitor import PerformanceMonitor       # Мониторинг производительности
import asyncio                                     # Для асинхронных операций
import time                                        # Для работы со временем
import json                                        # Для работы с JSON
from datetime import datetime                      # Для работы с датой/временем
import os                                          # Для работы с файловой системой

class ChatApp:
    def __init__(self):
        # Инициализация основных компонентов
        self.api_client = OpenRouterClient()       # Создание клиента API
        self.cache = ChatCache()                   # Инициализация кэша
        self.logger = AppLogger()                  # Инициализация логгера
        self.analytics = Analytics()               # Инициализация аналитики
        self.monitor = PerformanceMonitor()        # Инициализация мониторинга

        # Создание текста для отображения баланса
        self.balance_text = ft.Text(
            "Баланс: Загрузка...",
            **AppStyles.BALANCE_TEXT
        )
        self.update_balance()                      # Обновление баланса

        # Создание директории для экспорта
        self.exports_dir = "exports"
        os.makedirs(self.exports_dir, exist_ok=True)  # Создание папки если её нет
        
    def load_chat_history(self):
        """Загрузка истории чата из кэша"""
        try:
            history = self.cache.get_chat_history()    # Получение истории из кэша
            for msg in reversed(history):              # Перебор сообщений в обратном порядке
                # Распаковка данных сообщения
                _, model, user_message, ai_response, timestamp, tokens = msg
                # Добавление сообщений в интерфейс
                self.chat_history.controls.extend([
                    MessageBubble(                     # Создание пузырька сообщения пользователя
                        message=user_message,
                        is_user=True
                    ),
                    MessageBubble(                     # Создание пузырька ответа AI
                        message=ai_response,
                        is_user=False
                    )
                ])
        except Exception as e:
            # Логирование ошибки при загрузке
            self.logger.error(f"Ошибка загрузки истории чата: {e}")

    def update_balance(self):
        """Обновление отображения баланса"""
        try:
            balance = self.api_client.get_balance()    # Получение баланса через API
            self.balance_text.value = f"Баланс: {balance}"  # Обновление текста баланса
            self.balance_text.color = ft.Colors.GREEN_400   # Установка зеленого цвета
        except Exception as e:
            # Обработка ошибки получения баланса
            self.balance_text.value = "Баланс: н/д"
            self.balance_text.color = ft.Colors.RED_400     # Установка красного цвета
            self.logger.error(f"Ошибка обновления баланса: {e}")
            
            
    def main(self, page: ft.Page):
        # Применение настроек страницы из стилей
        for key, value in AppStyles.PAGE_SETTINGS.items():
            setattr(page, key, value)

        AppStyles.set_window_size(page)    # Установка размера окна

        # Инициализация компонентов выбора модели
        models = self.api_client.available_models
        self.model_dropdown = ModelSelector(models)
        self.model_dropdown.value = models[0] if models else None

        # Создание компонентов интерфейса
        self.message_input = ft.TextField(**AppStyles.MESSAGE_INPUT)    # Поле ввода
        self.chat_history = ft.ListView(**AppStyles.CHAT_HISTORY)       # История чата

        # Загрузка существующей истории
        self.load_chat_history()
        
        
        async def send_message_click(e):
            """Асинхронная функция отправки сообщения"""
            if not self.message_input.value:   # Проверка наличия текста
                return

            try:
                # Визуальная индикация процесса
                self.message_input.border_color = ft.Colors.BLUE_400
                page.update()

                # Сохранение данных сообщения
                start_time = time.time()
                user_message = self.message_input.value
                self.message_input.value = ""   # Очистка поля ввода
                page.update()

                # Добавление сообщения пользователя
                self.chat_history.controls.append(
                    MessageBubble(message=user_message, is_user=True)
                )

                # Индикатор загрузки
                loading = ft.ProgressRing()
                self.chat_history.controls.append(loading)
                page.update()

                # Асинхронная отправка запроса
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: self.api_client.send_message(
                        user_message, 
                        self.model_dropdown.value
                    )
                )

                # Удаление индикатора загрузки
                self.chat_history.controls.remove(loading)

                # Обработка ответа
                if "error" in response:
                    response_text = f"Ошибка: {response['error']}"
                    tokens_used = 0
                    self.logger.error(f"Ошибка API: {response['error']}")
                else:
                    response_text = response["choices"][0]["message"]["content"]
                    tokens_used = response.get("usage", {}).get("total_tokens", 0)

                # Сохранение в кэш
                self.cache.save_message(
                    model=self.model_dropdown.value,
                    user_message=user_message,
                    ai_response=response_text,
                    tokens_used=tokens_used
                )

                # Добавление ответа в чат
                self.chat_history.controls.append(
                    MessageBubble(message=response_text, is_user=False)
                )

                # Обновление аналитики
                response_time = time.time() - start_time
                self.analytics.track_message(
                    model=self.model_dropdown.value,
                    message_length=len(user_message),
                    response_time=response_time,
                    tokens_used=tokens_used
                )

                # Логирование метрик
                self.monitor.log_metrics(self.logger)
                page.update()

            except Exception as e:
                # Обработка ошибок
                self.logger.error(f"Ошибка отправки сообщения: {e}")
                self.message_input.border_color = ft.Colors.RED_500

                # Показ уведомления об ошибке
                snack = ft.SnackBar(
                    content=ft.Text(
                        str(e),
                        color=ft.Colors.RED_500,
                        weight=ft.FontWeight.BOLD
                    ),
                    bgcolor=ft.Colors.GREY_900,
                    duration=5000,
                )
                page.overlay.append(snack)
                snack.open = True
                page.update()
                
        def show_error_snack(page, message: str):
            """Показ уведомления об ошибке"""
            snack = ft.SnackBar(                  # Создание уведомления
                content=ft.Text(
                    message,
                    color=ft.Colors.RED_500
                ),
                bgcolor=ft.Colors.GREY_900,
                duration=5000,
            )
            page.overlay.append(snack)            # Добавление уведомления
            snack.open = True                     # Открытие уведомления
            page.update()                         # Обновление страницы

        async def show_analytics(e):
            """Показ статистики использования"""
            stats = self.analytics.get_statistics()    # Получение статистики

            # Создание диалога статистики
            dialog = ft.AlertDialog(
                title=ft.Text("Аналитика"),
                content=ft.Column([
                    ft.Text(f"Всего сообщений: {stats['total_messages']}"),
                    ft.Text(f"Всего токенов: {stats['total_tokens']}"),
                    ft.Text(f"Среднее токенов/сообщение: {stats['tokens_per_message']:.2f}"),
                    ft.Text(f"Сообщений в минуту: {stats['messages_per_minute']:.2f}")
                ]),
                actions=[
                    ft.TextButton("Закрыть", on_click=lambda e: close_dialog(dialog)),
                ],
            )

            page.overlay.append(dialog)           # Добавление диалога
            dialog.open = True                    # Открытие диалога
            page.update()                         # Обновление страницы

        async def clear_history(e):
            """Очистка истории чата"""
            # Очистка данных
            self.chat_history.controls.clear()    # Очистка визуального списка
            self.cache.clear_history()            # Очистка кэша
            self.analytics.clear_data()           # Очистка аналитики
            
            # Обновляем страницу сразу после очистки
            page.update()

            # Показ уведомления об успешной очистке
            snack = ft.SnackBar(
                content=ft.Text(
                   "История чата успешно очищена",
                    color=ft.Colors.WHITE
                ),
                bgcolor=ft.Colors.GREEN_700,
                duration=3000,
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()

        async def confirm_clear_history(e):
            """Подтверждение очистки истории"""
            def close_dlg(e):                     # Функция закрытия диалога
                close_dialog(dialog)

            async def clear_confirmed(e):         # Функция подтверждения очистки
                close_dialog(dialog)
                await clear_history(e)

            # Создание диалога подтверждения
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Подтверждение удаления"),
                content=ft.Text("Вы уверены? Это действие нельзя отменить!"),
                actions=[
                    ft.TextButton("Отмена", on_click=close_dlg),
                    ft.TextButton("Очистить", on_click=clear_confirmed),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        def close_dialog(dialog):
            """Закрытие диалогового окна"""
            dialog.open = False                   # Закрытие диалога
            page.update()                         # Обновление страницы
            if dialog in page.overlay:            # Удаление из overlay
                page.overlay.remove(dialog)
                
        async def save_dialog(e):
            """Сохранение диалога в файл"""
            try:
                # Получение истории из кэша
                history = self.cache.get_chat_history()

                # Форматирование данных для сохранения
                dialog_data = []
                for msg in history:
                    dialog_data.append({
                        "timestamp": msg[4],
                        "model": msg[1],
                        "user_message": msg[2],
                        "ai_response": msg[3],
                        "tokens_used": msg[5]
                    })

                # Создание имени файла
                filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                filepath = os.path.join(self.exports_dir, filename)

                # Сохранение в JSON
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(dialog_data, f, ensure_ascii=False, indent=2, default=str)

                # Создание диалога успешного сохранения
                dialog = ft.AlertDialog(
                    title=ft.Text("Диалог сохранен"),
                    content=ft.Column([
                        ft.Text("Путь сохранения:"),
                        ft.Text(filepath, selectable=True, weight=ft.FontWeight.BOLD),
                    ]),
                    actions=[
                        ft.TextButton("OK", on_click=lambda e: close_dialog(dialog)),
                        ft.TextButton("Открыть папку", 
                            on_click=lambda e: os.startfile(self.exports_dir)
                        ),
                    ],
                )

                page.overlay.append(dialog)
                dialog.open = True
                page.update()

            except Exception as e:
                self.logger.error(f"Ошибка сохранения: {e}")
                show_error_snack(page, f"Ошибка сохранения: {str(e)}")
                
        # Создание основных кнопок управления
        save_button = ft.ElevatedButton(
            on_click=save_dialog,                 # Привязка функции сохранения
            **AppStyles.SAVE_BUTTON              # Применение стилей
        )

        clear_button = ft.ElevatedButton(
            on_click=confirm_clear_history,       # Привязка функции очистки
            **AppStyles.CLEAR_BUTTON             # Применение стилей
        )

        send_button = ft.ElevatedButton(
            on_click=send_message_click,          # Привязка функции отправки
            **AppStyles.SEND_BUTTON              # Применение стилей
        )

        analytics_button = ft.ElevatedButton(
            on_click=show_analytics,              # Привязка функции аналитики
            **AppStyles.ANALYTICS_BUTTON         # Применение стилей
        )

        # Создание ряда кнопок управления
        control_buttons = ft.Row(
            controls=[                            # Размещение кнопок в ряд
                save_button,
                analytics_button,
                clear_button
            ],
            **AppStyles.CONTROL_BUTTONS_ROW      # Применение стилей к ряду
        )

        # Создание строки ввода с кнопкой отправки
        input_row = ft.Row(
            controls=[                            # Размещение элементов ввода
                self.message_input,
                send_button
            ],
            **AppStyles.INPUT_ROW               # Применение стилей к строке ввода
        )

        # Создание колонки для элементов управления
        controls_column = ft.Column(
            controls=[                            # Размещение элементов управления
                input_row,
                control_buttons
            ],
            **AppStyles.CONTROLS_COLUMN         # Применение стилей к колонке
        )

        # Создание контейнера для баланса
        balance_container = ft.Container(
            content=self.balance_text,            # Размещение текста баланса
            **AppStyles.BALANCE_CONTAINER        # Применение стилей к контейнеру
        )

        # Создание колонки выбора модели
        model_selection = ft.Column(
            controls=[                            # Размещение элементов выбора модели
                self.model_dropdown.search_field,
                self.model_dropdown,
                balance_container
            ],
            **AppStyles.MODEL_SELECTION_COLUMN   # Применение стилей к колонке
        )

        # Создание основной колонки приложения
        main_column = ft.Column(
            controls=[                            # Размещение основных элементов
                model_selection,
                self.chat_history,
                controls_column
            ],
            **AppStyles.MAIN_COLUMN             # Применение стилей к главной колонке
        )

        # Добавление основной колонки на страницу
        page.add(main_column)
        
        
        # Настройка обработки нажатия Enter
        def on_message_key(e):
            """Обработчик нажатия клавиш в поле ввода"""
            if e.key == "Enter" and e.shift:      # Проверка комбинации Shift+Enter
                asyncio.create_task(send_message_click(e))  # Асинхронная отправка

        # Привязка обработчика к полю ввода
        self.message_input.on_key_event = on_message_key

        # Получение метрик
        self.monitor.get_metrics()

        # Логирование запуска
        self.logger.info("Приложение запущено")

def main():
    """Точка входа в приложение"""
    app = ChatApp()                              # Создание экземпляра приложения
    ft.app(target=app.main)                      # Запуск приложения

if __name__ == "__main__":
    main()                                       # Запуск если файл запущен напрямую
