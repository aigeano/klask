from rest_framework.views import APIView
from .models import Player, Tournament
from rest_framework.response import Response


class CreateTournament(APIView):

    def post(self, request):
        player_names  = request.data.get('players').split(',')
        players = []
        for player_name in player_names:
            players.append(Player.object.create(name=player_name))
        tournament = Tournament.objects.create()
        tournament.players.add(*players)
        bracket = self.create_balanced_round_robin()
        tournament.bracket = bracket
        tournament.save()
        return Response(tournament)


class GetTournamentBracket(APIView):
    def get(self, request, tournament_id):
        tournament = Tournament.objects.get(tournament_id)
        return Response(tournament.bracket)





    def create_balanced_round_robin(self, players):
        """ Create a schedule for the players in the list and return it"""
        s = []
        if len(players) % 2 == 1: players = players + [None]
        # manipulate map (array of indexes for list) instead of list itself
        # this takes advantage of even/odd indexes to determine home vs. away
        n = len(players)
        map = list(range(n))
        mid = n // 2
        for i in range(n - 1):
            l1 = map[:mid]
            l2 = map[mid:]
            l2.reverse()
            round = []
            for j in range(mid):
                t1 = players[l1[j]]
                t2 = players[l2[j]]
                if j == 0 and i % 2 == 1:
                    # flip the first match only, every other round
                    # (this is because the first match always involves the last player in the list)
                    round.append((t2, t1))
                else:
                    round.append((t1, t2))
            s.append(round)
            # rotate list by n/2, leaving last element at the end
            map = map[mid:-1] + map[:mid] + map[-1:]
        return s




