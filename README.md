# League of Legends insta-locker

Links:
* https://michael.kim/blog/lol-client
* https://riot-api-libraries.readthedocs.io/en/latest/ddragon.html
* https://ddragon.leagueoflegends.com/cdn/11.1.1/data/en_US/champion.json
* https://lcu.vivide.re/
* https://github.com/Remlas/lolcup-tools/blob/master/AllRequests.txt

A champion can be:
* banned
* over picked

Flow:
* Check if the client is running (if lockfile exists)
* Check if the game has been accepted (or create a function to accept a game)
* Pick the champion
* Check if no one is hovering the champion that we are going to ban
* Ban that garbage called Samira (so I need another priority list)
* Check if my champion has not been banned or over picked (if so, delete the entry from the priority list)
* Insta-lock it
* Maybe a function that detects my runes based on the champion?
  
Data structures:
* Priority list with the champions I want to pick.
* Priority list with the champions I want to ban. (not instantly)

Maybe useful things for picking a champ:
* /lol-champ-select-legacy/v1/pickable-champions

