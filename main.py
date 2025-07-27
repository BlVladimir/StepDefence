import asyncio
import threading

from scripts.main_classes.main_class import StepDefence
from nicegui import ui


class Panda3DWidget:
    def __init__(self):
        self.engine = None
        self.update_task = None
        self.image_element = None

    async def start_engine(self):
        """Запуск движка в отдельном потоке"""

        def run_engine():
            self.engine = StepDefence()

        # Запускаем в отдельном потоке
        thread = threading.Thread(target=run_engine, daemon=True)
        thread.start()

        # Ждем инициализации
        while self.engine is None:
            await asyncio.sleep(0.1)

        # Запускаем цикл обновления
        self.start_update_loop()

    def start_update_loop(self):
        """Запуск цикла обновления"""

        async def update_loop():
            while self.engine and self.engine.running:
                try:
                    # Обновляем движок
                    self.engine.update()

                    # Получаем кадр
                    frame_data = self.engine.get_frame_data()
                    if frame_data and self.image_element:
                        # Обновляем изображение
                        self.image_element.set_source(f'data:image/png;base64,{frame_data}')

                    await asyncio.sleep(1 / 30)  # 30 FPS
                except Exception as e:
                    print(f"Ошибка в цикле обновления: {e}")
                    break

        if self.update_task:
            self.update_task.cancel()
        self.update_task = asyncio.create_task(update_loop())

    def handle_click(self, event):
        """Обработка клика по изображению"""
        if self.engine:
            x = event.args.get('offsetX', 0)
            y = event.args.get('offsetY', 0)
            self.engine.handle_mouse_click(x, y, 800, 600)

    def create_ui(self):
        """Создание пользовательского интерфейса"""
        with ui.column().classes('w-full h-full items-center'):
            ui.label('Panda3D в NiceGUI').classes('text-2xl font-bold mb-4')

            with ui.card().classes('p-4'):
                ui.label('3D Сцена:').classes('text-lg mb-2')

                # Контейнер для 3D сцены
                self.image_element = ui.interactive_image(
                    source='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
                ).classes('border-2 border-gray-300 cursor-pointer')

                # Привязываем обработчик клика
                self.image_element.on('click', self.handle_click)

            with ui.row().classes('mt-4 gap-4'):
                ui.button('Запустить 3D', on_click=self.start_engine).classes('bg-green-500')
                ui.button('Остановить', on_click=self.stop_engine).classes('bg-red-500')

            ui.label('Инструкции:').classes('text-lg mt-4 mb-2')
            with ui.column().classes('text-sm'):
                ui.label('• Нажмите "Запустить 3D" для инициализации движка')
                ui.label('• Кликайте по разноцветным кубам для их анимации')
                ui.label('• Движок работает в реальном времени с частотой 30 FPS')

    def stop_engine(self):
        """Остановка движка"""
        if self.engine:
            self.engine.cleanup()
            self.engine = None

        if self.update_task:
            self.update_task.cancel()
            self.update_task = None


# Основная функция
def main():
    # Создаем виджет
    widget = Panda3DWidget()

    # Создаем интерфейс
    widget.create_ui()

    # Запускаем NiceGUI
    ui.run(
        native=True,
        title='StepDeffence',
        port=8080,
        show=True,
        reload=False
    )


if __name__ == '__main__':
    main()