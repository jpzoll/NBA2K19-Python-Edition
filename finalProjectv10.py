#/*  NBA 2K19: Python Edition
#finalProject.java
# Joseph Zoll
# Joe 
# jpzoll
# Section 3 */


from graphics import *
from random import randrange
from random import random

#Creates the game ball in the graphics window at the center of the court and returns it to be moved throughout the game
def drawBasketball(win):
    Basketball = Circle(Point(500, 250), 8)
    Basketball.setFill("orange")
    Basketball.draw(win)
    return Basketball

#Takes in the game ball, the coordinates of the new position, and moves it accordingly in the window
def moveBasketball(Basketball, x, y, win):
    Basketball.undraw()
    Basketball = Circle(Point(x, y), 8)
    Basketball.setFill("orange")
    Basketball.draw(win)
    return Basketball

  
#Simulates one NBA game
#Takes in the point limit so it knows when to end; Abbreviations for the scoreboard; team lists are for the player objects; team colors are for the player blip colors; team score texts and commentary text to be updated; basketball to be moved in the window
def simOneGame(pointLimit, team1Name, team1Abbreviation, team1List, team1Color, team1Num, team2Name, team2Abbreviation, team2List, team2Color, team2Num, team1ScoreText, team2ScoreText, commentaryText, Basketball, win):
#Clicking within the bounds of the ADVANCE button starts the simulation. Scores are defaulted to 0
    confirmMousePosition(775, 925, 460, 490, win) # (IMS), (FNC)
    score1 = 0
    score2 = 0
#Possesion(s) are defaulted to None because nobody has the ball yet
    Possession = None
    playerPossession = None
#Jump ball proceeds and whatever team won it has possession 
    Possession = simJumpBall(commentaryText, team1Name, team2Name) # (FNC)
#The play entry for the user's input will be drawn
    playEntry = drawChoosePlayEntry(win) # (FNC)
#While game over function continues be False, the simulation will continue
    while not gameOver(pointLimit, score1, score2): # (FNC)
        win.getMouse()
#Based on what team has the ball, the point guard will ALWAYS start with the ball
        if Possession == team1Name:
            Possession = team1Name
#team1List[0] is the point guard
            playerPossession = team1List[0]
            Basketball = moveBasketball(Basketball, 710, 255, win) # (FNC)
#This class method moves every player on team with the ball to their offensive positions
            team1OnOffense(team1List, team1Color, team1Num, team2List, team2Color, team2Num, win) # (FNC)
#One offensive play is simulated
            result, Basketball = simOffensivePlay(team1Name, team2Name, team1List, team2List, playerPossession, commentaryText, playEntry, Basketball, win) # (FNC)
#If the team scores, show ball going through the net, otherwise show it missing the net
            if result == 2 or result == 3:
                Basketball = moveBasketball(Basketball, 927, 250, win) # (FNC)
            else:
                Basketball = moveBasketball(Basketball, 920, 260, win) # (FNC)
#The other team gets the ball and the score is updated
            Possession = team2Name
            playerPossession = team2List[0]
            score1 = score1 + result
            updateScoreboard(team1Abbreviation, team2Abbreviation, team1ScoreText, team2ScoreText, team1Num, score1, score2) # (FNC)
        elif Possession == team2Name:
            Possession = team2Name
            playerPossession = team2List[0]
            Basketball = moveBasketball(Basketball, 290, 245, win) # (FNC)
            team2OnOffense(team1List, team1Color, team1Num, team2List, team2Color, team2Num, win) # (FNC)
            result, Basketball = simOffensivePlay(team1Name, team2Name, team2List, team1List, playerPossession, commentaryText, playEntry, Basketball, win) # (FNC)
            if result == 2 or result == 3:
                Basketball = moveBasketball(Basketball, 82.5, 250, win) # (FNC)
            else:
                Basketball = moveBasketball(Basketball, 90, 237.5, win) # (FNC)
            Possession = team1Name
            playerPossession = team1List[0]
            score2 = score2 + result
            updateScoreboard(team1Abbreviation, team2Abbreviation, team1ScoreText, team2ScoreText, team2Num, score1, score2) # (FNC)
#Once the game is finished, the results are displayed and the scores are returned
    if score1 > score2:
        commentaryText.setText(team1Name + " win the game! ADVANCE")
        win.getMouse()
        commentaryText.setText("FINAL SCORE: " + str(score1) + ":" + str(score2) + "      ADVANCE")
    elif score2 > score1:
        commentaryText.setText(team2Name + " win the game! ADVANCE")
        win.getMouse()
        commentaryText.setText("FINAL SCORE: " + str(score2) + ":" + str(score1) + "      ADVANCE")
        print("FINAL SCORE: " + str(score2) + ":" + str(score1))
    confirmMousePosition(775, 925, 460, 490, win) # (IMS)
    win.close()
    return score1, score2
        
        
#Takes in the scores and based on the point limit, determines if the game is over or not
def gameOver(pointLimit, score1, score2):
    scoreDifference = 0
    if score1 >= score2:
        scoreDifference = score1 - score2
    elif score2 >= score1:
        scoreDifference = score2 - score1
    if score1 >= pointLimit and scoreDifference > 1:
        return True
    elif score2 >= pointLimit and scoreDifference > 1:
        return True
    else:
        return False
  
#Simulates the jump ball and returns whoever has possesion of the ball
def simJumpBall(commentaryText, team1Name, team2Name):
    Possession = None
    jumpBallResult = random() # (RND)
    if jumpBallResult < 0.5:
        Possession = team1Name
    elif jumpBallResult >= 0.5:
        Possession = team2Name
    if Possession == team1Name:
        commentaryText.setText(team1Name + " win the jump ball! ADVANCE")
    elif Possession == team2Name:
        commentaryText.setText(team2Name + " win the jump ball! ADVANCE")
    return Possession

#Takes in the abbreviations, score texts, and scores and uses them 
def updateScoreboard(team1Abbreviation, team2Abbreviation, team1ScoreText, team2ScoreText, teamNum, score1, score2):
    if teamNum == 1:
        team1ScoreText.setText(team1Abbreviation + ": " + str(score1))
    elif teamNum == 2:
        team2ScoreText.setText(team2Abbreviation + ": " + str(score2))
 
