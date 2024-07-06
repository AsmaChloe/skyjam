import pygame

class PickaxeManager:
    def manage_ore_hit(self, pickaxe, collided_ore, player, sound_player):
        if not pickaxe.noHit:
            if collided_ore:
                # Add XP
                self.player.XP += collided_ore.ore_type.XP

                # Remove ore
                self.sound_player.ore_channel.play(collided_ore.broken_sound)
                collided_ore.broken = True

                if self.pickaxe_type != PickaxeType.DIAMOND_PICKAXE and self.player.XP >= self.pickaxe_type.next_pickaxe_cost:
                    self.player.isEvolvingPickaxe = True
                    self.player.XP -= self.pickaxe_type.next_pickaxe_cost
                    self.pickaxe_type, self.max_XP = self.pickaxe.evolve()
                    self.evolution_time_begin = pygame.time.get_ticks()

