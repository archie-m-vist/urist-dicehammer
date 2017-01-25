import random

touhousByGame = [
   ["Reimu", "Shingyoku", "YuugenMagan", "Mima", "Elis", "Kikuri", "Sariel", "Konngara"],
   ["Genji", "Rika", "Meira"],
   ["Orange", "Kurumi", "Elly", "Yuuka", "Mugetsu", "Gengetsu"],
   ["Ellen", "Kotohime", "Kana", "Rikako", "Chiyuri", "Yumemi", "Ruukoto"],
   ["Sara", "Luize", "Alice", "Yuki", "Mai", "Yumeko", "Shinki"],
   ["Rumia", "Daiyousei" "Cirno", "Meiling", "Koakuma", "Patchouli", "Sakuya", "Remilia", "Flandre"],
   ["Letty", "Chen", "Alice", "Lily White", "Lyrica", "Lunasa", "Merlin", "Youmu", "Yuyuko", "Ran", "Yukari"],
   ["Wriggle", "Mystia", "Keine", "Tewi", "Reisen", "Eirin", "Kaguya", "Mokou"],
   ["Aya", "Medicine", "Komachi", "Eiki"],
   ["Shizuha", "Minoriko", "Hina", "Nitori", "Momiji", "Sanae", "Kanako", "Suwako"],
   ["Kisume", "Yamame", "Parsee", "Yuugi", "Satori", "Rin", "Utsuho", "Koishi"],
   ["Nazrin", "Kogasa", "Ichirin", "Unzan", "Murasa", "Shou", "Byakuren", "Nue"],
   ["Kyouko", "Yoshika", "Seiga", "Tojiko", "Futo", "Miko", "Mamizou"],
   ["Wakasagihime", "Sekibanki", "Kagerou", "Benben", "Yatsuhashi", "Seija", "Shinmyoumaru", "Raiko"],
   ["Seiran", "Ringo", "Doremy", "Sagume", "Clownpiece", "Junko", "Hecatia"]
]

spinoffNumbers = {
   7.5 : 0,
   9.5 : 1,
   12.5 : 2,
   13.5 : 3,
   14.5 : 4
}

spinoffGames = [
   ["Suika"],
   ["Iku", "Tenshi"],
   ["Hatate"],
   ["Kokoro"],
   ["Sumireko"]
]

otherTouhous = [
   ["Rinnosuke", "Tokiko"],
   ["Luna", "Star", "Sunny"], 
   ["Rei'sen", "Toyohime", "Yorihime", "Chang'e", "Tsukuyomi", "Iwakasa"],
   ["Kasen"],
   ["Kosuzu"],
   ["Maribel", "Renko"],
   ["Akyuu"]
]

touhousPC98 = [i for lst in touhousByGame[0:5] for i in lst]
touhousPC98Returning = ["Reimu", "Marisa", "Yuuka", "Alice"]
touhousWindowsOnly = [i for lst in touhousByGame[5:] for i in lst] + [i for lst in spinoffGames for i in lst]
touhousWindows = touhousPC98Returning + touhousWindowsOnly
touhous = touhousPC98 + touhousWindowsOnly + [i for lst in otherTouhous for i in lst]

poketypes = ["Normal", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy", "Steel", "Ghost", "Bug", "Rock", "Ground", "Poison", "Flying", "Fighting"]

lists = {
   "touhou" : touhous,
   "poketype" : poketypes
}

def randomFromList (lst):
   if lst in lists:
      return random.choice(lists[lst])
   else:
      return None