#Makes sure the input of the desired play is valid and confirms it; takes in the list of possible choices, the error message to be drawn, play entry box to get text from it, commentary text to be updated in the graphics window
def confirmAdvancePlay(choices, commentaryErrorMessage, playEntry, commentaryText, win):
    confirmMousePosition(775, 925, 460, 490, win) # (IMS), (FNC)
    commentaryText.setSize(10)
    playValidity = checkInList(playEntry.getText(), choices) # (IEB)
    if playValidity == False:
        commentaryText.setText(commentaryErrorMessage)
        while playValidity == False:
            confirmMousePosition(775, 925, 460, 490, win) # (IMS), (FNC)
            playValidity = checkInList(playEntry.getText(), choices) # (IEB)
            if playValidity == True:
                commentaryText.setText("")
    choice = playEntry.getText() # (IEB)
    return choice

           
#Simulates a pass play based on the coordinates to move the ball; team list for whoever has possession to find the index of the specified player; team names to see what team is on offense; commentary text to be updated; play entry to get the user input; basketball to be moved in the window           
def simPassPlay(offensiveTeamListIndex, x1, x2, x3, x4, offensiveTeamList, team1Name, team2Name, commentaryText, playEntry, Basketball, win):
    playerPossession = offensiveTeamList[offensiveTeamListIndex]
    if team1Name == playerPossession.team:
        Basketball = moveBasketball(Basketball, x1, x2, win) # (FNC)
    elif team2Name == playerPossession.team:
        Basketball = moveBasketball(Basketball, x3, x4, win) # (FNC)
    commentaryText.setText(playerPossession.name + " has the ball. PASS, SHOOT, or DRIVE? ")
    chooseTypePlay = confirmAdvancePlay(["PASS", "SHOOT","DRIVE"], "This is not a valid play choice. PASS, SHOOT, or DRIVE? ", playEntry, commentaryText, win) # (FNC)
    playEntry.setText("")
    return playerPossession, team1Name, team2Name, chooseTypePlay, Basketball
    
#If the user tries passing to a player that already has the ball, it corrects them and updates the play-by-play text    
def correctPass(playerPossession, commentaryText, playEntry, win):
    commentaryText.setSize(10)
    commentaryText.setText(playerPossession.name + " already has the ball. ENTER POSITION INITIALS: ")
    passChoice = confirmAdvancePlay(['PG', 'SG', 'SF', 'PF', 'C'], "These are not valid position intials. ENTER POSITION INITIALS ", playEntry, commentaryText, win) # (FNC)
    playEntry.setText("")
    return passChoice
    
#Simulates a mid range shot. Takes in the player who has the ball to see their mid range success rate, list of player objects on defense to show they have the ball; commentary text to be updated   
def simMidRangeShot(playerPossession, defensiveTeamList, commentaryText):
    if playerPossession.midRangeSuccess == "Very Low":
                if random() < 0.10: # (RND)
                    commentaryText.setText(playerPossession.name + " pulls up for two and makes it! ADVANCE")
                    result = 2
                else:
                    commentaryText.setText(playerPossession.name + " pulls up for two and misses it! ADVANCE")
                    result = 0
    elif playerPossession.midRangeSuccess == "Low":
                if random() < 0.15: # (RND)
                    commentaryText.setText(playerPossession.name + " pulls up for two and makes it! ADVANCE")
                    result = 2
                else:
                    commentaryText.setText(playerPossession.name + " pulls up for two and misses it! ADVANCE")
                    result = 0
    elif playerPossession.midRangeSuccess == "Medium":
                if random() < 0.25: # (RND)
                    commentaryText.setText(playerPossession.name + " pulls up for two and makes it! ADVANCE")
                    result = 2
                else:
                    commentaryText.setText(playerPossession.name + " pulls up for two and misses it! ADVANCE")
                    result = 0
    elif playerPossession.midRangeSuccess == "High":
                if random() < 0.40: # (RND)
                    commentaryText.setText(playerPossession.name + " pulls up for two and makes it! ADVANCE")
                    result = 2
                else:
                    commentaryText.setText(playerPossession.name + " pulls up for two and misses it! ADVANCE")
                    result = 0
    elif playerPossession.midRangeSuccess == "Very High":
                if random() < 0.45: # (RND)
                    commentaryText.setText(playerPossession.name + " pulls up for two and makes it! ADVANCE")
                    result = 2
                else:
                    commentaryText.setText(playerPossession.name + " pulls up for two and misses it! ADVANCE")
                    result = 0
    return result

#Simulates a three point shot. Takes in the player who has the ball to see their three point success rate, list of player objects on defense to show they have the ball; commentary text to be updated
def simThreePointShot(playerPossession, defensiveTeamList, commentaryText):
    if playerPossession.threeSuccess == "Very Low":
                if random() < 0.05: # (RND)
                    commentaryText.setText(playerPossession.name + " pulls up for three and makes it! ADVANCE")
                    result = 3
                    
                else:
                    commentaryText.setText(playerPossession.name + " pulls up for three and misses it! ADVANCE")
                    result = 0
    elif playerPossession.threeSuccess == "Low":
                if random() < 0.20: # (RND)
                    commentaryText.setText(playerPossession.name + " pulls up for three and makes it! ADVANCE")
                    result = 3
                else:
                    commentaryText.setText(playerPossession.name + " pulls up for three and misses it! ADVANCE")
                    result = 0
    elif playerPossession.threeSuccess == "Medium":
                if random() < 0.33: # (RND)
                    commentaryText.setText(playerPossession.name + " pulls up for three and makes it! ADVANCE")
                    result = 3
                    
                else:
                    commentaryText.setText(playerPossession.name + " pulls up for three and misses it! ADVANCE")
                    result = 0
    elif playerPossession.threeSuccess == "High":
                if random() < 0.40: #(RND)
                    commentaryText.setText(playerPossession.name + " pulls up for three and makes it! ADVANCE")
                    result = 3
                    
                else:
                    commentaryText.setText(playerPossession.name + " pulls up for three and misses it! ADVANCE")
                    result = 0
    elif playerPossession.threeSuccess == "Very High":
                if random() < 0.45: # (RND)
                    commentaryText.setText(playerPossession.name + " pulls up for three and makes it! ADVANCE")
                    result = 3
                    
                else:
                    commentaryText.setText(playerPossession.name + " pulls up for three and misses it! ADVANCE")
                    result = 0
    return result

