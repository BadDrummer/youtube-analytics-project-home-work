

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.ID = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        pass
