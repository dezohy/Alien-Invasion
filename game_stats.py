class GameStats:
    """Відслідковування статистики для Alien Invasion."""

    def __init__(self, ai_settings):
        """Ініціалізувати статистику."""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Почати гру в неактивному стані.
        self.game_active = False

        # Рекордний рахунок ніколи не повинен скидатися.
        self.high_score = 0

    def reset_stats(self):
        """Ініціалізувати статистику, яка може змінюватися під час гри."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