#Simulates a drive play/layup. Takes in the player who has the ball to see their drive success rate, list of player objects on defense to show they have the ball; commentary text to be updated
def simDrivePlay(playerPossession, defensiveTeamList, commentaryText):
    if playerPossession.driveSuccess == "Very Low":
            if random() < 0.40: # (RND)
                commentaryText.setText(playerPossession.name + " drives and makes the layup! ADVANCE")
                result = 2
                
            else:
                commentaryText.setText(playerPossession.name + " drives and misses the layup! ADVANCE")
                result = 0
    elif playerPossession.driveSuccess == "Low":
            if random() < 0.45: # (RND)
                commentaryText.setText(playerPossession.name + " drives and makes the layup! ADVANCE")
                result = 2
                
            else:
                commentaryText.setText(playerPossession.name + " drives and misses the layup! ADVANCE")
                result = 0
    elif playerPossession.driveSuccess == "Medium":
            if random() < 0.55: # (RND)
                commentaryText.setText(playerPossession.name + " drives and makes the layup! ADVANCE")
                result = 2
                
            else:
                commentaryText.setText(playerPossession.name + " drives and misses the layup! ADVANCE")
                result = 0
    elif playerPossession.driveSuccess == "High":
            if random() < 0.60: # (RND)
                commentaryText.setText(playerPossession.name + " drives and makes the layup! ADVANCE")
                result = 2
                
            else:
                commentaryText.setText(playerPossession.name + " drives and misses the layup! ADVANCE")
                result = 0
    elif playerPossession.driveSuccess == "Very High":
            if random() < 0.65: # (RND)
                commentaryText.setText(playerPossession.name + " drives and makes the layup! ADVANCE")
                result = 2
                
            else:
                commentaryText.setText(playerPossession.name + " drives and misses the layup! ADVANCE")
                result = 0
    return result
    
#Simulates one offensive play. Takes in the team names for possession info; offensive and defensive team lists for all the player objects; the player object of who has the ball; commentary text to be updated, playEntry for user input; Basketball to be moved in the window     
def simOffensivePlay(team1Name, team2Name, offensiveTeamList, defensiveTeamList, playerPossession, commentaryText, playEntry, Basketball, win):
    result = 0
    commentaryText.setText(playerPossession.name + " has the ball. PASS, SHOOT, or DRIVE? ")
    chooseTypePlay = confirmAdvancePlay(["PASS", "SHOOT","DRIVE"], "This is not a valid play choice. PASS, SHOOT, or DRIVE? ", playEntry, commentaryText, win) # (FNC)
    playEntry.setText("")
    numPassAttempts = 0
#While the user keeps choosing to pass, a pass play is simulated and the number passes is accumulated
    while chooseTypePlay == "PASS":
        numPassAttempts += 1
#If the user passes too many times in one possession, the other team will get the ball
        if numPassAttempts == 11:
            commentaryText.setText("Too many pass attempts and the shot clock has run out! ADVANCE")
            result = 0
            break
        commentaryText.setText("Pass to who? ENTER POSITION INITIALS: ")
        passChoice = confirmAdvancePlay(['PG', 'SG', 'SF', 'PF', 'C'], "These are not valid position intials. ENTER POSITION INITIALS ", playEntry, commentaryText, win) # (FNC)
        passChoice = playEntry.getText() # (IEB)
        playEntry.setText("")
        while passChoice == playerPossession.position:
            passChoice = correctPass(playerPossession, commentaryText, playEntry, win) # (FNC)
        commentaryText.setSize(10)
        if passChoice == "PG":
            playerPossession, team1Name, team2Name, chooseTypePlay, Basketball = simPassPlay(0, 710, 255, 290, 245, offensiveTeamList, team1Name, team2Name, commentaryText, playEntry, Basketball, win) # (FNC)
        elif passChoice == "SG":
            playerPossession, team1Name, team2Name, chooseTypePlay, Basketball = simPassPlay(1, 870, 440, 130, 435, offensiveTeamList, team1Name, team2Name, commentaryText, playEntry, Basketball, win) # (FNC)
        elif passChoice == "SF":
            playerPossession, team1Name, team2Name, chooseTypePlay, Basketball = simPassPlay(2, 870, 60, 130, 75, offensiveTeamList, team1Name, team2Name, commentaryText, playEntry, Basketball, win) # (FNC)
        elif passChoice == "PF":
            playerPossession, team1Name, team2Name, chooseTypePlay, Basketball = simPassPlay(3, 895, 185, 125, 310, offensiveTeamList, team1Name, team2Name, commentaryText, playEntry, Basketball, win) # (FNC)
        elif passChoice == "C":
            playerPossession, team1Name, team2Name, chooseTypePlay, Basketball = simPassPlay(4, 895, 295, 125, 205, offensiveTeamList, team1Name, team2Name, commentaryText, playEntry, Basketball, win) # (FNC)
#If the user chooses to shoot the ball, they must decide to shoot a two or a three, and the shot will be simulated    
    if chooseTypePlay == "SHOOT":
        commentaryText.setText("Shoot a TWO or a THREE? ")
        shotChoice = confirmAdvancePlay(['TWO', 'THREE'], "This is not a valid shot choice. Shoot a TWO or a THREE? ", playEntry, commentaryText, win) # (FNC)   
        if shotChoice == "TWO":
            result = simMidRangeShot(playerPossession, defensiveTeamList, commentaryText) # (FNC)
        if shotChoice == "THREE":
            result = simThreePointShot(playerPossession, defensiveTeamList, commentaryText) # (FNC)
#If the user chooses to drive and perform a layup, that drive play will be simulated
    if chooseTypePlay == "DRIVE":
        result = simDrivePlay(playerPossession, defensiveTeamList, commentaryText) # (FNC)
    #win.getMouse()
    playEntry.setText("")
#The result of this one offensive play will be returned, as well as the current state of the game ball
    return result, Basketball
        

#For each player object on both teams, move them to their respective positions on offense and defense
def team1OnOffense(team1List, team1Color, team1Num, team2List, team2Color, team2Num, win):
    for player in team1List:
        player.moveToOffense(team1Color, team1Num, win) # (FNC)
    for player in team2List:
        player.moveToDefense(team2Color, team2Num, win) # (FNC)
        
def team2OnOffense(team1List, team1Color, team1Num, team2List, team2Color, team2Num, win):
    for player in team1List:
        player.moveToDefense(team1Color, team1Num, win) # (FNC)
    for player in team2List:
        player.moveToOffense(team2Color, team2Num, win) # (FNC)

