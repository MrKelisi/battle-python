from model.battle import *

print(all_french_cards())

decks = create_decks(4)
for deck in decks:
	print("deck of", deck.number_of_cards(), "cards")
	print(deck)


print()
c1 = decks[0].draw()
c2 = decks[1].draw()
c3 = decks[2].draw()
c4 = decks[2].draw()

print(c1, "VS", c2, "VS", c3, "VS", c4)
print(c1.get_rank().value, "VS", c2.get_rank().value, "VS", c3.get_rank().value, "VS", c4.get_rank().value)
print("Winner(s):", compare_cards([c1, c2, c3, c4]))
