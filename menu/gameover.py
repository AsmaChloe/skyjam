from menu.menu import MenuSubOptions
import random
import pygame


class GameOver(MenuSubOptions):
    def __init__(self, game, state = "GameOver", previous_state=(None, None)):
        
        MenuSubOptions.__init__(self, game, state, self.randomCatchPhrase(), ["Rejouer", "Menu principal"], previous_state=previous_state)
        
    def validate(self, text):
        '''
        Validate the current option selected in the menu
        :return:
        '''
        self.validate_button_sound.play()
        if text == "Rejouer":
            self.game.reset_game()
            self.game.playing = True
        elif text == "Menu principal":
            self.game.reset_game()
            self.game.playing = False
        self.game.current_menu = self.game.main_menu
        self.game.current_menu.state = "Main"
        self.randomizePhrase()
    
    def randomCatchPhrase(self):
        return random.choice(["J'en ai vu des gens tomber… Toi, tu le fais très mal.", "Alors ? t'en a pas marre de te manger des trucs ?", "J'ai vu un truc tomber, c'était ton skill.", "T'en est content de tes doigts ?", "Ça fait mal ?", "Ça fait longtemps que t'es dans le camp des perdants ?", "La loose a un nom: le tien.","On dirait que la chance n'était pas de ton côté aujourd'hui.",
    "Tu es vraiment doué pour trouver de nouvelles façons de perdre.",
    "Encore un coup de maître... de la défaite.",
    "On pourrait presque croire que tu le fais exprès.",
    "Dommage, la victoire était presque à ta portée… ou pas.",
    "Encore un échec, tu deviens vraiment expert.",
    "La défaite et toi, une histoire d'amour éternelle.",
    "Peut-être que ce jeu n'est tout simplement pas fait pour toi.",
    "Tu pourrais être l’ambassadeur de la défaite.",
    "On dirait que gagner n'est pas vraiment ton fort.",
    "Même le hasard n'a pas voulu de toi aujourd'hui.",
    "La victoire t'a encore échappé, comme d'habitude.",
    "Tu es le champion incontesté… de la défaite.",
    "Encore une partie où tu as su te distinguer… en perdant.",
    "Tu devrais breveter ta méthode de défaite.",
    "Une autre partie, une autre défaite, bravo !",
    "Encore une fois, tu as prouvé que tu pouvais perdre avec panache.",
    "Ton talent pour perdre est vraiment impressionnant.",
    "À ce rythme, tu pourrais devenir perdant professionnel.",
    "Tu as encore réussi à faire ce que tu fais de mieux : perdre.",
    "Encore une fois, tu as su décevoir tous tes espoirs.",
    "Gagner, ce n'est vraiment pas ton truc.",
    "Une autre défaite bien méritée.",
    "Tu es vraiment constant dans tes défaites, bravo !",
    "Si perdre était un art, tu serais un grand maître.",
    "Tu as perdu ? Encore ? Quelle surprise.",
    "La défaite te va comme un gant.",
    "On pourrait presque dire que tu es né pour perdre.",
    "Tu devrais penser à changer de hobby.",
    "Encore une défaite à ajouter à ton palmarès.",
    "Echouer semble être ta vocation.",
    "Encore une performance remarquable… dans la défaite.",
    "Tu as perdu ? Je commence à m'y habituer.",
    "Tu es vraiment régulier… dans la défaite.",
    "Une autre partie, une autre défaite, quelle constance.",
    "Ton talent pour perdre est inégalé.",
    "Tu fais vraiment honneur à la défaite.",
    "Encore une fois, tu as su nous impressionner par ta défaite.",
    "Perdre avec autant de grâce, c'est rare.",
    "Tu pourrais faire carrière dans la défaite.",
    "Encore une belle défaite à ton actif.",
    "On peut toujours compter sur toi pour perdre.",
    "La défaite est définitivement ta meilleure amie.",
    "Encore une fois, tu as prouvé que tu pouvais perdre avec brio.",
    "Perdre semble être ta spécialité.",
    "Encore une défaite bien méritée.",
    "On dirait que tu as un don pour la défaite.",
    "Ta capacité à perdre est vraiment remarquable.",
    "Encore une performance exceptionnelle… dans la défaite.",
    "Tu devrais recevoir un prix pour tes défaites.",
    "Perdre, c'est vraiment ton domaine de prédilection.",
    "Encore une défaite mémorable.",
    "On dirait que tu es fait pour perdre.",
    "Une autre partie, une autre défaite, quel talent.",
    "Tu es vraiment un expert… en défaite.",
    "Encore une fois, tu as su perdre avec panache.",
    "Ton talent pour perdre est vraiment unique.",
    "Encore une belle démonstration de comment perdre.",
    "La défaite te va si bien.",
    "On dirait que la victoire n'est pas ton truc.",
    "Tu pourrais donner des cours sur la défaite.",
    "Encore une performance remarquable… en perdant.",
    "La défaite est définitivement ta meilleure alliée.",
    "Tu es vraiment constant… dans la défaite.",
    "On peut toujours compter sur toi pour perdre.",
    "Ta capacité à perdre ne cesse de nous étonner.",
    "On dirait que tu es abonné aux défaites.",
    "L'important ce n'est pas la chute, c'est l'atterrissage",
    "Je n'ai j'amais parié sur toi, et j'ai bien fait.",
    "La chute était belle. L'atterrissage... pas tellement.",
    "Les oiseaux volent, toi, tu t'écrases.",
    "Tomber, c'est humain. Atterrir, c'est... un autre problème."
])
    
    def randomizePhrase(self):
        self.main_text = self.randomCatchPhrase()
        self.create_sprites()
        self.position_sprites()