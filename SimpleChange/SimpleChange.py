def changeemulator():
    newemulator = PlayniteApi.Dialogs.SelectString('Input emulator name', 'Change emulator', 'RetroArch')
    newprofile = PlayniteApi.Dialogs.SelectString('Input profile name', 'Change emulator profile', 'Genesis Plus GX')
    for game in PlayniteApi.MainView.SelectedGames:
        emulator = Emulator()
        emulator.Id, emulator.Profiles, emulator.Name = emuidsearch(newemulator.SelectedString)
        try:
            gametask = GameAction()
            gametask.Type = GameActionType.Emulator
            gametask.EmulatorId = emulator.Id
            gametask.EmulatorProfileId = emuprofilesearch(emulator.Profiles, newprofile.SelectedString)
            game.PlayAction = gametask
            PlayniteApi.Database.Games.Update(game)
        except Exception as identifier:
            __logger.Error(str(identifier))


def emuprofilesearch(profiles, emuprofile):
    for profile in profiles:
        if profile.Name == emuprofile:
            return profile.Id


def emuidsearch(emu):
    for item in PlayniteApi.Database.Emulators:
        if item.Name == emu:
            return item.Id, item.Profiles, item.Name


def changeextension():
    oldextension = PlayniteApi.Dialogs.SelectString('Old extension, with a dot', 'Change extension', '')
    newextension = PlayniteApi.Dialogs.SelectString('New extension, with a dot', 'Change extension', '.7z')
    for game in PlayniteApi.MainView.SelectedGames:
        try:
            if (oldextension.SelectedString in game.GameImagePath) and (len(oldextension.SelectedString)>0):
                newGameImagePath = game.GameImagePath.replace(oldextension.SelectedString, newextension.SelectedString)
                game.GameImagePath = newGameImagePath
                PlayniteApi.Database.Games.Update(game)
        except Exception as identifier:
            __logger.Error(str(identifier))