#Using the input file, read it and retrieve the info for each player object on the team
# (IFL)
def retrievePointGuardInfo(inFile):
    pgName = inFile.readline().strip('\n')
    pg3Success = inFile.readline().strip('\n')
    pgMidSuccess = inFile.readline().strip('\n')
    pgDriveSuccess = inFile.readline().strip('\n')
    return pgName, pg3Success, pgMidSuccess, pgDriveSuccess
def retrieveShootingGuardInfo(inFile):
    sgName = inFile.readline().strip('\n')
    sg3Success = inFile.readline().strip('\n')
    sgMidSuccess = inFile.readline().strip('\n')
    sgDriveSuccess = inFile.readline().strip('\n')
    return sgName, sg3Success, sgMidSuccess, sgDriveSuccess
def retrieveSmallForwardInfo(inFile):
    sfName = inFile.readline().strip('\n')
    sf3Success = inFile.readline().strip('\n')
    sfMidSuccess = inFile.readline().strip('\n')
    sfDriveSuccess = inFile.readline().strip('\n')
    return sfName, sf3Success, sfMidSuccess, sfDriveSuccess
def retrievePowerFowardInfo(inFile):
    pfName = inFile.readline().strip('\n')
    pf3Success = inFile.readline().strip('\n')
    pfMidSuccess = inFile.readline().strip('\n')
    pfDriveSuccess = inFile.readline().strip('\n')
    return pfName, pf3Success, pfMidSuccess, pfDriveSuccess
def retrieveCenterInfo(inFile):
    cName = inFile.readline().strip('\n')
    c3Success = inFile.readline().strip('\n')
    cMidSuccess = inFile.readline().strip('\n')
    cDriveSuccess = inFile.readline().strip('\n')
    return cName, c3Success, cMidSuccess, cDriveSuccess
    

#Only registers a mouse click when the user clicks within the bounds given in the parameters
def confirmMousePosition(x1, x2, y1, y2, win): # (IMS)
    withinBounds = False
    while withinBounds == False:
        mouseClick = win.getMouse()
        if not mouseClick == None:
            if mouseClick.getX() >= x1 and mouseClick.getX() <= x2 and mouseClick.getY() >= y1 and mouseClick.getY() <= y2:
                withinBounds = True
            #else:
                #withinBounds = False

#Creates for input file name based on the input in the choose team screen and gets the info for both teams
def getTeamInfo(team1Choice, team2Choice):
    team1FileName = team1Choice + ".txt"
    team2FileName = team2Choice + ".txt"
    inFile = open(team1FileName, "r") # (IFL)
    team1Name, team1Abbreviation = retrieveTeamNameInfo(inFile) # (FNC)
    inFile.readline()
    team1List = [PG1, SG1, SF1, PF1, C1] = getStartingLineupTeam1(team1Name, inFile) # (FNC)
    inFile = open(team2FileName, "r") # (IFL)
    team2Name, team2Abbreviation = retrieveTeamNameInfo(inFile) # (FNC)
    inFile.readline()
    team2List = [PG2, SG2, SF2, PF2, C2] = getStartingLineupTeam2(team2Name, inFile) # (FNC)
    return team1List, team1Name, team1Abbreviation, team2List, team2Name, team2Abbreviation


#Gets the info for the team name and abbreviation
def retrieveTeamNameInfo(inFile):
    teamNameInfo = inFile.readline()
    teamNameInfo = teamNameInfo.split('-')
    teamName = teamNameInfo[0].strip()
    teamAbbreviation = (teamNameInfo[1].strip('\n')).strip()
    return teamName, teamAbbreviation

#Reads input file and creates the player objects for team 1
def getStartingLineupTeam1(teamName, inFile):
    pgName, pg3Success, pgMidSuccess, pgDriveSuccess = retrievePointGuardInfo(inFile) # (FNC)
    inFile.readline()
    sgName, sg3Success, sgMidSuccess, sgDriveSuccess = retrieveShootingGuardInfo(inFile) # (FNC)
    inFile.readline()
    sfName, sf3Success, sfMidSuccess, sfDriveSuccess = retrieveSmallForwardInfo(inFile) # (FNC)
    inFile.readline()
    pfName, pf3Success, pfMidSuccess, pfDriveSuccess = retrievePowerFowardInfo(inFile) # (FNC)
    inFile.readline()
    cName, c3Success, cMidSuccess, cDriveSuccess = retrieveCenterInfo(inFile) # (FNC)
    inFile.readline()
    
    # (CLOD)
    PG1 = Player(pgName, teamName, "PG", pg3Success, pgMidSuccess, pgDriveSuccess)
    SG1 = Player(sgName, teamName, "SG", sg3Success, sgMidSuccess, sgDriveSuccess)
    SF1 = Player(sfName, teamName, "SF", sf3Success, sfMidSuccess, sfDriveSuccess)
    PF1 = Player(pfName, teamName, "PF", pf3Success, pfMidSuccess, pfDriveSuccess)
    C1 = Player(cName, teamName, "C", c3Success, cMidSuccess, cDriveSuccess)
        
    # (LOOD)
    teamList = [PG1, SG1, SF1, PF1, C1]
    return teamList

#Reads input file and creates the player objects for team 2
def getStartingLineupTeam2(teamName, inFile):
    pgName, pg3Success, pgMidSuccess, pgDriveSuccess = retrievePointGuardInfo(inFile) # (FNC)
    inFile.readline()
    sgName, sg3Success, sgMidSuccess, sgDriveSuccess = retrieveShootingGuardInfo(inFile) # (FNC)
    inFile.readline()
    sfName, sf3Success, sfMidSuccess, sfDriveSuccess = retrieveSmallForwardInfo(inFile) # (FNC)
    inFile.readline()
    pfName, pf3Success, pfMidSuccess, pfDriveSuccess = retrievePowerFowardInfo(inFile) # (FNC)
    inFile.readline()
    cName, c3Success, cMidSuccess, cDriveSuccess = retrieveCenterInfo(inFile) # (FNC)
    
    # (CLOD)
    PG2 = Player(pgName, teamName, "PG", pg3Success, pgMidSuccess, pgDriveSuccess)
    SG2 = Player(sgName, teamName, "SG", sg3Success, sgMidSuccess, sgDriveSuccess)
    SF2 = Player(sfName, teamName, "SF", sf3Success, sfMidSuccess, sfDriveSuccess)
    PF2 = Player(pfName, teamName, "PF", pf3Success, pfMidSuccess, pfDriveSuccess)
    C2 = Player(cName, teamName, "C", c3Success, cMidSuccess, cDriveSuccess)
    
    # (LOOD)
    teamList = [PG2, SG2, SF2, PF2, C2]
    return teamList

