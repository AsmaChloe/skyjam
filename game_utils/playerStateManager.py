class PlayerStateManager():
    def __init__(self):
        self.isThrowing = False
        self.isWithBat = False
        self.isInvincible = False
        self.isProtected = False
        self.isDynamite = False
        self.isDynamiteStarting = False
        self.isDynamiteEnding = False
        self.isDynamiteDuring = False
        self.isEvolvingPickaxe = False

    def touchBat(self, isBatTouched):
        self.isWithBat = isBatTouched

    def protect(self, newState):
        self.isProtected = newState
