from StatsGrabber import StatsGrabber

grabber = StatsGrabber('RGAPI-f6990f6b-5df7-4f2e-9826-e2050326af22')

ranked_games = grabber.get_ranked_games('CrystalJayde')
unranked_games = grabber.get_unranked_games('CrystalJayde')

print(ranked_games)
print(unranked_games)