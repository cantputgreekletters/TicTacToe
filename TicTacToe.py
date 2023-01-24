class Table:
  def __init__(self):
    self.table = [[1,2,3],[4,5,6],[7,8,9]]
    self.finish = False
    self.picked = []
    self.option = {
      1: (0,0),
      2: (0,1),
      3: (0,2),
      4: (1,0),
      5: (1,1),
      6: (1,2),
      7: (2,0),
      8: (2,1),
      9: (2,2)
    }
    self.win_text = None
    self.constructor()
    pass
  
  def check(self):
    Table = self.table
    if (Table[0][0] ==  Table[1][1] and Table[0][0] == Table[2][2]) or (Table[0][2] ==  Table[1][1] and Table[0][2] == Table[2][0]):
      self.finish = True
      return
    for i in range(3):
      if (Table[i][0] == Table[i][1] and Table[i][1] == Table[i][2]) or (Table[0][i] == Table[1][i] and Table[0][i] == Table[2][i]):
        self.finish = True
        return
  
  def ShowTable(self):
    text = "-+-+-"
    text2 = "{one}|{two}|{three}"
    print(text2.format(one=self.table[0][0],two=self.table[0][1],three=self.table[0][2]))
    print(text)
    print(text2.format(one=self.table[1][0],two=self.table[1][1] ,three=self.table[1][2]))
    print(text)
    print(text2.format(one=self.table[2][0],two=self.table[2][1] ,three=self.table[2][2]))
      
        
      

  def constructor(self):
    self.finish = False
    Player1 = Player(str(input("What's your name Player1 ? = ")))
    name = str(input("What's your name Player2 ? = "))
    if name == "Bot":
      Player2 = Bot_Player()  
    else:
      Player2 = Player(name)
    while not self.finish:
      
      self.Processing(Player1,"x")
      if self.finish:
        break

      if self.check_draw():
        self.finish = True
        self.win_text = "Nobody won"
        break
      
      self.Processing(Player2,"o")  
      
    self.ShowTable()  
    print("Match has ended")
    print(self.win_text)

  def Processing(self,Player,text):
    print("=" * 20)
    self.ShowTable()
    a,b = self.option.get(Player.choose(self.picked))
    self.table[a][b] = text
    self.check()
    Player.points += 1
    self.win_text = Player.name + " won"
    return 
  
  def check_draw(self):
    for x in self.table:
      for y in x:
        if y in range(1,10):
          return False
    return True


class Player:
  def __init__(self,name = "player"):
    self.name = name
    self.points = 0
    pass
  
  def choose(self,table):
    while True:
      try:
        x = int(input("pick an option {name}: ".format(name=self.name)))
      except:
        print("Invalid option\nTry again!")
      else:
        if x in range(1,10) and not (x in table):
          break
        elif x not in range(1,10):
          print("Invalid Number\nTry Again!!!")
        elif x in table:
          print("Number already picked\nTry Again!!!")
        else:
          print("You did everything wrong\nTry again...")
    table.append(x)
    return x

class Bot_Player(Player):
  def __init__(self):
    super().__init__()
    self.name = "Bot"

  def choose(self,table):
    from random import randint as rn
    while True:
      x = rn(1,9)
      if x not in table:
        break
    table.append(x)
    return x




Game = Table()