#Creates the welcome screen
def welcomeScreen():
    win = GraphWin("NBA 2K19: Python Edition", 1000, 500) # (GW)
    win.setBackground("lightblue")
    titleText1, titleText2 = welcomeText(win) # (FNC)
    startButton, startButtonText = drawStartButton(win) # (FNC)
    return win, titleText1, titleText2, startButton, startButtonText

#Creates the welcome text in the first window
def welcomeText(win):
    titleText1 = Text(Point(500, 100), "Welcome To" ) # (OTXT)
    titleText1.setSize(18)
    #titleText1.setStyle("bold")
    titleText2 = Text(Point(500, 150), "NBA 2K19: Python Edition") # (OTXT)
    titleText2.setSize(18)
    titleText2.setStyle("bold")
    titleText1.draw(win)
    titleText2.draw(win)
    return titleText1, titleText2

#Creates the start button in the first window
def drawStartButton(win):
    startButton = Rectangle(Point(400, 250), Point(600, 200))
    startButton.setFill("red")
    startButton.draw(win)
    startButtonText = Text(Point(500, 225), "Click here to start") # (OTXT)
    startButtonText.draw(win)
    return startButton, startButtonText

#Transitions from the welcome screen to the choose team screen
def switchToChooseTeamScreen(titleText1, titleText2, startButton, startButtonText, win):
    startButton.undraw()
    startButtonText.undraw()
    
#Draws the components of the choose team screen
def drawChooseTeamScreen(win):
    team1Entry = Entry(Point(500, 225), 12)
    team2Entry = Entry(Point(500, 275), 12)
    team1Entry.draw(win)
    team2Entry.draw(win)
    team1Text = Text(Point(500, 200), "Team 1") # (OTXT)
    team2Text = Text(Point(500, 250), "Team 2") # (OTXT)
    team1Text.draw(win)
    team2Text.draw(win)
    submitButton = Rectangle(Point(565, 235), Point(635, 212.5))
    submitButton.setFill("lightgrey")
    submitButton.draw(win)
    submitText = Text(Point(600, 223.75), "Submit") # (OTXT)
    submitText.draw(win)
    return team1Entry, team2Entry, team1Text, team2Text, submitText, submitButton


#Transitions from the choose team screen to the point limit input screen
def switchToInputLimitScreen(team1Entry, team2Entry, team1Text, team2Text, submitText, submitButton, win):
    team2Entry.undraw()
    team2Text.undraw()
    team1Text.undraw()
    team1Entry.undraw()
    submitButton.undraw()
    submitText.undraw()
    pointLimitBox, limitText, submitText, submitButton = drawPointLimitEntryScreen(win) # (FNC)
    return pointLimitBox, limitText, submitText, submitButton

#Transitions to team color input screen
def switchToInputColorScreen(limitText, pointLimitBox, win):
    teamColorText = limitText
    teamColorText.setText("Team 1 Color")
    teamColorEntry = pointLimitBox
    teamColorEntry.setText("")
    return teamColorText, teamColorEntry

#Draws the point limit entry screen   
def drawPointLimitEntryScreen(win):
    pointLimitBox = Entry(Point(500, 225), 12)
    pointLimitBox.draw(win)
    limitText = Text(Point(500, 200), "Point Limit") # (OTXT)
    limitText.draw(win)
    submitButton = Rectangle(Point(565, 235), Point(635, 212.5))
    submitButton.setFill("lightgrey")
    submitButton.draw(win)
    submitText = Text(Point(600, 223.75), "Submit") # (OTXT)
    submitText.draw(win)
    return pointLimitBox, limitText, submitText, submitButton

#Gets the point limit for the game based on the users input in the pointLimitBox in the first graphics window
def getPointLimit(pointLimitBox, win):
    availablePointLimits = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
    confirmMousePosition(565, 635, 212.5, 235, win) # (IMS), (FNC)
    limitValidity = checkInList(pointLimitBox.getText(), availablePointLimits) # (FNC)
    if limitValidity == False:
        limitErrorText1 = Text(Point(500, 250), "This is not a valid point limit. Please try again.") # (OTXT)
        limitErrorText2 = Text(Point(500, 275), "(Point limits from 2 to 30 are allowed)") # (OTXT)
        limitErrorText1.draw(win)
        limitErrorText2.draw(win)
        while limitValidity == False:
            confirmMousePosition(565, 635, 212.5, 235, win) # (IMS), (FNC)
            limitValidity = checkInList(pointLimitBox.getText(), availablePointLimits) # (FNC)
            if limitValidity == True:
                limitErrorText1.undraw()
                limitErrorText2.undraw()
    pointLimit = int(pointLimitBox.getText())
    return pointLimit

#Based on the input in the choose team screen, gets team 1 and team 2
def getTeams(team1Entry, team2Entry, win):
    NBATeams = ['Cavaliers', 'Celtics', 'Heat', 'Knicks', 'Lakers', 'Rockets', 'Thunder', 'Warriors']
    guideLineMessage = Text(Point(500, 310), "Choose 2 of the following teams:\nCavaliers, Celtics, Heat, Knicks, Lakers, Rockets, Thunder, Warriors") # (OTXT)
    guideLineMessage.draw(win)
    confirmMousePosition(565, 635, 212.5, 235, win) # (IMS), (FNC)
    guideLineMessage.undraw()
    team1Validity = checkInList(team1Entry.getText(), NBATeams) # (IEB), (FNC)
    team2Validity = checkInList(team2Entry.getText(), NBATeams) # (IEB), (FNC)
    if (team1Validity == False) or (team2Validity == False):
        teamErrorText1 = Text(Point(500, 300), "At least one of your team choices are invalid. Please pick two of the following teams:\n Cavaliers, Celtics, Heat, Knicks, Lakers, Rockets, Thunder, Warriors") # (OTXT)
        teamErrorText2 = Text(Point(500, 325), "(Make sure only the first letter in the team name is capitalized. Team input file must be present as well)") # (OTXT)
        teamErrorText1.draw(win)
        teamErrorText2.draw(win)
        while (team1Validity == False) or (team2Validity == False):
            confirmMousePosition(565, 635, 212.5, 235, win) # (IMS), (FNC)
            team1Validity = checkInList(team1Entry.getText(), NBATeams) # (IEB), (FNC)
            team2Validity = checkInList(team2Entry.getText(), NBATeams) # (IEB), (FNC)
            if (team1Validity == True) and (team2Validity == True):
                teamErrorText1.undraw()
                teamErrorText2.undraw()
    team1Choice = team1Entry.getText() # (IEB)
    team2Choice = team2Entry.getText() # (IEB)
    return team1Choice, team2Choice
        
