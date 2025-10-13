#Lets lock in bud

from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playergamelog
import pandas as pd



class Roster:
    def __init__(self):
        self.allP = players.get_active_players()
        self.allT = teams.get_teams()

        
    def analyze_roster(self,roster):
        seasons = ['2020-21', '2021-22', '2022-23', '2023-24', '2024-25']
        rstats = []

        for player in roster:
             matches = self.find_player(player)
             if len(matches) == 0:
                  print("There are no players by that name")
                  continue
             
             if len(matches) == 1:
                  player = matches[0]
                  print(matches[0]['full_name'] + " " + str(matches[0]['id']))
             else:
                  player = self.select_player(matches)
                  if not player:
                       print("Could not be found skipping player")
                       continue
             print("Getting stats~ \n")

             stats = self.get_stats(player['id'], seasons)

             for i in stats:
                  print(i)


    def get_stats(self, player_id, seasons):
         all_stats = []
         for season in seasons:
              try:
                   log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
                   data = log.get_data_frames()[0]
                   if len(data) > 0:
                        data['FANTASY_PTS'] = ((data['PTS'] * 1.0) + (data['AST'] * 1.5) + (data['REB'] * 1.2) + (data['STL'] * 3) + (data['BLK'] * 3) - (data['TOV'] * 1) + (data['FG3M'] * 0.5))
                        all_stats.append(data)
              except Exception as e:
                   print("Error getting " + season + " stats for player " + str(player_id) + ": " + str(e))
         return all_stats

    def find_player(self, name):
         matches = []
         name = name.lower().strip()

         for player in self.allP:
              full = player['full_name'].lower()
              first = player['first_name'].lower()
              last = player['last_name'].lower()

              if name == full:
                   matches.insert(0,player)
              elif name == first:
                   matches.append(player)
              elif name == last:
                   matches.append(player)
              elif name in full:
                   matches.append(player)
         return matches
    
    def calc_average(self, all_stats):
         if not all_stats:
              return None
         c_log = pd.concat(all_stats, ignore_index=True)
         averages = { 'games': len(c_log), 'pts': c_log['PTS'].mean(), 'ast': c_log['AST'].mean(), 'reb': c_log['REB'].mean(), 'stl': c_log['STL'].mean(), 'blk': c_log['BLK'].mean(), 'tov': c_log['TOV'].mean(), 'fg3m': c_log['FG3M'].mean(),'fantasy_pts': c_log['FANTASY_PTS'].mean()
        }
         return averages   


    def select_player(self,matches):
         print("Yo choose your player ")
         count = 1
         for player in matches:
              print(str(count) + ". " + player['full_name'] + " id(" + str(player['id']) + ")")
              count+=1
         
         while True:
              try:
                   num = input("Select player (1-" + str(len(matches)) + ") or 'skip' to skip: ").strip().lower()

                   if num == "skip":
                        return None
                   
                   num = int(num)
                   if 1 <= num <= len(matches):
                        selected = matches[num-1]
                        print("You have selected: " + selected['full_name'] + "(id: " + str(selected['id']) + ")")
                        return selected
              except ValueError:
                   print("Please enter a valid number or skip")
         return None
    

#====================================================================================================================================

def main():
        #get_player_id(player_name) -> get player names and convert into a list of player ids
        #get_todays_matchups(date)
        #get_player_gamelogs(player_id, season="ALL")
        #filter_games_vs_team(gamelogs, opponent_team)
        #calculate_average_stats(games)
        #calculate_fantasy_points(stats_row)
        #project_player_points(player_id, opponent_team)
        #build_lineup_projection(lineup, date)
        #optimize_lineup(lineup_projections)

        rost = Roster()
        print("\nEnter your roster (one player per line, press Enter on empty line to finish)(Case Sensitive):")
        roster = []
        while True:
            player_name = input("Player name: ").strip()
            if not player_name:
                break
            roster.append(player_name)
        
        if not roster:
            print("No players entered. Exiting.")
            return
        
        results = rost.analyze_roster(roster)

        
        
if __name__ == "__main__":
    main()




'''
PG Curry -> 35
SG klay thomson
PF
SF
C Giannis -> 50
C
G
F
Util1 POS doesnt matter
Util2 POS doesn't matter
UTIL3

=======
B 
B 
B



25
24 
23
22
21
'''
