#Lets lock in bud

from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playergamelog
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import leagueseasonmatchups
import pandas as pd
import time



class Roster:
    def __init__(self):
        self.allP = players.get_active_players()
        self.allT = teams.get_teams()

        
    def analyze_roster(self,roster):
        seasons = ['2020-21', '2021-22', '2022-23', '2023-24', '2024-25']
        rstats = []
        count = 1
        projected_pts = 0

        for player in roster:
             matches = self.find_player(player)
             if len(matches) == 0:
                  print("There are no players by that name")
                  continue
             
             if len(matches) == 1:
                  player = matches[0]
                  print(str(count) + "." + matches[0]['full_name'] + " " + str(matches[0]['id']))
                  count+=1
             else:
                  player = self.select_player(matches)
                  if not player:
                       print("Could not be found skipping player")
                       continue
             print("Getting stats \n")

             stats = self.get_stats(player['id'], seasons)

             averages = self.calc_average(stats)

             #idk if theres a better way to do this so im just gonna print one by one lol
             print("Avg Games: " + str(int(averages["games"])))
             print("Avg Points: " + str(int(averages["pts"])))
             print("Avg Assists: " + str(int(averages["ast"])))
             print("Avg Rebounds: " + str(int(averages["reb"])))
             print("Avg Steals: " + str(int(averages["stl"])))
             print("Avg Blocks: " + str(int(averages["blk"])))
             print("Avg Turnovers: " + str(int(averages["tov"])))
             print("Avg Fantasy Points: " + str(int(averages["fantasy_pts"])) + "\n")
             projected_pts += int(averages['fantasy_pts'])
        print("\n\nYour total projected fantasy points per game is: " + str(projected_pts))

        return averages




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
         averages = { 'games': len(c_log)/5, 'pts': c_log['PTS'].mean(), 'ast': c_log['AST'].mean(), 'reb': c_log['REB'].mean(), 'stl': c_log['STL'].mean(), 'blk': c_log['BLK'].mean(), 'tov': c_log['TOV'].mean(), 'fg3m': c_log['FG3M'].mean(),'fantasy_pts': c_log['FANTASY_PTS'].mean()
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
   
 

    def getPlayerMatchup(self, roster):
          print("Enter the team abbreviation(LAL, BOS, ATL) the player is playing against(Press enter on an empty line to quit): ")
          opposing_teams = {}
          for player in roster:
               
                while True:
                     team = input(player['full_name'] + ": ").strip().upper()
                     if not team:
                          break
                     valid = False
                     for t in self.allT:
                         if t['abbreviation'] == team:
                             valid = True
                             break
                     if valid:
                          opposing_teams[player['full_name']] = team
                          break
                     else:
                          print("thats not a team bro")
          return opposing_teams


    def getMatchupData(self, player, opposition, seasons):
         all_stats = []
         for season in seasons:
           time.sleep(0.5)
           try:
               log = playergamelog.PlayerGameLog(player_id=player['id'], season=season)
               data = log.get_data_frames()[0]
               if len(data) > 0:
                   #try different ways to find the team
                   vs_opp = data[data['MATCHUP'].str.contains(opposition, na=False)]
                   if len(vs_opp) == 0:
                       vs_opp = data[data['MATCHUP'].str.contains("vs. " + opposition, na=False)]
                   if len(vs_opp) == 0:
                       vs_opp = data[data['MATCHUP'].str.contains("@" + opposition, na=False)]
                   
                   if len(vs_opp) > 0:
                       vs_opp = vs_opp.copy()
                       vs_opp['FANTASY_PTS'] = ((vs_opp['PTS'] * 1.0) + (vs_opp['AST'] * 1.5) + (vs_opp['REB'] * 1.2) + (vs_opp['STL'] * 3) + (vs_opp['BLK'] * 3) - (vs_opp['TOV'] * 1) + (vs_opp['FG3M'] * 0.5))
                       all_stats.append(vs_opp)
           except Exception as e:
               print("Error getting " + season + " data for " + player['full_name'] + ": " + str(e))
         
         if all_stats:
             combined = pd.concat(all_stats, ignore_index=True)
             return combined['FANTASY_PTS'].mean()
         else:
             #fallback to season average if no matchup data found 
             print("No matchup data for " + player['full_name'] + " vs " + opposition + ", using season average")
             return self.getSeasonAverage(player, seasons)

    def getSeasonAverage(self, player, seasons):
         #i need this js incase the user inputs a player and the player was majorly injured or was on that opposing team in the last 5 seasons
         all_stats = []
         for season in seasons:
           time.sleep(0.3)
           try:
               log = playergamelog.PlayerGameLog(player_id=player['id'], season=season)
               data = log.get_data_frames()[0]
               if len(data) > 0:
                   data = data.copy()
                   data['FANTASY_PTS'] = ((data['PTS'] * 1.0) + (data['AST'] * 1.5) + (data['REB'] * 1.2) + (data['STL'] * 3) + (data['BLK'] * 3) - (data['TOV'] * 1) + (data['FG3M'] * 0.5))
                   all_stats.append(data)
           except Exception as e:
               print("Error getting " + season + " season data for " + player['full_name'] + ": " + str(e))
         
         if all_stats:
             combined = pd.concat(all_stats, ignore_index=True)
             return combined['FANTASY_PTS'].mean()
         return 0.0

    def getPlayerPositions(self, roster):
         print("Please enter player positions here(Eg: SGA: PG,SG): ")
         player_pos = {}
         '''so in order to do this i have to go through the roster and ask the user to input the players positions
         so i guess kinda like: {player: "PGSGC"} -> that player is a PG, SG, and C'''
         for player in roster:
          
          positions = ["PG", "SG", "SF", "PF", "C"]
          
          user_input = input("Enter player positions for " + player['full_name'] + ": ").upper().replace(",", "").replace(" ", "")

          player_positions = []
          for pos in positions:
                    if pos in user_input:
                         player_positions.append(pos)

          player_pos[player['full_name']] = player_positions

         return player_pos
              
    def sortPlayers(self, roster, positions):
         sorted_roster = {}
         for player in roster:
              sorted_roster[player['full_name']] = player.get('FANTASY_PTS', 0)
     
         sorted_roster = dict(sorted(sorted_roster.items(), key=lambda item: item[1], reverse=True))
         return sorted_roster
    

    def buildOptimalLineup(self, players,matchup_data, positions):
         player_data = []
         for player in players:
              player_name = player['full_name']
              if player_name in matchup_data and player_name in positions:
                   player_data.append({'name': player_name, 'id': player['id'], 'fantasy_pts': matchup_data[player_name], 'positions' : positions[player_name]})
          
         player_data.sort(key=lambda x: x['fantasy_pts'], reverse=True)
         lineup = {
             'PG': None, 'SG': None, 'SF': None, 'PF': None, 'C': None,
             'G': None, 'F': None, 'UTIL1': None, 'UTIL2': None, 'UTIL3': None,
             'BENCH1': None, 'BENCH2': None, 'BENCH3': None
         }

         used = set()

         specific_positions = ['PG', 'SG', 'SF', 'PF', 'C']
         for pos in specific_positions:
             for player in player_data:
                 if player['name'] not in used and pos in player['positions']:
                     lineup[pos] = player
                     used.add(player['name'])
                     break
         for player in player_data:
             if player['name'] not in used and ('PG' in player['positions'] or 'SG' in player['positions']):
                 lineup['G'] = player
                 used.add(player['name'])
                 break
          
         for player in player_data:
             if player['name'] not in used and ('SF' in player['positions'] or 'PF' in player['positions']):
                 lineup['F'] = player
                 used.add(player['name'])
                 break
             
         util_positions = ['UTIL1', 'UTIL2', 'UTIL3']
         for util_pos in util_positions:
             for player in player_data:
                 if player['name'] not in used:
                     lineup[util_pos] = player
                     used.add(player['name'])
                     break
                 
         bench_positions = ['BENCH1', 'BENCH2', 'BENCH3']
         for bench_pos in bench_positions:
             for player in player_data:
                 if player['name'] not in used:
                     lineup[bench_pos] = player
                     used.add(player['name'])
                     break
         
             return lineup

    def displayLineup(self, lineup):
         print("\n Optimal Lineup:")
         starting_positions = ['PG', 'SG', 'SF', 'PF', 'C']
         for pos in starting_positions:
             if lineup[pos]:
                 player = lineup[pos]
                 print(pos + ": " + player['name'] + " (" + str(round(player['fantasy_pts'], 1)) + " FP)")
         
         flex_positions = ['G', 'F', 'UTIL1', 'UTIL2', 'UTIL3']
         for pos in flex_positions:
             if lineup[pos]:
                 player = lineup[pos]
                 print(pos + ": " + player['name'] + " (" + str(round(player['fantasy_pts'], 1)) + " FP)")

         bench_positions = ['BENCH1', 'BENCH2', 'BENCH3']
         for pos in bench_positions:
             if lineup[pos]:
                 player = lineup[pos]
                 print(pos + ": " + player['name'] + " (" + str(round(player['fantasy_pts'], 1)) + " FP)")
         
         total_fp = 0
         for pos in starting_positions + flex_positions:
             if lineup[pos]:
                 total_fp += lineup[pos]['fantasy_pts']
         print("\nTotal Active Team Points: " + str(round(total_fp, 1)))


         

               
               
               
         


#====================================================================================================================================

def main():
        seasons = ['2020-21', '2021-22', '2022-23', '2023-24', '2024-25']
        rost = Roster()
        print("\nEnter your roster (one player per line, press Enter on empty line to finish):")
        roster = []
        while True:
            player_name = input("Player name: ").strip()
            if not player_name:
                break
            roster.append(player_name)
        
        if not roster:
            print("No players entered. Exiting.")
            return
        
        #get player objects first
        print("\nAnalyzing Roster:")
        player_objects = []
        for player_name in roster:
            matches = rost.find_player(player_name)
            if len(matches) == 0:
                print("No players found for " + player_name)
                continue
            
            if len(matches) == 1:
                player = matches[0]
                print("Found: " + player['full_name'])
            else:
                player = rost.select_player(matches)
                if not player:
                    print("Skipping " + player_name)
                    continue
            
            player_objects.append(player)
        
        if not player_objects:
            print("No valid players found. Exiting.")
            return
        
        #get matchup data
        opposing_teams = rost.getPlayerMatchup(player_objects)
        
        #get matchup fantasy points
        matchup_data = {}
        for player in player_objects:
            if player['full_name'] in opposing_teams:
                opposition = opposing_teams[player['full_name']]
                matchup_fp = rost.getMatchupData(player, opposition, seasons)
                matchup_data[player['full_name']] = matchup_fp
                print(player['full_name'] + " vs " + opposition + ": " + str(round(matchup_fp, 1)) + " FP")
        
        #get positions
        positions = rost.getPlayerPositions(player_objects)
        
        sorted_players = sorted(matchup_data.items(), key=lambda x: x[1], reverse=True)
        print("Players ranked by matchup performance:")
        for i, (name, fp) in enumerate(sorted_players, 1):
             print(str(i) + ". " + name + ": " + str(round(fp, 1)) + " FP")
         
        #build optimal lineup
        optimal_lineup = rost.buildOptimalLineup(player_objects, matchup_data, positions)
        rost.displayLineup(optimal_lineup)
        
        

          #done???/ # DONE

          
         
          

          #After getting the positions, sort the players into descedning order based on fantasy points.
          #that means the best performing players should get the highest priority.
          #put the best players into roles first. so lebron would go sf instead of utilty
          #then once all the named roles are filled put them in utility. So if I have a C, but C is already full, put in utility.

          

        
             

        
        
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