#Gets the color for team 1 and team 2
def getTeamColorInfo(teamColorEntry, teamColorText, win):
    availableColors = ["red", "blue", "yellow", "green", "purple", "orange", "white", "black", "grey", "brown"]
    confirmMousePosition(565, 635, 212.5, 235, win) # (IMS), (FNC)
    colorValidity = checkInList(teamColorEntry.getText(), availableColors) # (IEB), (FNC)
    if colorValidity == False:
        errorText1 = Text(Point(500, 250), "This is not a valid color. Please try again.") # (OTXT)
        errorText2 = Text(Point(500, 275), "(Make sure all letters typed in are in lower case)") # (OTXT)
        errorText1.draw(win)
        errorText2.draw(win)
        while colorValidity == False:
            confirmMousePosition(565, 635, 212.5, 235, win) # (IMS), (FNC)
            colorValidity = checkInList(teamColorEntry.getText(), availableColors) # (IEB), (FNC)
            if colorValidity == True:
                errorText1.undraw()
                errorText2.undraw()
    team1Color = teamColorEntry.getText() # (IEB)
    teamColorEntry.setText("")
    teamColorText.setText("Team 2 Color")
    confirmMousePosition(565, 635, 212.5, 235, win) # (IMS), (FNC)
    colorValidity = checkInList(teamColorEntry.getText(), availableColors) # (IEB), (FNC)
    if colorValidity == False:
        errorText1 = Text(Point(500, 250), "This is not a valid color. Please try again.") # (OTXT)
        errorText2 = Text(Point(500, 275), "(Make sure all letters typed in are in lower case)") # (OTXT)
        errorText1.draw(win)
        errorText2.draw(win)
        while colorValidity == False:
            confirmMousePosition(565, 635, 212.5, 235, win) # (IMS), (FNC)
            colorValidity = checkInList(teamColorEntry.getText(), availableColors) # (IEB), (FNC)
            if colorValidity == True:
                errorText1.undraw()
                errorText2.undraw()
    team2Color = teamColorEntry.getText() # (IEB)
    return team1Color, team2Color

#Transitions to the rules screen
def switchToRulesScreen(teamColorText, teamColorEntry, submitText, submitButton, titleText1, titleText2, win):
    teamColorText.undraw()
    teamColorEntry.undraw()
    submitText.undraw()
    submitButton.undraw()
    titleText1.undraw()
    titleText2.undraw()

#Transitions to the main game screen
def switchToMainGameScreen(rulesTitle, rule1, rule2, rule3, rule4, rule5, win):
    rulesTitle.undraw()
    rule1.undraw()
    rule2.undraw()
    rule3.undraw()
    rule4.undraw()
    rule5.undraw()
    win.setBackground("white")
    drawBasketballCourt(win) # (FNC)

#Draws every player object in the respective team list at jump ball position in the first window
def drawPlayersAtJumpball(teamList, teamColor, teamNum, win):
    for player in teamList:
        player.draw(teamColor, teamNum, win) # (FNC)

#Checks if the desired item is in the list of choices
def checkInList(chosenItem, list):
    for item in list:
        if chosenItem == item:
            Valid = True
            break
        else:
            Valid = False
    return Valid
        
    
#Draws the rules of the game
def rulesText(win):
    rulesTitle = Text(Point(500, 65), "Rules") # (OTXT)
    rulesTitle.setSize(18)
    rulesTitle.setStyle("bold")
    rulesTitle.draw(win)
    rule1 = Text(Point(500, 100), "This simulation requires 1-2 users") # (OTXT)
    rule1.draw(win)
    rule2 = Text(Point(500, 150), "The simulation will begin with a tipoff/jump ball.") # (OTXT)
    rule2.draw(win)
    rule3 = Text(Point(500, 200), "Click the ADVANCE button to forward through each play and portion of the game. Make sure all input is typed in ALL CAPS") # (OTXT)
    rule3.draw(win)
    rule4 = Text(Point(500, 250), "Based on who is on offense and how many users are participating in the simulation, the user(s) must type in the desired strategy for each possesion") # (OTXT)
    rule4.setSize(11)
    rule4.draw(win)
    rule5 = Text(Point(500, 300), "While there is a point limit, the simulation will not end until a team wins by 2 or 3.\n CLICK ANYWHERE TO CONTINUE") # (OTXT)
    rule5.draw(win)
    return rulesTitle, rule1, rule2, rule3, rule4, rule5

#Draws the basketball court to the graphics window
def drawBasketballCourt(win):
    courtOutline = Rectangle(Point(50, 450), Point(950, 50))
    courtOutline.draw(win)
    midLine = Line(Point(500, 450), Point(500, 50))
    midLine.draw(win)
    centerCircle = Circle(Point(500, 250), 35)
    centerCircle.draw(win)
    leftPaint = Rectangle(Point(50, 285), Point(180, 215))
    leftPaint.draw(win)
    rightPaint = Rectangle(Point(820, 285), Point(950, 215))
    rightPaint.draw(win)
    leftPaintCircle = Circle(Point(180, 250), 35)
    leftPaintCircle.draw(win)
    rightPaintCircle = Circle(Point(820, 250), 35)
    rightPaintCircle.draw(win)
    leftThreePointCircle = Circle(Point(50, 250), 178)
    leftThreePointCircle.draw(win)
    leftCircleCover = Rectangle(Point(0, 450), Point(49, 50))
    leftCircleCover.setFill("white")
    leftCircleCover.setOutline("white")
    leftCircleCover.draw(win)
    rightThreePointCircle = Circle(Point(950, 250), 178)
    rightThreePointCircle.draw(win)
    rightCircleCover = Rectangle(Point(1000, 450), Point(951, 50))
    rightCircleCover.setFill("white")
    rightCircleCover.setOutline("white")
    rightCircleCover.draw(win)
    leftGlass = Line(Point(75, 267.5), Point(75, 227.5))
    leftGlass.draw(win)
    rightGlass = Line(Point(935, 267.5), Point(935, 227.5))
    rightGlass.draw(win)
    leftNet = Circle(Point(80, 247.5), 5)
    leftNet.draw(win)
    rightNet = Circle(Point(930, 247.5), 5)
    rightNet.draw(win)
    return courtOutline, midLine, centerCircle, leftPaint, rightPaint, leftPaintCircle, rightPaintCircle, leftThreePointCircle, leftCircleCover, rightThreePointCircle, rightCircleCover, leftGlass, rightGlass, leftNet, rightNet
 
