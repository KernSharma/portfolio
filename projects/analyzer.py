#Lets lock in bud

from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playergamelog
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import leagueseasonmatchups
import pandas as pd



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
    '''
    def getPositions(self, roster):
         positions = []
         print("Now input the players position(PG,SF,SG,C,G,F,UTIL,BEN):")
         print("press enter on an empty line to finish")
         for i in roster:
             while True:
                  
               pos = input(i + ": ").upper().strip()
               if not pos:
                    break
               if pos not in ["PG", "SG", "PF", "SF", "C", "G", "F", "UTIL","BEN"]:
                  print("invalid position.")
               else:
                    positions.append(pos)
                    break
         return positions
    
    def getMatchup(self, roster, positions):
         for i in range(len(roster)-1):
              print(positions[i] + ": " + roster[i["full_name"]])
              '''
    #maybe unnecessary 

    def getPlayerMatchup(self, roster):
         print("Enter the team abbreviation(LAL, BOS, ATL) the player is playing against(Press enter on an empty line to quit): ")
         opposing_teams = {}
         for player in roster:
              
               while True:
                    team = input(player['full_name'] + ": ").strip().upper()
                    if not team:
                         break
                    if teams.find_team_by_abbreviation(team, teams = teams).strip().upper() == team:
                         opposing_teams.update(player['full_name'], team)
                    else:
                         print("thats not a team brotosynthesis")
                         break
               if not opposing_teams:
                    print("No teams entered. Exiting")
                    break
         return opposing_teams


    def getMatchupData(self, player, opposition,seasons):
         fantasy_pts = 0.0
         for season in seasons:
          log = playergamelog.PlayerGameLog(player_id= player['id'], season=season)
          data = log.get_data_frames()[0]
          player_vs_opp = data[data['MATCHUP'].str.contains(opposition,na = False)]

          if len(data) > 0:
               fantasy_pts  = ((player_vs_opp['PTS'] * 1.0) + (player_vs_opp['AST'] * 1.5) + (player_vs_opp['REB'] * 1.2) + (player_vs_opp['STL'] * 3) + (player_vs_opp['BLK'] * 3) - (player_vs_opp['TOV'] * 1) + (player_vs_opp['FG3M'] * 0.5))
          
          return fantasy_pts
     


               
               
               
         


#====================================================================================================================================

def main():
        seasons = ['2020-21', '2021-22', '2022-23', '2023-24', '2024-25']
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
        
        rost.analyze_roster(roster)
        opposing_team = rost.getPlayerMatchup(roster)

        data = {}
        for player in roster:
             opposition = opposing_team[player['full_name']]
             data.update(player, rost.getMatchupData(player['full_name'],opposition,seasons))
          
          #now i have å dictionary of players and their projected fantasy points against that specific team
          #now i need to get their positions so they can fit the roster
          #Remember: PG SG PF SF C C G F UTIL123 and 3 BEN
          #lowest 3 scores should go on the benches
          #individual players can have multiple roles(SG, PF, PG)
          #UTIITY does not care about roles
          #Create a dictionary of {position, player name}

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
