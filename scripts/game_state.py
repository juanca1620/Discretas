class GameState:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(cls)
            cls._instance.reset()
        return cls._instance

    def reset(self):
        self.is_sick = False
        self.trusts_mateo = False
        self.faces_fear = False
        self.accepts_new_home = False
        self.grandfather_interaction = None
        
    def calculate_ending(self):
        """Returns a string identifier for the calculated ending."""
        score = 0
        if self.trusts_mateo: score += 1
        if self.faces_fear: score += 1
        if self.accepts_new_home: score += 1
        
        if score == 0:
            return "El Lobo Solitario"
        elif score == 3 and not self.is_sick:
            return "El Mejor Chico"
        elif score == 3 and self.is_sick:
            return "Corazón Sanando"
        elif self.accepts_new_home and not self.faces_fear:
            return "Tímido pero a Salvo"
        elif self.accepts_new_home and not self.trusts_mateo:
            return "Guardián Independiente"
        else:
            return "Adaptación Neutral"