#Draws the scoreboard based on the abbreviations of the teams 
def drawScoreBoard(win, team1Abbreviation, team2Abbreviation):
    team1Score = 0
    team2Score = 0
    team1ScoreText = Text(Point(130, 35), team1Abbreviation + ": " + str(team1Score)) # (OTXT)
    team1ScoreText.setSize(15)
    team1ScoreText.draw(win)
    team2ScoreText = Text(Point(870, 35), team2Abbreviation + ": " + str(team2Score)) # (OTXT)
    team2ScoreText.setSize(15)
    team2ScoreText.draw(win)
    return team1Score, team2Score, team1ScoreText, team2ScoreText

#Draw the entry box for the player to input desired plays
def drawChoosePlayEntry(win):
    playEntry = Entry(Point(500, 475), 15)
    playEntry.draw(win)
    return playEntry

#Draws the play-by-play commentary text
def drawCommentaryText(win):
    commentaryText = Text(Point(200, 475), "Tipoff! ADVANCE") # (OTXT)
    commentaryText.setSize(10)
    commentaryText.draw(win)
    return commentaryText

#Draws the advance button
def drawAdvanceButton(win):
    advanceText = Text(Point(850, 475), "Click To Advance") # (OTXT)
    advanceText.draw(win)
    advanceButton = Rectangle(Point(775, 490), Point(925, 460))
    advanceButton.draw(win)

#Creates the second and final graphics window
def exitScreen():
    win = GraphWin("NBA 2K19: Python Edition", 1000, 500) # (GW)
    win.setBackground("lightblue")
    return win

#Gets the info from the last game to update the game history
def getNewGameHistoryInfo(team1Name, team2Name, score1, score2):
    matchup = team1Name + " V.S." + team2Name
    if score1 > score2:
        finalScore = str(score1) + "-" + str(score2)
        winner = team1Name
    else:
        finalScore = str(score2) + "-" + str(score1)
        winner = team2Name
        
    return matchup, finalScore, winner

#Draws the game history
def drawGameHistory(win):
    titleText = Text(Point(500, 40), "Game History") # (OTXT)
    titleText.setSize(17)
    titleText.setStyle("bold")
    titleText.draw(win)
    teamText = Text(Point(250, 75), "Past Matchups") # (OTXT)
    teamText.setSize(15)
    teamText.draw(win)
    scoreText = Text(Point(500, 75), "Scores") # (OTXT)
    scoreText.setSize(15)
    scoreText.draw(win)
    winnerText = Text(Point(750, 75), "Winners") # (OTXT)
    winnerText.setSize(15)
    winnerText.draw(win)
  
#Updates the game history lists based on the new info gathered
# (IFL)
def updateGameHistoryLists(matchup, finalScore, winner, outFile):
    matchupList = (outFile.readline().strip('\n')).split(';')
    matchupList.pop(-1)
    outFile.readline()
    scoresList = outFile.readline().strip('\n').split(';')
    scoresList.pop(-1)
    outFile.readline()
    winnerList = outFile.readline().strip('\n').split(';')
    winnerList.pop(-1)
    if len(matchupList) >= 15:
        matchupList.pop(0)
    if len(scoresList) >= 15:
        scoresList.pop(0)
    if len(winnerList) >= 15:
        winnerList.pop(0)
    matchupList.append(matchup) 
    scoresList.append(finalScore)
    winnerList.append(winner)
    return matchupList, scoresList, winnerList

#Updates and draws the game history based on the new info gathered     
def updateGameHistory(matchup, finalScore, winner, win):
    outFile = open("finalProjectOutput.txt", "r") # (IFL)
    matchupList, scoresList, winnerList = updateGameHistoryLists(matchup, finalScore, winner, outFile) # (FNC)
    y = 80
    for matchup in matchupList:
        y += 25
        matchupText = Text(Point(250, y), matchup) # (OTXT)
        matchupText.draw(win)
    y = 80
    for score in scoresList:
        y += 25
        scoreText = Text(Point(500, y), score) # (OTXT)
        scoreText.draw(win)
    y = 80
    for winner in winnerList:
        y += 25
        winnerText = Text(Point(750, y), winner) # (OTXT)
        winnerText.draw(win)
    outFile = open("finalProjectOutput.txt", "w") # (OFL)
    
    for matchupStr in matchupList:
        print(matchupStr, end = ";", file = outFile) # (OFL)
    print("\n", file = outFile)
    for scoreStr in scoresList:
        print(scoreStr, end = ";", file = outFile) # (OFL)
    print("\n", file = outFile)
    for winnerStr in winnerList:
        print(winnerStr, end = ";", file = outFile) # (OFL)
    print("\n", file = outFile)
    outFile.close()
        
# (CLOD)
class Player: 
    def __init__(self, name, team, position, threeSuccessRate, midRangeSuccessRate, driveSuccessRate):
        self.name = name
        self.team = team
        self.position = position
        self.threeSuccess = threeSuccessRate
        self.midRangeSuccess = midRangeSuccessRate
        self.driveSuccess = driveSuccessRate
   
#Draws the player objects at their starting positions. They are colored based on the team color and the teamNum determines what team they are on
    def draw(self, teamColor, teamNum,  win):
        if teamNum == 1:
            if self.position == "PG":
                blipPosition = Point(195, 250)
            elif self.position == "SG":
                blipPosition = Point(450, 350)
            elif self.position == "SF":
                blipPosition = Point(450, 150)
            elif self.position == "PF":
                blipPosition = Point(350, 250)
            elif self.position == "C":
                blipPosition = Point(485, 250)
        elif teamNum == 2:
            if self.position == "PG":
                blipPosition = Point(805, 250)
            elif self.position == "SG":
                blipPosition = Point(550, 350)
            elif self.position == "SF":
                blipPosition = Point(550, 150)
            elif self.position == "PF":
                blipPosition = Point(650, 250)
            elif self.position == "C":
                blipPosition = Point(515, 250)
        self.blip = Circle(blipPosition, 10)
        self.blip.setFill(teamColor)
        self.blip.draw(win)
        
        
