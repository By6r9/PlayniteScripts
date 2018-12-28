import re


def simpleimport():
    __logger.Info('-----------')
    import os
    import sys
    import re
    from os import listdir
    try:
        os.chdir('Extensions\\SimpleImport')
    except:
        pass

    import ConfigParser
    Config = ConfigParser.ConfigParser()
    try:
        Config.read("romimport.ini")
    except Exception as identifier:
        __logger.Error('No config file? ' + str(identifier))
        PlayniteApi.Dialogs.ShowMessage('No config file?')
    PlayniteApi.Dialogs.ShowMessage('Start import.')

    try:
        for section in Config.sections():
            __logger.Info(str(section))
            gamepath = str(Config.get(section.title(), "Path"))
            gameplatform = str(Config.get(section.title(), "Platform"))
            emu = str(Config.get(section.title(), "Emulator"))
            emuprofile = str(Config.get(section.title(), "EmulatorProfile"))
            for gamefile in files(str(Config.get(section.title(), "Path"))):
                # check if file is in database
                if not checkdatabase(Config.get(section.title(), "Path") + gamefile):
                    try:
                        # __logger.Info(str(gamefile))
                        simpleaddgame(gamefile, gamepath, gameplatform, emu, emuprofile)
                    except Exception as identifier:
                        __logger.Error(str(identifier))
    except Exception as identifier:
        __logger.Error('Wrong named section? ' + str(identifier))
    __logger.Info('End')


def simpleaddgame(gamefile, gamepath, gameplatform, emu, emuprofile):
    new_game = Game((os.path.splitext(gamefile)[0]).split(' (')[0])
    if 'redump' in gamepath:
        new_game.Source = 'Redump'
    elif 'nointro' in gamepath:
        new_game.Source = 'No-Intro'

    new_game.Region = addregion(gamefile)
    new_game.Version = addversion(gamefile)

    new_game.GameImagePath = gamepath + gamefile
    new_game.InstallDirectory = gamepath
    new_game.IsInstalled = True
    new_game.PlatformId = platformidsearch(gameplatform)

    emulator = Emulator()
    emulator.Id, emulator.Profiles, emulator.Name = emuidsearch(emu)

    try:
        gametask = GameAction()
        gametask.Type = GameActionType.Emulator
        gametask.EmulatorId = emulator.Id
        gametask.EmulatorProfileId = emuprofilesearch(emulator.Profiles, emuprofile)
        new_game.PlayAction = gametask
    except Exception as identifier:
        __logger.Error(str(identifier))

    try:
        PlayniteApi.Database.AddGame(new_game)
        PlayniteApi.Database.UpdateGame(new_game)
        __logger.Info('ADDED:' + gamefile + ' (' + gameplatform + ':' + gamepath + ')')
        with open('added.log', 'a') as f:
            f.write('ADDED:' + gamefile + ' (' + gameplatform + ':' + gamepath + ')' + '\n')
    except Exception as identifier:
        __logger.Error(identifier)


def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def addregion(gamefile):
    # Region (always first group)
    p = re.findall(r'\(.*?\)', str(gamefile))
    if len(p) > 0:
        return str(p[0]).replace("(", "").replace(")", "")


def addversion(gamefile):
    p = re.findall(r'\(.*?\)', str(gamefile))
    if len(p) > 1:
        versions = ''
        for item in p[1:]:
            # if you want to skip (Disc x) part
            # if 'Disc' not in item:
            if '--------' not in item:
                versions += str(item) + ','
        if versions.endswith(','):
            # __logger.Info('ver :' + str(versions[:-1]))
            versions = versions[0:-1]
            # __logger.Info('ver:' + str(versions))
        return versions.replace("(", "").replace(")", "").replace(",", ", ")


def emuprofilesearch(profiles, emuprofile):
    for profile in profiles:
        if profile.Name == emuprofile:
            return profile.Id


def platformidsearch(platform):
    for item in PlayniteApi.Database.GetPlatforms():
        if item.Name == platform:
            return item.Id


def emuidsearch(emu):
    for item in PlayniteApi.Database.GetEmulators():
        if item.Name == emu:
            return item.Id, item.Profiles, item.Name


def checkdatabase(path):
    result = False
    for game in PlayniteApi.Database.GetGames():
        if str(game.GameImagePath) == path:
            result = True
    return result


def SimpleFilename():
    import os
    for game in PlayniteApi.MainView.SelectedGames:
        # __logger.Info(str(game.Name))
        # __logger.Info(str(game.GameImagePath))
        head, tail = os.path.split(game.GameImagePath)
        tail = os.path.splitext(tail)[0]
        game.Name = str(tail.split(' (')[0])
        PlayniteApi.Database.UpdateGame(game)

        
def SimpleRegionVersionSource():
    import re
    import os
    for game in PlayniteApi.MainView.SelectedGames:
        __logger.Info(str(game.Name))
        # split path and filename
        head, tail = os.path.split(game.GameImagePath)
        # Source
        if (game.Source == None) or (game.Source == ''):
            if 'nointro' in game.GameImagePath:
                game.Source = 'No-Intro'
                PlayniteApi.Database.UpdateGame(game)
            if 'redump' in game.GameImagePath:
                game.Source = 'Redump'
                PlayniteApi.Database.UpdateGame(game)
        p = re.findall(r'\(.*?\)', str(tail))
        # region
        if len(p) > 0:
            game.Region = str(p[0]).replace("(", "").replace(")", "")
            PlayniteApi.Database.UpdateGame(game)
        # versions
        if len(p) > 1:
            versions = ''
            for item in p[1:]:
                # if you want to skip (Disc x) part
                # if 'Disc' not in item:
                if '--------' not in item:
                    versions += str(item) + ','
            if versions.endswith(','):
                versions = versions[0:-1]

            game.Version = versions.replace("(", "").replace(")", "").replace(",", ", ")
            PlayniteApi.Database.UpdateGame(game)        
        

def SimpleMarkRemoved():
    import os.path
    # __logger.Info('SMR:' + str(len(PlayniteApi.MainView.SelectedGames)))
    PlayniteApi.Dialogs.ShowMessage('Games to check: ' + str(len(PlayniteApi.Database.GetGames())))
    counter = 0
    for game in PlayniteApi.Database.GetGames():
        if str(PlayniteApi.Database.GetPlatform(game.PlatformId)) != 'PC':
            if os.path.isfile(game.GameImagePath) is False:
                # state = GameState()
                # state.Installed = False
                # game.State = state
                game.IsInstalled = False
                __logger.Info('SMR:' + game.GameImagePath)
                PlayniteApi.Database.UpdateGame(game)
                counter += 1

    if counter > 0:
            PlayniteApi.Dialogs.ShowMessage('Marked: ' + str(counter))


def ChangeEmulator():
    newemulator = PlayniteApi.Dialogs.SelectString('Input emulator name', 'Change emulator', '')
    newprofile = PlayniteApi.Dialogs.SelectString('Input profile name', 'Change emulator profile', '')
    for game in PlayniteApi.MainView.SelectedGames:
        emulator = Emulator()
        emulator.Id, emulator.Profiles, emulator.Name = emuidsearch(newemulator.SelectedString)
        __logger.Info(str(emulator.Name))
        try:
            gametask = GameAction()
            gametask.Type = GameActionType.Emulator
            gametask.EmulatorId = emulator.Id
            gametask.EmulatorProfileId = emuprofilesearch(emulator.Profiles, newprofile.SelectedString)
            game.PlayAction = gametask
        except Exception as identifier:
            __logger.Error(str(identifier))
        PlayniteApi.Database.UpdateGame(game)
        
