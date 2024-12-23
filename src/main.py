import flet as ft
from api.openrouter import OpenRouterClient
from ui.styles import AppStyles
from ui.components import MessageBubble, ModelSelector
from utils.cache import ChatCache
from utils.logger import AppLogger
from utils.analytics import Analytics
from utils.monitor import PerformanceMonitor
import asyncio
import time
import json
from datetime import datetime
import os

class ChatApp:
    def __init__(self):
        """Асинхронная инициализация компонентов"""
        self.api_client = OpenRouterClient()
        self.cache = ChatCache()
        self.logger = AppLogger(log_file='app.log')
        self.analytics = Analytics()
        self.monitor = PerformanceMonitor()
        
        self.balance_text = ft.Text(
            "Баланс: Загрузка...",
            **AppStyles.BALANCE_TEXT
        )
        self.update_balance()
        self.exports_dir = "exports"  # Директория для сохранения диалогов
        os.makedirs(self.exports_dir, exist_ok=True)

    def load_chat_history(self):
        """Загрузка истории чата из кэша"""
        try:
            history = self.cache.get_chat_history()
            for msg in reversed(history):  # Реверсируем чтобы показать старые сообщения первыми
                _, model, user_message, ai_response, timestamp, tokens = msg
                self.chat_history.controls.extend([
                    MessageBubble(
                        message=user_message,
                        is_user=True
                    ),
                    MessageBubble(
                        message=ai_response,
                        is_user=False
                    )
                ])
        except Exception as e:
            self.logger.error(f"Ошибка загрузки истории чата: {e}")
    
    def update_balance(self):
        """Обновить текст баланса"""
        try:
            balance = self.api_client.get_balance()
            self.balance_text.value = f"Баланс: {balance}"
            self.balance_text.color = ft.Colors.GREEN_400
        except Exception as e:
            self.balance_text.value = "Баланс: н/д"
            self.balance_text.color = ft.Colors.RED_400
            self.logger.error(f"Ошибка обновления баланса: {e}")
            
    def main(self, page: ft.Page):
        
        # Применяем настройки страницы
        for key, value in AppStyles.PAGE_SETTINGS.items():
            setattr(page, key, value)
            
        # Устанавливаем размер окна
        AppStyles.set_window_size(page)    
        
        # Проверяем доступные модели
        models = self.api_client.available_models
        
        self.model_dropdown = ModelSelector(models)
        self.model_dropdown.value = models[0] if models else None  # Устанавливаем значение по умолчанию
        
        self.message_input = ft.TextField(**AppStyles.MESSAGE_INPUT)
        self.chat_history = ft.ListView(**AppStyles.CHAT_HISTORY)

        # Загружаем историю чата при запуске
        self.load_chat_history()

        async def send_message_click(e):
            if not self.message_input.value:
                return

            try:
                self.message_input.border_color = ft.Colors.BLUE_400
                page.update()

                start_time = time.time()
                user_message = self.message_input.value
                self.message_input.value = ""
                page.update()

                self.chat_history.controls.append(
                    MessageBubble(message=user_message, is_user=True)
                )
                
                loading = ft.ProgressRing()
                self.chat_history.controls.append(loading)
                page.update()

                # Создаем футуру для асинхронного запроса
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: self.api_client.send_message(user_message, self.model_dropdown.value)
                )

                self.chat_history.controls.remove(loading)

                if "error" in response:
                    response_text = f"Ошибка: {response['error']}"
                    tokens_used = 0
                    self.logger.error(f"Ошибка API: {response['error']}")
                else:
                    response_text = response["choices"][0]["message"]["content"]
                    tokens_used = response.get("usage", {}).get("total_tokens", 0)

                self.cache.save_message(
                    model=self.model_dropdown.value,
                    user_message=user_message,
                    ai_response=response_text,
                    tokens_used=tokens_used
                )

                self.chat_history.controls.append(
                    MessageBubble(message=response_text, is_user=False)
                )

                response_time = time.time() - start_time
                self.analytics.track_message(
                    model=self.model_dropdown.value,
                    message_length=len(user_message),
                    response_time=response_time,
                    tokens_used=tokens_used
                )

                self.monitor.log_metrics(self.logger)
                page.update()

            except Exception as e:
                self.logger.error(f"Ошибка отправки сообщения в send_message: {e}")
                self.message_input.border_color = ft.Colors.RED_500
                
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
            """Вспомогательная функция для показа ошибок"""
            snack = ft.SnackBar(
                content=ft.Text(
                    message,
                    color=ft.Colors.RED_500
                ),
                bgcolor=ft.Colors.GREY_900,
                duration=5000,
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()
            
        async def show_analytics(e):
            """Показать статистику использования"""
            stats = self.analytics.get_statistics()
            
            # Создаем диалог
            dialog = ft.AlertDialog(
                title=ft.Text("Аналитика"),
                content=ft.Column([
                    ft.Text(f"Всего сообщений: {stats['total_messages']}"),
                    ft.Text(f"Всего токенов: {stats['total_tokens']}"),
                    ft.Text(f"Среднее число токенов на сообщение: {stats['tokens_per_message']:.2f}"),
                    ft.Text(f"Сообщений в минуту: {stats['messages_per_minute']:.2f}")
                ]),
                actions=[
                    ft.TextButton("Закрыть", on_click=lambda e: close_dialog(dialog)),
                ],
            )
            
            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        async def clear_history(e):
            # Очищаем визуальный список
            self.chat_history.controls.clear()
            
            # Очищаем кэш в базе данных
            self.cache.clear_history()
            
            # Очищаем аналитику
            self.analytics.clear_data()
            
            # Показываем уведомление об успешной очистке
            snack = ft.SnackBar(
                content=ft.Text(
                   "Chat history and analytics cleared successfully",
                    color=ft.Colors.WHITE
                ),
                bgcolor=ft.Colors.GREEN_700,
                duration=3000,
            )
            page.overlay.append(snack)
            snack.open = True
            
            # Обновляем UI
            page.update()

        # Можно также добавить диалог подтверждения перед очисткой:
        async def confirm_clear_history(e):
            def close_dlg(e):
                close_dialog(dialog)

            async def clear_confirmed(e):
                close_dialog(dialog)
                await clear_history(e)

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Подтверждение удаления истории"),
                content=ft.Text("Вы действительно хотите очистить всю историю чата? Это действие безвозвратное!"),
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
            """Закрыть диалог и удалить его из overlay"""
            dialog.open = False
            page.update()
            if dialog in page.overlay:
                page.overlay.remove(dialog)
                
        async def save_dialog(e):
            try:
                # Получаем историю диалога из кэша
                history = self.cache.get_chat_history()
                
                # Форматируем данные для сохранения
                dialog_data = []
                for msg in history:
                    dialog_data.append({
                        "timestamp": msg[4],  # Предполагаем, что timestamp это 5-й элемент
                        "model": msg[1],      # model это 2-й элемент
                        "user_message": msg[2],
                        "ai_response": msg[3],
                        "tokens_used": msg[5]
                    })

                # Создаем имя файла с текущей датой и временем
                filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                filepath = os.path.join(self.exports_dir, filename)

                # Сохраняем в JSON файл
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(dialog_data, f, ensure_ascii=False, indent=2, default=str)

                # Создаем и показываем диалог через overlay
                dialog = ft.AlertDialog(
                    title=ft.Text("Диалог успешно сохранен"),
                    content=ft.Column([
                        ft.Text("Диалог сохранен в:"),
                        ft.Text(
                            filepath,
                            selectable=True,
                            weight=ft.FontWeight.BOLD
                        ),
                    ]),
                    actions=[
                        ft.TextButton("OK", on_click=lambda e: close_dialog(dialog)),
                        ft.TextButton(
                            "Открыть папку",
                            on_click=lambda e: os.startfile(self.exports_dir)
                        ),
                    ],
                )

                # Добавляем диалог в overlay и показываем его
                page.overlay.append(dialog)
                dialog.open = True
                page.update()

            except Exception as e:
                self.logger.error(f"Ошибка созранения диалога: {e}")
                show_error_snack(page, f"Ошибка созранения диалога: {str(e)}")

                
        
        # Создаем кнопку сохранения
        save_button = ft.ElevatedButton(
            on_click=save_dialog,
            **AppStyles.SAVE_BUTTON
        )
                
        # Создаем кнопку очистки
        clear_button = ft.ElevatedButton(
            on_click=confirm_clear_history,  # Меняем на confirm_clear_history
            **AppStyles.CLEAR_BUTTON
        )

        # Создаем кнопки
        send_button = ft.ElevatedButton(
            on_click=send_message_click,
            **AppStyles.SEND_BUTTON
        )



        analytics_button = ft.ElevatedButton(
            on_click=show_analytics,
            **AppStyles.ANALYTICS_BUTTON
        )


        # Создаем кнопки управления (нижний ряд)
        control_buttons = ft.Row(
            controls=[
                save_button,
                analytics_button,
                clear_button
            ],
            **AppStyles.CONTROL_BUTTONS_ROW
        )

        # Создаем строку ввода с кнопкой отправки
        input_row = ft.Row(
            controls=[
                self.message_input,
                send_button
            ],
            **AppStyles.INPUT_ROW
        )
        
        # Создаем контейнер для баланса
        balance_container = ft.Container(
            content=self.balance_text,
            **AppStyles.BALANCE_CONTAINER,
        )
        
        # Создаем верхнюю панель с балансом и выбором модели
        top_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.model_dropdown.search_field,
                            self.model_dropdown
                        ],
                        **AppStyles.MODEL_SELECTION_COLUMN
                    ),
                    expand=True
                ),
                balance_container
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START
        )

        # Создаем колонку с элементами управления
        controls_column = ft.Column(
            controls=[
                input_row,
                control_buttons
            ],
            **AppStyles.CONTROLS_COLUMN
        )

        # Обновляем основной интерфейс
        page.add(
            ft.Column(
                controls=[
                    top_row,
                    self.chat_history,
                    controls_column  # Добавляем новую организацию кнопок
                ],
                **AppStyles.MAIN_COLUMN
            )
        )

        # Начинаем мониторинг производительности
        self.monitor.get_metrics()
        self.logger.info("Приложение успешно запущено!")


if __name__ == "__main__":
    app = ChatApp()
    ft.app(target=app.main)