#Moves the drawn player blips to their offensive positions
    def moveToOffense(self, teamColor, teamNum, win):
        if teamNum == 1:
            if self.position == "PG":
                offensivePosition = Point(700, 250)
            elif self.position == "SG":
                offensivePosition = Point(860, 430)
            elif self.position == "SF":
                offensivePosition = Point(860, 70)
            elif self.position == "PF":
                offensivePosition = Point(885, 195)
            elif self.position == "C":
                offensivePosition = Point(885, 305)
        elif teamNum == 2:
            if self.position == "PG":
                offensivePosition = Point(300, 250)
            elif self.position == "SG":
                offensivePosition = Point(140, 430)
            elif self.position == "SF":
                offensivePosition = Point(140, 70)
            elif self.position == "PF":
                offensivePosition = Point(115, 305)
            elif self.position == "C":
                offensivePosition = Point(115, 195)
        self.blip.undraw()
        self.blip = Circle(offensivePosition, 10)
        self.blip.setFill(teamColor)
        self.blip.draw(win)
    
#Moves the drawn player blips to their defensive positions
    def moveToDefense(self, teamColor, teamNum, win):
        if teamNum == 1:
            if self.position == "PG":
                offensivePosition = Point(240, 250)
            elif self.position == "SG":
                offensivePosition = Point(120, 380)
            elif self.position == "SF":
                offensivePosition = Point(130, 120)
            elif self.position == "PF":
                offensivePosition = Point(100, 215)
            elif self.position == "C":
                offensivePosition = Point(100, 285)
        elif teamNum == 2:
            if self.position == "PG":
                offensivePosition = Point(760, 250)
            elif self.position == "SG":
                offensivePosition = Point(880, 380)
            elif self.position == "SF":
                offensivePosition = Point(870, 120)
            elif self.position == "PF":
                offensivePosition = Point(900, 215)
            elif self.position == "C":
                offensivePosition = Point(900, 285)
        self.blip.undraw()
        self.blip = Circle(offensivePosition, 10)
        self.blip.setFill(teamColor)
        self.blip.draw(win)
     
#Undraws the player blip
    def undrawBlip(self):
        self.blip.undraw()
        
def main():
#The program begins with the first graphics window, with all the text and start button, being drawn together as the welcome screen
    win, titleText1, titleText2, startButton, startButtonText = welcomeScreen() # (FNC)
#Waits for the user to click the start button to proceed    
    confirmMousePosition(400, 600, 200, 250, win) # (IMS), (FNC)
#All the unneeded parts of the welcome screen are undrawn and there is a transition to the next screen    
    switchToChooseTeamScreen(titleText1, titleText2, startButton, startButtonText, win) # (FNC)
#The entry boxes and other new objects are drawn to create the screen to input the new teams
    team1Entry, team2Entry, team1Text, team2Text, submitText, submitButton = drawChooseTeamScreen(win) # (FNC)
#This function determines the teams that will be used in the simulation and assigns them to variables
    team1Choice, team2Choice = getTeams(team1Entry, team2Entry, win) # (FNC)
#All the unneeded parts of the choose team screen are undrawn and there is a transition to the point limit input screen
    pointLimitBox, limitText, submitText, submitButton = switchToInputLimitScreen(team1Entry, team2Entry, team1Text, team2Text, submitText, submitButton, win) # (FNC)
#This function determines the point limit for the game that will be played 
    pointLimit = getPointLimit(pointLimitBox, win) # (FNC)
#All the unneeded parts of the point limit input screen are undrawn and there is a transition to the team color input screen
    teamColorText, teamColorEntry = switchToInputColorScreen(limitText, pointLimitBox, win) # (FNC)
#The team colors are determined through the user's input in each entry box
    team1Color, team2Color = getTeamColorInfo(teamColorEntry, teamColorText, win) # (FNC)

#There is a transition from the team color input screen to the rules screen based on the user's click
    switchToRulesScreen(teamColorText, teamColorEntry, submitText, submitButton, titleText1, titleText2, win) # (FNC)
#The rules for the game are drawn for the user to read and understand. Once the user is ready to proceed to the simulation they can click and it will close the rules screen    
    rulesTitle, rule1, rule2, rule3, rule4, rule5 = rulesText(win) # (FNC)
    win.getMouse()

#There is a transition to the main game screen
    switchToMainGameScreen(rulesTitle, rule1, rule2, rule3, rule4, rule5, win) # (FNC)
#Based on the input file's information, both team's players, name, and abbreviation will be retrieved based on the input on the choose team screen
    team1List, team1Name, team1Abbreviation, team2List, team2Name, team2Abbreviation = getTeamInfo(team1Choice, team2Choice) # (FNC)
#Using the graphics window created and the team abbreviation's retrieved, the scoreboard will be drawn    
    team1Score, team2Score, team1ScoreText, team2ScoreText = drawScoreBoard(win, team1Abbreviation, team2Abbreviation) # (FNC)
#Both teams are assigned their respective number that will be used for drawing the players at jump ball
    team1Num = 1
    team2Num = 2
#Team 1 and 2's players are drawn at jumpball based on the player info retrieved from the input file, as well as the team color info retrieved from the input screen
    drawPlayersAtJumpball(team1List, team1Color, team1Num, win) # (FNC)
    drawPlayersAtJumpball(team2List, team2Color, team2Num, win) # (FNC)
#The game ball is drawn
    Basketball = drawBasketball(win) # (FNC)
#The simulation UI is drawn. Specifically, the play-by-play text and the advance button
    commentaryText = drawCommentaryText(win) # (FNC)
    drawAdvanceButton(win) # (FNC)

#Based on all the information received through the user's input, the simulation will take place and produce the two scores from it
    score1, score2, = simOneGame(pointLimit, team1Name, team1Abbreviation, team1List, team1Color, team1Num, team2Name, team2Abbreviation, team2List, team2Color, team2Num, team1ScoreText, team2ScoreText, commentaryText, Basketball, win) # (FNC)

#After the user pressed ADVANCE one more time, the main window wil close and the final screen will open with a second graphics window    
    win2 = exitScreen() # (FNC)

#Based on the results of the last game, the new simulation/game history will be gathered
    matchup, finalScore, winner = getNewGameHistoryInfo(team1Name, team2Name, score1, score2) # (FNC)
#The game/simulation will be drawn to the new graphics window based on the newly gathered and updated information
    drawGameHistory(win2) # (FNC)
    updateGameHistory(matchup, finalScore, winner, win2) # (FNC)

#On the user's final click, the window will close the program will be finished
    win2.getMouse()
    win2.close()


        
main()