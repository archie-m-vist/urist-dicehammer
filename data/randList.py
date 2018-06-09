import random

touhousByGame = [
   ["Reimu", "Shingyoku", "YuugenMagan", "Mima", "Elis", "Kikuri", "Sariel", "Konngara"],
   ["Genji", "Rika", "Meira", "Marisa"],
   ["Orange", "Kurumi", "Elly", "Yuuka", "Mugetsu", "Gengetsu"],
   ["Ellen", "Kotohime", "Kana", "Rikako", "Chiyuri", "Yumemi", "Ruukoto"],
   ["Sara", "Luize", "Alice", "Yuki", "Mai (PC-98)", "Yumeko", "Shinki"],
   ["Rumia", "Daiyousei", "Cirno", "Meiling", "Koakuma", "Patchouli", "Sakuya", "Remilia", "Flandre"],
   ["Letty", "Chen", "Alice", "Lily White", "Lyrica", "Lunasa", "Merlin", "Youmu", "Yuyuko", "Ran", "Yukari"],
   ["Wriggle", "Mystia", "Keine", "Tewi", "Reisen", "Eirin", "Kaguya", "Mokou"],
   ["Aya", "Medicine", "Komachi", "Eiki"],
   ["Shizuha", "Minoriko", "Hina", "Nitori", "Momiji", "Sanae", "Kanako", "Suwako"],
   ["Kisume", "Yamame", "Parsee", "Yuugi", "Satori", "Rin", "Utsuho", "Koishi"],
   ["Nazrin", "Kogasa", "Ichirin", "Unzan", "Minamitsu", "Shou", "Byakuren", "Nue"],
   ["Kyouko", "Yoshika", "Seiga", "Tojiko", "Futo", "Miko", "Mamizou"],
   ["Wakasagihime", "Sekibanki", "Kagerou", "Benben", "Yatsuhashi", "Seija", "Shinmyoumaru", "Raiko"],
   ["Seiran", "Ringo", "Doremy", "Sagume", "Clownpiece", "Junko", "Hecatia"],
   ["Eternity", "Nemuno", "Aunn", "Narumi", "Satono", "Teireida Mai", "Okina"]
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
   ["Reisen (SSiB)", "Toyohime", "Yorihime", "Chang'e", "Tsukuyomi", "Iwakasa"],
   ["Kasen"],
   ["Kosuzu"],
   ["Maribel", "Renko"],
   ["Akyuu"]
]

# dark heresy psyker powers
biomancy = ["Agony","Bio-Lightning","Blood Boil","Cellular Control","Constrict","Drain Vigour","Enhanced Senses","Flesh Like Iron","Hammerhand","Regenerate","Seal Wounds","Shape Flesh","Toxic Siphon"]
divination = ["Divine Shot","Dowsing","Far Sight","Glimpse","Personal Augery","Precognitive Dodge","Precognitive Strike","Preternatural Awareness","Psychometry","Soul Sight"]
pyrokinesis = ["Blinding Flash","Burning Fist","Call Flame","Douse Flames","Fire Bolt","Fire Storm","Holocaust","Incinerate","Molten Man","Sculpt Flame","Wall of Fire"]
telekinesis = ["Catch Projectiles","Fling","Force Barrage","Force Bolt","Precision Telekinesis","Psychic Blade","Psychic Crush","Psychokinetic Storm","Push","Telekinesis","Telekinetic Shield"]
telepathy = ["Beastmaster","Compel","Dominate","Inspire","Mind Scan","Projection","Psychic Shriek","See Me Not","Seed Mind","Soul Killer","Telepathy","Terrify","Zone of Compulsion"]
powers = biomancy + divination + pyrokinesis + telepathy + telekinesis

# touhous
touhousPC98 = [i for lst in touhousByGame[0:5] for i in lst]
touhousPC98Returning = ["Reimu", "Marisa", "Yuuka", "Alice"]
touhousWindowsOnly = [i for lst in touhousByGame[5:] for i in lst] + [i for lst in spinoffGames for i in lst]
touhousWindows = touhousPC98Returning + touhousWindowsOnly
touhousNoPC98 = touhousWindows + [i for lst in otherTouhous for i in lst]
touhous = touhousPC98 + touhousWindowsOnly + [i for lst in otherTouhous for i in lst]

# pokemon types
poketypes = ["Normal", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy", "Steel", "Ghost", "Bug", "Rock", "Ground", "Poison", "Flying", "Fighting"]

lists = {
   "touhou" : touhous,
   "touhou modern" : touhousNoPC98,
   "touhou pc-98" : touhousPC98,
   "poketype" : poketypes,
   "power" : powers
}

def randomFromList (lst):
   if lst in lists:
      return random.choice(lists[lst])
   else:
      return None
