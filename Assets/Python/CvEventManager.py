from CvPythonExtensions import *
from Core import (
    civilization,
    civilizations,
    get_data_from_upside_down_map,
    human,
    text,
    message,
    player,
    team,
    cities,
)
import CvEspionageAdvisor
import CvUtil
import CvScreensInterface
import CvDebugTools
import CvWBPopups
from MiscData import MODNET_EVENTS
import PyHelpers
import Popup as PyPopup
import CvCameraControls
import CvTopCivs
import CvAdvisorUtils
from PyUtils import percentage_chance, rand, choice
from RFCUtils import getBaseUnit, getUniqueUnit
import random
from Consts import MessageData
from CityMapData import CITIES_MAP
from CoreTypes import Building, Wonder, Promotion, Project, Improvement, Feature, Unit, Bonus

## Ultrapack ##
import WBCityEditScreen
import WBUnitScreen
import WBPlayerScreen
import WBGameDataScreen
import WBPlotScreen
import CvPlatyBuilderScreen

## Ultrapack ##

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

# globals
###################################################
class CvEventManager(object):

    global iImpBeforeCity
    iImpBeforeCity = 0

    def __init__(self):
        #################### ON EVENT MAP ######################
        self.bCtrl = False
        self.bShift = False
        self.bAlt = False
        self.bAllowCheats = False

        # OnEvent Enums
        self.EventLButtonDown = 1
        self.EventLcButtonDblClick = 2
        self.EventRButtonDown = 3
        self.EventBack = 4
        self.EventForward = 5
        self.EventKeyDown = 6
        self.EventKeyUp = 7

        self.__LOG_MOVEMENT = 0
        self.__LOG_BUILDING = 0
        self.__LOG_COMBAT = 0
        self.__LOG_CONTACT = 0
        self.__LOG_IMPROVEMENT = 1
        self.__LOG_CITYLOST = 0
        self.__LOG_CITYBUILDING = 0
        self.__LOG_TECH = 0
        self.__LOG_UNITBUILD = 0
        self.__LOG_UNITKILLED = 0  # Rhye
        self.__LOG_UNITLOST = 0
        self.__LOG_UNITPROMOTED = 0
        self.__LOG_UNITSELECTED = 0
        self.__LOG_UNITPILLAGE = 0
        self.__LOG_GOODYRECEIVED = 0
        self.__LOG_GREATPERSON = 0
        self.__LOG_RELIGION = 0
        self.__LOG_RELIGIONSPREAD = 0
        self.__LOG_GOLDENAGE = 0
        self.__LOG_ENDGOLDENAGE = 0
        self.__LOG_WARPEACE = 0
        self.__LOG_PUSH_MISSION = 0

        ## EVENTLIST
        self.EventHandlerMap = {
            "mouseEvent": self.onMouseEvent,
            "kbdEvent": self.onKbdEvent,
            "ModNetMessage": self.onModNetMessage,
            "Init": self.onInit,
            "Update": self.onUpdate,
            "UnInit": self.onUnInit,
            "OnSave": self.onSaveGame,
            "OnPreSave": self.onPreSave,
            "OnLoad": self.onLoadGame,
            "GameStart": self.onGameStart,
            "GameEnd": self.onGameEnd,
            "plotRevealed": self.onPlotRevealed,
            "plotFeatureRemoved": self.onPlotFeatureRemoved,
            "plotPicked": self.onPlotPicked,
            "nukeExplosion": self.onNukeExplosion,
            "gotoPlotSet": self.onGotoPlotSet,
            "BeginGameTurn": self.onBeginGameTurn,
            "EndGameTurn": self.onEndGameTurn,
            "BeginPlayerTurn": self.onBeginPlayerTurn,
            "EndPlayerTurn": self.onEndPlayerTurn,
            "endTurnReady": self.onEndTurnReady,
            "combatResult": self.onCombatResult,
            "combatLogCalc": self.onCombatLogCalc,
            "combatLogHit": self.onCombatLogHit,
            "improvementBuilt": self.onImprovementBuilt,
            "improvementDestroyed": self.onImprovementDestroyed,
            "routeBuilt": self.onRouteBuilt,
            "firstContact": self.onFirstContact,
            "cityBuilt": self.onCityBuilt,
            "cityRazed": self.onCityRazed,
            "cityAcquired": self.onCityAcquired,
            "cityAcquiredAndKept": self.onCityAcquiredAndKept,
            "cityLost": self.onCityLost,
            "cultureExpansion": self.onCultureExpansion,
            "cityGrowth": self.onCityGrowth,
            "cityDoTurn": self.onCityDoTurn,
            "cityBuildingUnit": self.onCityBuildingUnit,
            "cityBuildingBuilding": self.onCityBuildingBuilding,
            "cityRename": self.onCityRename,
            "cityHurry": self.onCityHurry,
            "selectionGroupPushMission": self.onSelectionGroupPushMission,
            "unitMove": self.onUnitMove,
            "unitSetXY": self.onUnitSetXY,
            "unitCreated": self.onUnitCreated,
            "unitBuilt": self.onUnitBuilt,
            "unitKilled": self.onUnitKilled,
            "unitLost": self.onUnitLost,
            "unitPromoted": self.onUnitPromoted,
            "unitSelected": self.onUnitSelected,
            "UnitRename": self.onUnitRename,
            "unitPillage": self.onUnitPillage,
            "unitSpreadReligionAttempt": self.onUnitSpreadReligionAttempt,
            "unitGifted": self.onUnitGifted,
            "unitBuildImprovement": self.onUnitBuildImprovement,
            "goodyReceived": self.onGoodyReceived,
            "greatPersonBorn": self.onGreatPersonBorn,
            "buildingBuilt": self.onBuildingBuilt,
            "projectBuilt": self.onProjectBuilt,
            "techAcquired": self.onTechAcquired,
            "techSelected": self.onTechSelected,
            "religionFounded": self.onReligionFounded,
            "religionSpread": self.onReligionSpread,
            "religionRemove": self.onReligionRemove,
            "corporationFounded": self.onCorporationFounded,
            "corporationSpread": self.onCorporationSpread,
            "corporationRemove": self.onCorporationRemove,
            "goldenAge": self.onGoldenAge,
            "endGoldenAge": self.onEndGoldenAge,
            "chat": self.onChat,
            "victory": self.onVictory,
            "vassalState": self.onVassalState,
            "changeWar": self.onChangeWar,
            "setPlayerAlive": self.onSetPlayerAlive,
            "playerChangeAllCivics": self.onPlayerChangeAllCivics,  # Absinthe: Python Event for civic changes
            "playerChangeSingleCivic": self.onPlayerChangeSingleCivic,  # Absinthe: Python Event for civic changes
            "playerChangeStateReligion": self.onPlayerChangeStateReligion,
            "playerGoldTrade": self.onPlayerGoldTrade,
            "windowActivation": self.onWindowActivation,
            "gameUpdate": self.onGameUpdate,  # sample generic event
        }

        ################## Events List ###############################
        #
        # Dictionary of Events, indexed by EventID (also used at popup context id)
        # entries have name, beginFunction, applyFunction [, randomization weight...]
        #
        # Normal events first, random events after
        #
        ################## Events List ###############################
        self.Events = {
            CvUtil.EventEditCityName: (
                "EditCityName",
                self.__eventEditCityNameApply,
                self.__eventEditCityNameBegin,
            ),
            CvUtil.EventPlaceObject: (
                "PlaceObject",
                self.__eventPlaceObjectApply,
                self.__eventPlaceObjectBegin,
            ),
            CvUtil.EventAwardTechsAndGold: (
                "AwardTechsAndGold",
                self.__eventAwardTechsAndGoldApply,
                self.__eventAwardTechsAndGoldBegin,
            ),
            CvUtil.EventEditUnitName: (
                "EditUnitName",
                self.__eventEditUnitNameApply,
                self.__eventEditUnitNameBegin,
            ),
            ## Platy Builder ##
            CvUtil.EventWBLandmarkPopup: (
                "WBLandmarkPopup",
                self.__eventWBLandmarkPopupApply,
                self.__eventWBScriptPopupBegin,
            ),
            CvUtil.EventShowWonder: (
                "ShowWonder",
                self.__eventShowWonderApply,
                self.__eventShowWonderBegin,
            ),
            1111: (
                "WBPlayerScript",
                self.__eventWBPlayerScriptPopupApply,
                self.__eventWBScriptPopupBegin,
            ),
            2222: (
                "WBCityScript",
                self.__eventWBCityScriptPopupApply,
                self.__eventWBScriptPopupBegin,
            ),
            3333: (
                "WBUnitScript",
                self.__eventWBUnitScriptPopupApply,
                self.__eventWBScriptPopupBegin,
            ),
            4444: (
                "WBGameScript",
                self.__eventWBGameScriptPopupApply,
                self.__eventWBScriptPopupBegin,
            ),
            5555: (
                "WBPlotScript",
                self.__eventWBPlotScriptPopupApply,
                self.__eventWBScriptPopupBegin,
            ),
            ## Platy Builder ##
        }

    #################### EVENT STARTERS ######################
    def handleEvent(self, argsList):
        "EventMgr entry point"
        # extract the last 6 args in the list, the first arg has already been consumed
        self.origArgsList = argsList  # point to original
        tag = argsList[0]  # event type string
        idx = len(argsList) - 6
        bDummy = False
        self.bDbg, bDummy, self.bAlt, self.bCtrl, self.bShift, self.bAllowCheats = argsList[idx:]
        ret = 0
        gc.getGame().logMsg("Something")
        if self.EventHandlerMap.has_key(tag):
            fxn = self.EventHandlerMap[tag]
            ret = fxn(argsList[1:idx])
        return ret

    #################### EVENT APPLY ######################
    def beginEvent(self, context, argsList=-1):
        "Begin Event"
        entry = self.Events[context]
        return entry[2](argsList)

    def applyEvent(self, argsList):
        "Apply the effects of an event"
        context, playerID, netUserData, popupReturn = argsList

        if context == CvUtil.PopupTypeEffectViewer:
            return CvDebugTools.g_CvDebugTools.applyEffectViewer(
                playerID, netUserData, popupReturn
            )

        entry = self.Events[context]

        if context not in CvUtil.SilentEvents:
            self.reportEvent(entry, context, (playerID, netUserData, popupReturn))
        return entry[1](playerID, netUserData, popupReturn)  # the apply function

    def reportEvent(self, entry, context, argsList):
        "Report an Event to Events.log"
        if gc.getGame().getActivePlayer() != -1:
            message = "DEBUG Event: %s (%s)" % (
                entry[0],
                gc.getActivePlayer().getCivilizationShortDescription(0),
            )
            CyInterface().addImmediateMessage(message, "")
            CvUtil.pyPrint(message)
        return 0

    #################### ON EVENTS ######################
    def onKbdEvent(self, argsList):
        "keypress handler - return 1 if the event was consumed"

        eventType, key, mx, my, px, py = argsList
        game = gc.getGame()

        if self.bAllowCheats:
            # notify debug tools of input to allow it to override the control
            argsList = (
                eventType,
                key,
                self.bCtrl,
                self.bShift,
                self.bAlt,
                mx,
                my,
                px,
                py,
                gc.getGame().isNetworkMultiPlayer(),
            )
            if CvDebugTools.g_CvDebugTools.notifyInput(argsList):
                return 0

        if eventType == self.EventKeyDown:
            theKey = int(key)

            CvCameraControls.g_CameraControls.handleInput(theKey)

            if self.bAllowCheats:
                # Shift - T (Debug - No MP)
                if theKey == int(InputTypes.KB_T):
                    if self.bShift:
                        self.beginEvent(CvUtil.EventAwardTechsAndGold)
                        # self.beginEvent(CvUtil.EventCameraControlPopup)
                        return 1

                elif theKey == int(InputTypes.KB_W):
                    if self.bShift and self.bCtrl:
                        self.beginEvent(CvUtil.EventShowWonder)
                        return 1

                # Shift - ] (Debug - currently mouse-overd unit, health += 10
                elif theKey == int(InputTypes.KB_LBRACKET) and self.bShift:
                    unit = CyMap().plot(px, py).getUnit(0)
                    if not unit.isNone():
                        d = min(unit.maxHitPoints() - 1, unit.getDamage() + 10)
                        unit.setDamage(d, PlayerTypes.NO_PLAYER)

                # Shift - [ (Debug - currently mouse-overd unit, health -= 10
                elif theKey == int(InputTypes.KB_RBRACKET) and self.bShift:
                    unit = CyMap().plot(px, py).getUnit(0)
                    if not unit.isNone():
                        d = max(0, unit.getDamage() - 10)
                        unit.setDamage(d, PlayerTypes.NO_PLAYER)

                elif theKey == int(InputTypes.KB_F1):
                    if self.bShift:
                        CvScreensInterface.replayScreen.showScreen(False)
                        return 1
                    # don't return 1 unless you want the input consumed

                elif theKey == int(InputTypes.KB_F2):
                    if self.bShift:
                        CvScreensInterface.showDebugInfoScreen()
                        return 1

                elif theKey == int(InputTypes.KB_F3):
                    if self.bShift:
                        CvScreensInterface.showDanQuayleScreen(())
                        return 1

                elif theKey == int(InputTypes.KB_F4):
                    if self.bShift:
                        CvScreensInterface.showUnVictoryScreen(())
                        return 1

        return 0

    def onModNetMessage(self, argsList):
        "Called whenever CyMessageControl().sendModNetMessage() is called - this is all for you modders!"
        iData1, iData2, iData3, iData4, iData5 = argsList
        if iData1 == MODNET_EVENTS["CHANGE_COMMERCE_PERCENT"]:
            CommerceType = [
                CommerceTypes.COMMERCE_GOLD,
                CommerceTypes.COMMERCE_RESEARCH,
                CommerceTypes.COMMERCE_CULTURE,
                CommerceTypes.COMMERCE_ESPIONAGE,
            ]
            gc.getPlayer(iData2).changeCommercePercent(CommerceType[iData3], iData4)
            if iData2 == CyGame().getActivePlayer():
                screen = CvEspionageAdvisor.CvEspionageAdvisor().getScreen()
                if screen.isActive():
                    CvEspionageAdvisor.CvEspionageAdvisor().updateEspionageWeights()

        CvUtil.pyPrint("onModNetMessage")

    def onInit(self, argsList):
        "Called when Civ starts up"
        CvUtil.pyPrint("OnInit")

    def onUpdate(self, argsList):
        "Called every frame"
        fDeltaTime = argsList[0]

        # allow camera to be updated
        CvCameraControls.g_CameraControls.onUpdate(fDeltaTime)

    def onWindowActivation(self, argsList):
        "Called when the game window activates or deactivates"
        bActive = argsList[0]

    def onUnInit(self, argsList):
        "Called when Civ shuts down"
        CvUtil.pyPrint("OnUnInit")

    def onPreSave(self, argsList):
        "called before a game is actually saved"
        CvUtil.pyPrint("OnPreSave")

    def onSaveGame(self, argsList):
        "return the string to be saved - Must be a string"
        return ""

    def onLoadGame(self, argsList):
        CvAdvisorUtils.resetNoLiberateCities()
        return 0

    def onGameStart(self, argsList):
        "Called at the start of the game"

        # Rhye - Dawn of Man must appear in late starts too
        # Duplicate with Assets/Python/Contrib/CvAllErasDawnOfManScreenEventManager.py
        if (
            gc.getGame().getStartEra() == gc.getDefineINT("STANDARD_ERA")
            or gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_START)
        ) and player().isAlive():
            popupInfo = CyPopupInfo()
            popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
            popupInfo.setText(u"showDawnOfMan")
            popupInfo.addPopup(human())
        else:
            CyInterface().setSoundSelectionReady(True)

        if gc.getGame().isPbem() and player().isAlive():
            popupInfo = CyPopupInfo()
            popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_DETAILS)
            popupInfo.setOption1(True)
            popupInfo.addPopup(human())

        CvAdvisorUtils.resetNoLiberateCities()

    def onGameEnd(self, argsList):
        "Called at the End of the game"
        return

    def onBeginGameTurn(self, argsList):
        "Called at the beginning of the end of each turn"
        iGameTurn = argsList[0]
        CvTopCivs.CvTopCivs().turnChecker(iGameTurn)

    def onEndGameTurn(self, argsList):
        "Called at the end of the end of each turn"
        iGameTurn = argsList[0]

    def onBeginPlayerTurn(self, argsList):
        "Called at the beginning of a players turn"
        iGameTurn, iPlayer = argsList

    def onEndPlayerTurn(self, argsList):
        "Called at the end of a players turn"
        iGameTurn, iPlayer = argsList

        if gc.getGame().getElapsedGameTurns() == 1:
            if gc.getPlayer(iPlayer).isHuman():
                if gc.getPlayer(iPlayer).canRevolution(0):
                    popupInfo = CyPopupInfo()
                    popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_CHANGECIVIC)
                    popupInfo.addPopup(iPlayer)

        CvAdvisorUtils.resetAdvisorNags()
        CvAdvisorUtils.endTurnFeats(iPlayer)

    def onEndTurnReady(self, argsList):
        iGameTurn = argsList[0]

    def onFirstContact(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Contact"
        iTeamX, iHasMetTeamY = argsList
        if not self.__LOG_CONTACT:
            return
        CvUtil.pyPrint("Team %d has met Team %d" % (iTeamX, iHasMetTeamY))

    def onCombatResult(self, argsList):
        "Combat Result"
        pWinner, pLoser = argsList
        playerX = PyPlayer(pWinner.getOwner())
        unitX = PyInfo.UnitInfo(pWinner.getUnitType())
        playerY = PyPlayer(pLoser.getOwner())
        unitY = PyInfo.UnitInfo(pLoser.getUnitType())
        if not self.__LOG_COMBAT:
            return
        if playerX and playerX and unitX and playerY:
            CvUtil.pyPrint(
                "Player %d Civilization %s Unit %s has defeated Player %d Civilization %s Unit %s"
                % (
                    playerX.getID(),
                    playerX.getCivilizationName(),
                    unitX.getDescription(),
                    playerY.getID(),
                    playerY.getCivilizationName(),
                    unitY.getDescription(),
                )
            )
        # Absinthe: Gediminas Tower wonder effect: extra city defence on unit win in the city
        pPlayer = gc.getPlayer(pWinner.getOwner())
        if pPlayer.countNumBuildings(Wonder.GEDIMINAS_TOWER) > 0:
            pPlot = pWinner.plot()
            if pPlot.isCity():
                pCity = pPlot.getPlotCity()
                if pCity.getNumActiveBuilding(Wonder.GEDIMINAS_TOWER):
                    pCity.changeDefenseDamage(-10)
        # Absinthe: Gediminas Tower end

    def onCombatLogCalc(self, argsList):
        "Combat Result"
        genericArgs = argsList[0][0]
        cdAttacker = genericArgs[0]
        cdDefender = genericArgs[1]
        iCombatOdds = genericArgs[2]
        CvUtil.combatMessageBuilder(cdAttacker, cdDefender, iCombatOdds)

    def onCombatLogHit(self, argsList):
        "Combat Message"
        global gCombatMessages, gCombatLog
        genericArgs = argsList[0][0]
        cdAttacker = genericArgs[0]
        cdDefender = genericArgs[1]
        iIsAttacker = genericArgs[2]
        iDamage = genericArgs[3]

        if cdDefender.eOwner == cdDefender.eVisualOwner:
            szDefenderName = gc.getPlayer(cdDefender.eOwner).getNameKey()
        else:
            szDefenderName = text("TXT_KEY_TRAIT_PLAYER_UNKNOWN")
        if cdAttacker.eOwner == cdAttacker.eVisualOwner:
            szAttackerName = gc.getPlayer(cdAttacker.eOwner).getNameKey()
        else:
            szAttackerName = text("TXT_KEY_TRAIT_PLAYER_UNKNOWN")

        if iIsAttacker == 0:
            combatMessage = text(
                "TXT_KEY_COMBAT_MESSAGE_HIT",
                szDefenderName,
                cdDefender.sUnitName,
                iDamage,
                cdDefender.iCurrHitPoints,
                cdDefender.iMaxHitPoints,
            )
            CyInterface().addCombatMessage(cdAttacker.eOwner, combatMessage)
            CyInterface().addCombatMessage(cdDefender.eOwner, combatMessage)
            if cdDefender.iCurrHitPoints <= 0:
                combatMessage = text(
                    "TXT_KEY_COMBAT_MESSAGE_DEFEATED",
                    szAttackerName,
                    cdAttacker.sUnitName,
                    szDefenderName,
                    cdDefender.sUnitName,
                )
                CyInterface().addCombatMessage(cdAttacker.eOwner, combatMessage)
                CyInterface().addCombatMessage(cdDefender.eOwner, combatMessage)
        elif iIsAttacker == 1:
            combatMessage = text(
                "TXT_KEY_COMBAT_MESSAGE_HIT",
                szAttackerName,
                cdAttacker.sUnitName,
                iDamage,
                cdAttacker.iCurrHitPoints,
                cdAttacker.iMaxHitPoints,
            )
            CyInterface().addCombatMessage(cdAttacker.eOwner, combatMessage)
            CyInterface().addCombatMessage(cdDefender.eOwner, combatMessage)
            if cdAttacker.iCurrHitPoints <= 0:
                combatMessage = text(
                    "TXT_KEY_COMBAT_MESSAGE_DEFEATED",
                    szDefenderName,
                    cdDefender.sUnitName,
                    szAttackerName,
                    cdAttacker.sUnitName,
                )
                CyInterface().addCombatMessage(cdAttacker.eOwner, combatMessage)
                CyInterface().addCombatMessage(cdDefender.eOwner, combatMessage)

    def onImprovementBuilt(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Improvement Built"
        iImprovement, iX, iY = argsList
        # Absinthe: Stephansdom start
        if iImprovement == Improvement.COTTAGE:
            pPlot = CyMap().plot(iX, iY)
            iOwner = pPlot.getOwner()
            # if there is an owner
            if iOwner >= 0:
                pOwner = gc.getPlayer(iOwner)
                if pOwner.countNumBuildings(Wonder.STEPHANSDOM) > 0:
                    pPlot.setImprovementType(Improvement.HAMLET)
        # Absinthe: Stephansdom end
        if not self.__LOG_IMPROVEMENT:
            return
        CvUtil.pyPrint(
            "Improvement %s was built at %d, %d"
            % (PyInfo.ImprovementInfo(iImprovement).getDescription(), iX, iY)
        )

    def onImprovementDestroyed(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Improvement Destroyed"
        iImprovement, iOwner, iX, iY = argsList
        if not self.__LOG_IMPROVEMENT:
            return
        CvUtil.pyPrint(
            "Improvement %s was Destroyed at %d, %d"
            % (PyInfo.ImprovementInfo(iImprovement).getDescription(), iX, iY)
        )
        # Absinthe: Free walls if city is built on a fort
        #             This is a hack for it, checking what was the improvement before the city was built
        #             Saving the improvement type and coordinates here as a global variable, and accessing later in the onCityBuilt function
        global iImpBeforeCity
        iImpBeforeCity = 10000 * iImprovement + 100 * iX + 1 * iY

    def onRouteBuilt(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Route Built"
        iRoute, iX, iY = argsList
        if not self.__LOG_IMPROVEMENT:
            return
        CvUtil.pyPrint(
            "Route %s was built at %d, %d" % (gc.getRouteInfo(iRoute).getDescription(), iX, iY)
        )

    def onPlotRevealed(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Plot Revealed"
        pPlot = argsList[0]
        iTeam = argsList[1]

    def onPlotFeatureRemoved(self, argsList):
        "Plot Revealed"
        # Absinthe: mistake in the Firaxis code, argslist should be switched around:
        pPlot = argsList[0]
        iFeatureType = argsList[2]
        pCity = argsList[1]  # This can be null

        # Absinthe: remove specific resources if the forest/dense forest/palm forest was cut down:
        if pPlot.getBonusType(-1) != -1:  # only proceed if there is a bonus resource on the plot
            if (
                iFeatureType == gc.getInfoTypeForString("FEATURE_FOREST")
                or iFeatureType == Feature.DENSEFOREST
                or iFeatureType == Feature.PALMFOREST
            ):
                iBonusType = pPlot.getBonusType(-1)
                if iBonusType in [Bonus.TIMBER, Bonus.DEER, Bonus.FUR]:
                    pPlot.setBonusType(-1)
                    # also remove corresponding improvements
                    iImprovementType = pPlot.getImprovementType()
                    if (
                        iImprovementType == Improvement.CAMP
                    ):  # camp is only buildable on resources, while lumbermills are removed by default on forest removal
                        pPlot.setImprovementType(-1)
                    # Absinthe: message for the human player if it was inside it's territory
                    iOwner = pPlot.getOwner()
                    if iOwner == human():
                        message(
                            iOwner,
                            text(
                                "TXT_KEY_NO_FOREST_NO_RESOURCE",
                                gc.getBonusInfo(iBonusType).getTextKey(),
                            ),
                            sound="AS2D_DISCOVERBONUS",
                            event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                            button=gc.getBonusInfo(iBonusType).getButton(),
                            color=MessageData.LIME,
                            location=pPlot,
                        )

    def onPlotPicked(self, argsList):
        "Plot Picked"
        pPlot = argsList[0]
        CvUtil.pyPrint("Plot was picked at %d, %d" % (pPlot.getX(), pPlot.getY()))

    def onNukeExplosion(self, argsList):
        "Nuke Explosion"
        pPlot, pNukeUnit = argsList
        CvUtil.pyPrint("Nuke detonated at %d, %d" % (pPlot.getX(), pPlot.getY()))

    def onGotoPlotSet(self, argsList):
        "Nuke Explosion"
        pPlot, iPlayer = argsList

    def onBuildingBuilt(self, argsList):
        "Building Completed"
        pCity, iBuildingType = argsList
        iPlayer = pCity.getOwner()
        pPlayer = gc.getPlayer(iPlayer)

        # Absinthe: Leaning Tower start
        if iBuildingType == Wonder.LEANING_TOWER:
            iX = pCity.getX()
            iY = pCity.getY()
            iUnit = Unit.GREAT_PROPHET + rand(7)
            pNewUnit = pPlayer.initUnit(
                iUnit,
                iX,
                iY,
                UnitAITypes(gc.getUnitInfo(iUnit).getDefaultUnitAIType()),
                DirectionTypes.NO_DIRECTION,
            )
            if player().isExisting():
                szText = (
                    text("TXT_KEY_BUILDING_LEANING_TOWER_EFFECT")
                    + " "
                    + gc.getUnitInfo(iUnit).getDescription()
                )
                message(
                    human(),
                    szText,
                    event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                    color=MessageData.LIGHT_BLUE,
                )
        # Absinthe: Leaning Tower end

        # Absinthe: Bibliotheca Corviniana start
        if iBuildingType == Wonder.BIBLIOTHECA_CORVINIANA:
            # techs known by the owner civ
            iTeam = pPlayer.getTeam()
            pTeam = gc.getTeam(iTeam)
            lBuilderKnownTechs = []
            for iTech in xrange(gc.getNumTechInfos()):  # type: ignore
                if pTeam.isHasTech(iTech):
                    lBuilderKnownTechs.append(iTech)

            # techs known by the other civs
            lOthersKnownTechs = []
            for iLoopPlayer in civilizations().majors().ids():
                pLoopPlayer = gc.getPlayer(iLoopPlayer)
                iLoopTeam = pLoopPlayer.getTeam()
                pLoopTeam = gc.getTeam(iLoopTeam)
                # only for known civs
                if iLoopPlayer != iPlayer and pTeam.isHasMet(iLoopTeam):
                    for iTech in xrange(gc.getNumTechInfos()):  # type: ignore
                        if pLoopTeam.isHasTech(iTech):
                            lOthersKnownTechs.append(iTech)

            # collecting the not known techs which are available for at least one other civ
            # note that we can have the same tech multiple times
            lPotentialTechs = []
            for iTech in lOthersKnownTechs:
                if iTech not in lBuilderKnownTechs:
                    lPotentialTechs.append(iTech)

            if len(lPotentialTechs) > 0:
                # converting to a set (and then back to a list), as sets only keep unique elements
                lUniquePotentialTechs = list(set(lPotentialTechs))

                # randomizing the order of the techs
                random.shuffle(lPotentialTechs)

                # adding the techs, with message for the human player
                if len(lUniquePotentialTechs) == 1:
                    # add the first instance of the single tech, with message for the human player
                    iChosenTech = lPotentialTechs[0]
                    pTeam.setHasTech(iChosenTech, True, iPlayer, False, True)
                    if iPlayer == human():
                        sText = text(
                            "TXT_KEY_BUILDING_BIBLIOTHECA_CORVINIANA_EFFECT",
                            gc.getTechInfo(iChosenTech).getDescription(),
                        )
                        message(iPlayer, sText, force=True, color=MessageData.LIGHT_BLUE)
                elif len(lUniquePotentialTechs) > 1:
                    # add two different random techs, with message for the human player
                    for tech in random.sample(lPotentialTechs, 2):
                        pTeam.setHasTech(tech, True, iPlayer, False, True)
                        if iPlayer == human():
                            sText = text(
                                "TXT_KEY_BUILDING_BIBLIOTHECA_CORVINIANA_EFFECT",
                                gc.getTechInfo(tech).getDescription(),
                            )
                            message(iPlayer, sText, force=True, color=MessageData.LIGHT_BLUE)
        # Absinthe: Bibliotheca Corviniana end

        # Absinthe: Kalmar Castle start
        if iBuildingType == Wonder.KALMAR_CASTLE:
            for neighbour in civilization(iPlayer).location.neighbours:
                iNeighbour = neighbour
                pNeighbour = gc.getPlayer(iNeighbour)
                if pNeighbour.isAlive() and iPlayer != iNeighbour:
                    pPlayer.AI_changeAttitudeExtra(iNeighbour, 3)
                    pNeighbour.AI_changeAttitudeExtra(iPlayer, 3)
        # Absinthe: Kalmar Castle end

        # Absinthe: Grand Arsenal start
        if iBuildingType == Wonder.GRAND_ARSENAL:
            iX = pCity.getX()
            iY = pCity.getY()
            for i in range(3):
                # should we have Galleass for all civs, or use the getUniqueUnit function in RFCUtils?
                pNewUnit = pPlayer.initUnit(
                    Unit.VENICE_GALLEAS,
                    iX,
                    iY,
                    UnitAITypes(gc.getUnitInfo(Unit.VENICE_GALLEAS).getDefaultUnitAIType()),
                    DirectionTypes.DIRECTION_SOUTH,
                )
                pNewUnit.setExperience(6, -1)
                for iPromo in [
                    Promotion.COMBAT,
                    Promotion.LEADERSHIP,
                    Promotion.NAVIGATION,
                ]:
                    pNewUnit.setHasPromotion(iPromo, True)
        # Absinthe: Grand Arsenal end

        # Absinthe: Magellan's Voyage start
        if iBuildingType == Wonder.MAGELLANS_VOYAGE:
            iTeam = pPlayer.getTeam()
            pTeam = gc.getTeam(iTeam)
            pTeam.changeExtraMoves(gc.getInfoTypeForString("DOMAIN_SEA"), 2)
        # Absinthe: Magellan's Voyage end

        # Absinthe: St. Catherine's Monastery start
        if iBuildingType == Wonder.ST_CATHERINE_MONASTERY:
            iX = pCity.getX()
            iY = pCity.getY()
            for i in range(2):
                pPlayer.initUnit(
                    Unit.HOLY_RELIC,
                    iX,
                    iY,
                    UnitAITypes.NO_UNITAI,
                    DirectionTypes.DIRECTION_SOUTH,
                )
            if human() == iPlayer:
                message(
                    iPlayer,
                    text("TXT_KEY_BUILDING_SAINT_CATHERINE_MONASTERY_EFFECT"),
                    color=MessageData.LIGHT_BLUE,
                )
        # Absinthe: St. Catherine's Monastery end

        # Absinthe: Al-Azhar University start
        if iBuildingType == Wonder.ALAZHAR:
            iTeam = pPlayer.getTeam()
            pTeam = gc.getTeam(iTeam)
            for iTech in xrange(gc.getNumTechInfos()):  # type: ignore
                if not pTeam.isHasTech(iTech):
                    if gc.getTechInfo(iTech).getAdvisorType() == gc.getInfoTypeForString(
                        "ADVISOR_RELIGION"
                    ):
                        research_cost = pTeam.getResearchCost(iTech)
                        pTeam.changeResearchProgress(
                            iTech,
                            min(
                                research_cost - pTeam.getResearchProgress(iTech), research_cost / 2
                            ),
                            iPlayer,
                        )
        # Absinthe: Al-Azhar University end

        # Absinthe: Sistine Chapel start
        if iBuildingType == Wonder.SISTINE_CHAPEL:
            for city in cities().owner(iPlayer).entities():
                if city.getNumWorldWonders() > 0:
                    city.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_ARTIST"), 1)
        elif isWorldWonderClass(gc.getBuildingInfo(iBuildingType).getBuildingClassType()):
            # if the given civ already had the Sistine Chapel, and built another wonder in a new city
            if pPlayer.countNumBuildings(Wonder.SISTINE_CHAPEL) > 0:
                if pCity.getNumWorldWonders() == 1:
                    pCity.changeFreeSpecialistCount(
                        gc.getInfoTypeForString("SPECIALIST_ARTIST"), 1
                    )
        # Absinthe: Sistine Chapel end

        # Absinthe: Jasna Gora start
        if iBuildingType == Wonder.JASNA_GORA:
            for city in cities().owner(iPlayer).entities():
                city.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_CATHOLIC_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    1,
                )
                city.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_ORTHODOX_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    1,
                )
                city.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_PROTESTANT_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    1,
                )
                city.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_ISLAMIC_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    1,
                )
        # Absinthe: Jasna Gora end

        # Absinthe: Kizil Kule start
        if iBuildingType == Wonder.KIZIL_KULE:
            for city in cities().owner(iPlayer).entities():
                city.setBuildingYieldChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_HARBOR"), YieldTypes.YIELD_COMMERCE, 2
                )
        # Absinthe: Kizil Kule end

        # Absinthe: Samogitian Alkas start
        if iBuildingType == Wonder.SAMOGITIAN_ALKAS:
            for city in cities().owner(iPlayer).entities():
                city.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_PAGAN_SHRINE"),
                    CommerceTypes.COMMERCE_RESEARCH,
                    2,
                )
        # Absinthe: Samogitian Alkas end

        # Absinthe: Magna Carta start
        if iBuildingType == Wonder.MAGNA_CARTA:
            for city in cities().owner(iPlayer).entities():
                city.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_COURTHOUSE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    2,
                )
        # Absinthe: Magna Carta end

        game = gc.getGame()
        if (
            (not game.isNetworkMultiPlayer())
            and (iPlayer == game.getActivePlayer())
            and isWorldWonderClass(gc.getBuildingInfo(iBuildingType).getBuildingClassType())
        ):
            popupInfo = CyPopupInfo()
            popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
            popupInfo.setData1(iBuildingType)
            popupInfo.setData2(pCity.getID())
            popupInfo.setData3(0)
            popupInfo.setText(u"showWonderMovie")
            popupInfo.addPopup(iPlayer)
            ## Platy Builder ##
            if not CyGame().GetWorldBuilderMode():
                ## Platy Builder ##
                popupInfo = CyPopupInfo()
                popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
                popupInfo.setData1(iBuildingType)
                popupInfo.setData2(pCity.getID())
                popupInfo.setData3(0)
                popupInfo.setText(u"showWonderMovie")
                popupInfo.addPopup(pCity.getOwner())

        CvAdvisorUtils.buildingBuiltFeats(pCity, iBuildingType)

        if not self.__LOG_BUILDING:
            return
        CvUtil.pyPrint(
            "%s was finished by Player %d Civilization %s"
            % (
                PyInfo.BuildingInfo(iBuildingType).getDescription(),
                iPlayer,
                pPlayer.getCivilizationDescription(0),
            )
        )

    def onProjectBuilt(self, argsList):
        "Project Completed"
        pCity, iProjectType = argsList
        iPlayer = pCity.getOwner()
        game = gc.getGame()
        if (not game.isNetworkMultiPlayer()) and (iPlayer == game.getActivePlayer()):
            popupInfo = CyPopupInfo()
            popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
            popupInfo.setData1(iProjectType)
            popupInfo.setData2(pCity.getID())
            popupInfo.setData3(2)
            popupInfo.setText(u"showWonderMovie")
            popupInfo.addPopup(iPlayer)

            ## Platy Builder ##
            if not CyGame().GetWorldBuilderMode():
                ## Platy Builder ##
                popupInfo = CyPopupInfo()
                popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
                popupInfo.setData1(iProjectType)
                popupInfo.setData2(pCity.getID())
                popupInfo.setData3(2)
                popupInfo.setText(u"showWonderMovie")
                popupInfo.addPopup(iPlayer)

        # Absinthe: Torre del Oro start
        if iProjectType >= len(Project):
            pPlayer = gc.getPlayer(iPlayer)
            if pPlayer.countNumBuildings(Wonder.TORRE_DEL_ORO) > 0:
                # 70% chance for a 3 turn Golden Age
                if percentage_chance(70, strict=True):
                    pPlayer.changeGoldenAgeTurns(3)
                    if human() == iPlayer:
                        message(
                            iPlayer,
                            text("TXT_KEY_PROJECT_COLONY_GOLDEN_AGE"),
                            color=MessageData.GREEN,
                        )
                # Absinthe: Torre del Oro end
                popupInfo.addPopup(pCity.getOwner())

    def onSelectionGroupPushMission(self, argsList):
        "selection group mission"
        eOwner = argsList[0]
        eMission = argsList[1]
        iNumUnits = argsList[2]
        listUnitIds = argsList[3]

        if not self.__LOG_PUSH_MISSION:
            return
        if pHeadUnit:  # type: ignore
            CvUtil.pyPrint("Selection Group pushed mission %d" % (eMission))

    def onUnitMove(self, argsList):
        "unit move"
        pPlot, pUnit, pOldPlot = argsList
        player = PyPlayer(pUnit.getOwner())
        unitInfo = PyInfo.UnitInfo(pUnit.getUnitType())
        if not self.__LOG_MOVEMENT:
            return
        if player and unitInfo:
            CvUtil.pyPrint(
                "Player %d Civilization %s unit %s is moving to %d, %d"
                % (
                    player.getID(),
                    player.getCivilizationName(),
                    unitInfo.getDescription(),
                    pUnit.getX(),
                    pUnit.getY(),
                )
            )

    def onUnitSetXY(self, argsList):
        "units xy coords set manually"
        pPlot, pUnit = argsList
        player = PyPlayer(pUnit.getOwner())
        unitInfo = PyInfo.UnitInfo(pUnit.getUnitType())
        if not self.__LOG_MOVEMENT:
            return

    def onUnitCreated(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Unit Completed"
        unit = argsList[0]
        player = PyPlayer(unit.getOwner())
        if not self.__LOG_UNITBUILD:
            return

    def onUnitBuilt(self, argsList):
        "Unit Completed"
        city = argsList[0]
        unit = argsList[1]
        player = PyPlayer(city.getOwner())

        # Absinthe: Topkapi Palace start
        iPlayer = unit.getOwner()
        pPlayer = gc.getPlayer(iPlayer)
        iUnitType = unit.getUnitType()
        iTeam = pPlayer.getTeam()
        pTeam = gc.getTeam(iTeam)

        if pTeam.isTrainVassalUU():
            l_vassalUU = []
            iDefaultUnit = getBaseUnit(iUnitType)
            for iLoopPlayer in civilizations().majors().ids():
                pLoopPlayer = gc.getPlayer(iLoopPlayer)
                if pLoopPlayer.isAlive():
                    if gc.getTeam(pLoopPlayer.getTeam()).isVassal(iTeam):
                        iUniqueUnit = getUniqueUnit(iLoopPlayer, iUnitType)
                        if iUniqueUnit != iDefaultUnit:
                            l_vassalUU.append(iUniqueUnit)
            if l_vassalUU:  # Only convert if vassal UU is possible
                iPlayerUU = getUniqueUnit(iPlayer, iUnitType)
                if iPlayerUU != iDefaultUnit:
                    # double chance for the original UU
                    l_vassalUU.append(iPlayerUU)
                    l_vassalUU.append(iPlayerUU)
                iUnit = choice(l_vassalUU)
                pNewUnit = pPlayer.initUnit(
                    iUnit,
                    unit.getX(),
                    unit.getY(),
                    UnitAITypes.NO_UNITAI,
                    DirectionTypes.NO_DIRECTION,
                )
                pNewUnit.convert(unit)
                # message if it was changed to a vassal UU
                if iUnit != iPlayerUU and iUnit != iDefaultUnit:
                    if human() == iPlayer:
                        szText = text(
                            "TXT_KEY_BUILDING_TOPKAPI_PALACE_EFFECT",
                            gc.getUnitInfo(iUnit).getDescription(),
                            gc.getUnitInfo(iPlayerUU).getDescription(),
                        )
                        message(
                            human(),
                            szText,
                            event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                            button=gc.getUnitInfo(iUnit).getButton(),
                            color=MessageData.LIGHT_BLUE,
                            location=city,
                        )
        # Absinthe: Topkapi Palace end

        # Absinthe: Brandenburg Gate start
        if unit.getUnitCombatType() != -1:
            if pPlayer.countNumBuildings(Wonder.BRANDENBURG_GATE) > 0:
                unit.changeExperience(
                    (
                        2
                        * city.getAddedFreeSpecialistCount(
                            gc.getInfoTypeForString("SPECIALIST_GREAT_GENERAL")
                        )
                    ),
                    999,
                    False,
                    False,
                    False,
                )
        # Absinthe: Brandenburg Gate end

        # Absinthe: Selimiye Mosque start
        if pPlayer.countNumBuildings(Wonder.SELIMIYE_MOSQUE) > 0:
            if pPlayer.isGoldenAge():
                unit.changeExperience(unit.getExperience(), 999, False, False, False)
        # Absinthe: Selimiye Mosque end

        CvAdvisorUtils.unitBuiltFeats(city, unit)

        if not self.__LOG_UNITBUILD:
            return
        CvUtil.pyPrint(
            "%s was finished by Player %d Civilization %s"
            % (
                PyInfo.UnitInfo(unit.getUnitType()).getDescription(),
                player.getID(),
                player.getCivilizationName(),
            )
        )

    def onUnitKilled(self, argsList):
        "Unit Killed"
        unit, iAttacker = argsList
        player = PyPlayer(unit.getOwner())
        attacker = PyPlayer(iAttacker)
        if not self.__LOG_UNITKILLED:
            return
        CvUtil.pyPrint(
            "Player %d Civilization %s Unit %s was killed by Player %d"
            % (
                player.getID(),
                player.getCivilizationName(),
                PyInfo.UnitInfo(unit.getUnitType()).getDescription(),
                attacker.getID(),
            )
        )

    def onUnitLost(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Unit Lost"
        unit = argsList[0]
        player = PyPlayer(unit.getOwner())
        if not self.__LOG_UNITLOST:
            return
        CvUtil.pyPrint(
            "%s was lost by Player %d Civilization %s"
            % (
                PyInfo.UnitInfo(unit.getUnitType()).getDescription(),
                player.getID(),
                player.getCivilizationName(),
            )
        )

    def onUnitPromoted(self, argsList):
        "Unit Promoted"
        pUnit, iPromotion = argsList
        player = PyPlayer(pUnit.getOwner())
        if not self.__LOG_UNITPROMOTED:
            return
        CvUtil.pyPrint(
            "Unit Promotion Event: %s - %s" % (player.getCivilizationName(), pUnit.getName())
        )

    def onUnitSelected(self, argsList):
        "Unit Selected"
        unit = argsList[0]
        player = PyPlayer(unit.getOwner())
        if not self.__LOG_UNITSELECTED:
            return
        CvUtil.pyPrint(
            "%s was selected by Player %d Civilization %s"
            % (
                PyInfo.UnitInfo(unit.getUnitType()).getDescription(),
                player.getID(),
                player.getCivilizationName(),
            )
        )

    def onUnitRename(self, argsList):
        "Unit is renamed"
        pUnit = argsList[0]
        if pUnit.getOwner() == gc.getGame().getActivePlayer():
            self.__eventEditUnitNameBegin(pUnit)

    def onUnitPillage(self, argsList):
        "Unit pillages a plot"
        pUnit, iImprovement, iRoute, iOwner = argsList
        iPlotX = pUnit.getX()
        iPlotY = pUnit.getY()
        pPlot = CyMap().plot(iPlotX, iPlotY)

        if not self.__LOG_UNITPILLAGE:
            return
        CvUtil.pyPrint(
            "Player %d's %s pillaged improvement %d and route %d at plot at (%d, %d)"
            % (
                iOwner,
                PyInfo.UnitInfo(pUnit.getUnitType()).getDescription(),
                iImprovement,
                iRoute,
                iPlotX,
                iPlotY,
            )
        )

    def onUnitSpreadReligionAttempt(self, argsList):
        "Unit tries to spread religion to a city"
        pUnit, iReligion, bSuccess = argsList

        iX = pUnit.getX()
        iY = pUnit.getY()
        pPlot = CyMap().plot(iX, iY)
        pCity = pPlot.getPlotCity()

    def onUnitGifted(self, argsList):
        "Unit is gifted from one player to another"
        pUnit, iGiftingPlayer, pPlotLocation = argsList

    def onUnitBuildImprovement(self, argsList):
        "Unit begins enacting a Build (building an Improvement or Route)"
        pUnit, iBuild, bFinished = argsList

    def onGoodyReceived(self, argsList):
        "Goody received"
        iPlayer, pPlot, pUnit, iGoodyType = argsList
        if not self.__LOG_GOODYRECEIVED:
            return
        CvUtil.pyPrint(
            "%s received a goody" % (gc.getPlayer(iPlayer).getCivilizationDescription(0))
        )

    def onGreatPersonBorn(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Unit Promoted"
        pUnit, iPlayer, pCity = argsList
        player = PyPlayer(iPlayer)
        pPlayer = gc.getPlayer(iPlayer)
        if pUnit.isNone() or pCity.isNone():
            return
        if not self.__LOG_GREATPERSON:
            # Absinthe: Louvre start
            if pPlayer.countNumBuildings(Wonder.LOUVRE) > 0:
                for loopCity in cities().owner(iPlayer).entities():
                    # bigger boost for the GP city and the Louvre city
                    if loopCity.getNumActiveBuilding(Wonder.LOUVRE) or pCity == loopCity:
                        loopCity.changeCulture(
                            iPlayer, min(300, loopCity.getCultureThreshold() / 5), True
                        )
                    else:
                        loopCity.changeCulture(
                            iPlayer, min(100, loopCity.getCultureThreshold() / 10), True
                        )
            # Absinthe: Louvre end

            # Absinthe: Peterhof Palace start
            if pPlayer.countNumBuildings(Wonder.PETERHOF_PALACE) > 0:
                if percentage_chance(70, strict=True):
                    if pUnit.getUnitType() == Unit.GREAT_SCIENTIST:
                        pCity.changeFreeSpecialistCount(
                            gc.getInfoTypeForString("SPECIALIST_SCIENTIST"), 1
                        )
                    elif pUnit.getUnitType() == Unit.GREAT_PROPHET:
                        pCity.changeFreeSpecialistCount(
                            gc.getInfoTypeForString("SPECIALIST_PRIEST"), 1
                        )
                    elif pUnit.getUnitType() == Unit.GREAT_ARTIST:
                        pCity.changeFreeSpecialistCount(
                            gc.getInfoTypeForString("SPECIALIST_ARTIST"), 1
                        )
                    elif pUnit.getUnitType() == Unit.GREAT_MERCHANT:
                        pCity.changeFreeSpecialistCount(
                            gc.getInfoTypeForString("SPECIALIST_MERCHANT"), 1
                        )
                    elif pUnit.getUnitType() == Unit.GREAT_ENGINEER:
                        pCity.changeFreeSpecialistCount(
                            gc.getInfoTypeForString("SPECIALIST_ENGINEER"), 1
                        )
                    elif pUnit.getUnitType() == Unit.GREAT_SPY:
                        pCity.changeFreeSpecialistCount(
                            gc.getInfoTypeForString("SPECIALIST_SPY"), 1
                        )
            # Absinthe: Peterhof Palace start
            return
        CvUtil.pyPrint(
            "A %s was born for %s in %s"
            % (pUnit.getName(), player.getCivilizationName(), pCity.getName())
        )

    def onTechAcquired(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Tech Acquired"
        iTechType, iTeam, iPlayer, bAnnounce = argsList
        # Note that iPlayer may be NULL (-1) and not a refer to a player object

        # Show tech splash when applicable
        if iPlayer > -1 and bAnnounce and not CyInterface().noTechSplash():
            if gc.getGame().isFinalInitialized() and not gc.getGame().GetWorldBuilderMode():
                if (not gc.getGame().isNetworkMultiPlayer()) and (
                    iPlayer == gc.getGame().getActivePlayer()
                ):
                    popupInfo = CyPopupInfo()
                    popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
                    popupInfo.setData1(iTechType)
                    popupInfo.setText(u"showTechSplash")
                    popupInfo.addPopup(iPlayer)

        if not self.__LOG_TECH:
            return
        CvUtil.pyPrint(
            "%s was finished by Team %d"
            % (PyInfo.TechnologyInfo(iTechType).getDescription(), iTeam)
        )

    def onTechSelected(self, argsList):
        "Tech Selected"
        iTechType, iPlayer = argsList
        if not self.__LOG_TECH:
            return
        CvUtil.pyPrint(
            "%s was selected by Player %d"
            % (PyInfo.TechnologyInfo(iTechType).getDescription(), iPlayer)
        )

    def onReligionFounded(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Religion Founded"
        iReligion, iFounder = argsList
        player = PyPlayer(iFounder)

        iCityId = gc.getGame().getHolyCity(iReligion).getID()
        if gc.getGame().isFinalInitialized() and not gc.getGame().GetWorldBuilderMode():
            if (not gc.getGame().isNetworkMultiPlayer()) and (
                iFounder == gc.getGame().getActivePlayer()
            ):
                popupInfo = CyPopupInfo()
                popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
                popupInfo.setData1(iReligion)
                popupInfo.setData2(iCityId)
                popupInfo.setData3(1)
                popupInfo.setText(u"showWonderMovie")
                popupInfo.addPopup(iFounder)

        if not self.__LOG_RELIGION:
            return
        CvUtil.pyPrint(
            "Player %d Civilization %s has founded %s"
            % (
                iFounder,
                player.getCivilizationName(),
                gc.getReligionInfo(iReligion).getDescription(),
            )
        )

    def onReligionSpread(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Religion Has Spread to a City"
        iReligion, iOwner, pSpreadCity = argsList
        player = PyPlayer(iOwner)
        if not self.__LOG_RELIGIONSPREAD:
            return
        CvUtil.pyPrint(
            "%s has spread to Player %d Civilization %s city of %s"
            % (
                gc.getReligionInfo(iReligion).getDescription(),
                iOwner,
                player.getCivilizationName(),
                pSpreadCity.getName(),
            )
        )

    def onReligionRemove(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Religion Has been removed from a City"
        iReligion, iOwner, pRemoveCity = argsList
        player = PyPlayer(iOwner)
        if not self.__LOG_RELIGIONSPREAD:
            return
        CvUtil.pyPrint(
            "%s has been removed from Player %d Civilization %s city of %s"
            % (
                gc.getReligionInfo(iReligion).getDescription(),
                iOwner,
                player.getCivilizationName(),
                pRemoveCity.getName(),
            )
        )

    def onCorporationFounded(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Corporation Founded"
        iCorporation, iFounder = argsList
        player = PyPlayer(iFounder)

        if not self.__LOG_RELIGION:
            return
        CvUtil.pyPrint(
            "Player %d Civilization %s has founded %s"
            % (
                iFounder,
                player.getCivilizationName(),
                gc.getCorporationInfo(iCorporation).getDescription(),
            )
        )

    def onCorporationSpread(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Corporation Has Spread to a City"
        iCorporation, iOwner, pSpreadCity = argsList
        player = PyPlayer(iOwner)
        if not self.__LOG_RELIGIONSPREAD:
            return
        CvUtil.pyPrint(
            "%s has spread to Player %d Civilization %s city of %s"
            % (
                gc.getCorporationInfo(iCorporation).getDescription(),
                iOwner,
                player.getCivilizationName(),
                pSpreadCity.getName(),
            )
        )

    def onCorporationRemove(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Corporation Has been removed from a City"
        iCorporation, iOwner, pRemoveCity = argsList
        player = PyPlayer(iOwner)
        if not self.__LOG_RELIGIONSPREAD:
            return
        CvUtil.pyPrint(
            "%s has been removed from Player %d Civilization %s city of %s"
            % (
                gc.getReligionInfo(iReligion).getDescription(),  # type: ignore
                iOwner,
                player.getCivilizationName(),
                pRemoveCity.getName(),
            )
        )

    def onGoldenAge(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Golden Age"
        iPlayer = argsList[0]
        player = PyPlayer(iPlayer)
        if not self.__LOG_GOLDENAGE:
            return
        CvUtil.pyPrint(
            "Player %d Civilization %s has begun a golden age"
            % (iPlayer, player.getCivilizationName())
        )

    def onEndGoldenAge(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "End Golden Age"
        iPlayer = argsList[0]
        player = PyPlayer(iPlayer)
        if not self.__LOG_ENDGOLDENAGE:
            return
        CvUtil.pyPrint(
            "Player %d Civilization %s golden age has ended"
            % (iPlayer, player.getCivilizationName())
        )

    # Absinthe: currently unused
    def onChangeWar(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "War Status Changes"
        bIsWar = argsList[0]
        iTeam = argsList[1]
        iRivalTeam = argsList[2]
        if not self.__LOG_WARPEACE:
            return
        if bIsWar:
            strStatus = "declared war"
        else:
            strStatus = "declared peace"
        CvUtil.pyPrint("Team %d has %s on Team %d" % (iTeam, strStatus, iRivalTeam))

    def onChat(self, argsList):
        "Chat Message Event"
        chatMessage = "%s" % (argsList[0],)

    def onSetPlayerAlive(self, argsList):
        "Set Player Alive Event"
        iPlayerID = argsList[0]
        bNewValue = argsList[1]
        CvUtil.pyPrint("Player %d's alive status set to: %d" % (iPlayerID, int(bNewValue)))

    # Absinthe: Python Event for civic changes
    def onPlayerChangeAllCivics(self, argsList):
        # note that this only reports civic change if it happened via normal revolution
        "Player changes his civics"
        iPlayer = argsList[0]
        lNewCivics = [argsList[1], argsList[2], argsList[3], argsList[4], argsList[5], argsList[6]]
        lOldCivics = [
            argsList[7],
            argsList[8],
            argsList[9],
            argsList[10],
            argsList[11],
            argsList[12],
        ]

    def onPlayerChangeSingleCivic(self, argsList):
        # note that this reports all civic changes in single instances (so also reports force converts by diplomacy or with spies)
        "Civics are changed for a player"
        iPlayer, iNewCivic, iOldCivic = argsList

    # Absinthe: end

    def onPlayerChangeStateReligion(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "Player changes his state religion"
        iPlayer, iNewReligion, iOldReligion = argsList

    def onPlayerGoldTrade(self, argsList):
        "Player Trades gold to another player"
        iFromPlayer, iToPlayer, iGoldAmount = argsList

    def onCityBuilt(self, argsList):
        "City Built"
        city = argsList[0]
        iPlayer = city.getOwner()
        pPlayer = gc.getPlayer(iPlayer)

        # Absinthe: city naming popup on city foundation - settable in GlobalDefines_Alt.xml
        bCityNamePopup = gc.getDefineINT("CITY_NAME_POPUP") == 1
        if bCityNamePopup:
            if iPlayer == gc.getGame().getActivePlayer():
                self.__eventEditCityNameBegin(city, False)
        # Absinthe: end

        # Absinthe: Jasna Gora start
        if pPlayer.countNumBuildings(Wonder.JASNA_GORA) > 0:
            city.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_CATHOLIC_TEMPLE"),
                CommerceTypes.COMMERCE_CULTURE,
                1,
            )
            city.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_ORTHODOX_TEMPLE"),
                CommerceTypes.COMMERCE_CULTURE,
                1,
            )
            city.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_PROTESTANT_TEMPLE"),
                CommerceTypes.COMMERCE_CULTURE,
                1,
            )
            city.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_ISLAMIC_TEMPLE"),
                CommerceTypes.COMMERCE_CULTURE,
                1,
            )
        # Absinthe: Jasna Gora end

        # Absinthe: Kizil Kule start
        if pPlayer.countNumBuildings(Wonder.KIZIL_KULE) > 0:
            city.setBuildingYieldChange(
                gc.getInfoTypeForString("BUILDINGCLASS_HARBOR"), YieldTypes.YIELD_COMMERCE, 2
            )
        # Absinthe: Kizil Kule end

        # Absinthe: Samogitian Alkas start
        if pPlayer.countNumBuildings(Wonder.SAMOGITIAN_ALKAS) > 0:
            city.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_PAGAN_SHRINE"),
                CommerceTypes.COMMERCE_RESEARCH,
                2,
            )
        # Absinthe: Samogitian Alkas end

        # Absinthe: Magna Carta start
        if pPlayer.countNumBuildings(Wonder.MAGNA_CARTA) > 0:
            city.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_COURTHOUSE"),
                CommerceTypes.COMMERCE_CULTURE,
                2,
            )
        # Absinthe: Magna Carta end

        CvUtil.pyPrint("City Built Event: %s" % (city.getName()))

    def onCityRazed(self, argsList):
        "City Razed"
        city, iPlayer = argsList

        # Rhye - start bugfix
        owner = PyPlayer(city.getOwner())
        if city.getOwner() == iPlayer:
            if city.getPreviousOwner() != -1:
                owner = PyPlayer(city.getPreviousOwner())
        # Rhye - end bugfix

        CvUtil.pyPrint("City Razed Event: %s" % (city.getName(),))
        razor = PyPlayer(iPlayer)
        CvUtil.pyPrint(
            "Player %d Civilization %s City %s was razed by Player %d Civilization %s"
            % (
                owner.getID(),
                owner.getCivilizationName(),
                city.getName(),
                razor.getID(),
                razor.getCivilizationName(),
            )
        )

        # Absinthe: Al-Azhar University start
        if city.getNumActiveBuilding(Wonder.ALAZHAR):
            pPlayer = gc.getPlayer(iPlayer)
            iTeam = pPlayer.getTeam()
            pTeam = gc.getTeam(iTeam)
            for iTech in xrange(gc.getNumTechInfos()):  # type: ignore
                if not pTeam.isHasTech(iTech):
                    if gc.getTechInfo(iTech).getAdvisorType() == gc.getInfoTypeForString(
                        "ADVISOR_RELIGION"
                    ):
                        pTeam.changeResearchProgress(
                            iTech,
                            max(
                                -pPreviousTeam.getResearchProgress(iTech),  # type: ignore
                                -pTeam.getResearchCost(iTech) / 5,
                            ),
                            iPlayer,
                        )
        # Absinthe: Al-Azhar University end

        # Absinthe: Sistine Chapel start
        if city.getNumActiveBuilding(Wonder.SISTINE_CHAPEL):
            for loopCity in cities().owner(iPlayer).entities():
                if loopCity.getNumWorldWonders() > 0:
                    loopCity.changeFreeSpecialistCount(
                        gc.getInfoTypeForString("SPECIALIST_ARTIST"), -1
                    )
        # Absinthe: Sistine Chapel end

        # Absinthe: Jasna Gora start
        if city.getNumActiveBuilding(Wonder.JASNA_GORA):
            for loopCity in cities().owner(iPlayer).entities():
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_CATHOLIC_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    0,
                )
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_ORTHODOX_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    0,
                )
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_PROTESTANT_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    0,
                )
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_ISLAMIC_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    0,
                )
        # Absinthe: Jasna Gora end

        # Absinthe: Kizil Kule start
        if city.getNumActiveBuilding(Wonder.KIZIL_KULE):
            for loopCity in cities().owner(iPlayer).entities():
                loopCity.setBuildingYieldChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_HARBOR"), YieldTypes.YIELD_COMMERCE, 0
                )
        # Absinthe: Kizil Kule end

        # Absinthe: Samogitian Alkas start
        if city.getNumActiveBuilding(Wonder.SAMOGITIAN_ALKAS):
            for loopCity in cities().owner(iPlayer).entities():
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_PAGAN_SHRINE"),
                    CommerceTypes.COMMERCE_RESEARCH,
                    0,
                )
        # Absinthe: Samogitian Alkas end

        # Absinthe: Magna Carta start
        if city.getNumActiveBuilding(Wonder.MAGNA_CARTA):
            for loopCity in cities().owner(iPlayer).entities():
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_COURTHOUSE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    0,
                )
        # Absinthe: Magna Carta end

        # Absinthe: wonder destroyed message start
        if city.getNumWorldWonders() > 0:
            ConquerPlayer = gc.getPlayer(city.getOwner())
            ConquerTeam = ConquerPlayer.getTeam()
            if city.getPreviousOwner() != -1:
                PreviousPlayer = gc.getPlayer(city.getPreviousOwner())
                PreviousTeam = PreviousPlayer.getTeam()
            HumanTeam = team()
            if ConquerPlayer.isHuman() or (
                player().isExisting()
                and (HumanTeam.isHasMet(ConquerTeam) or HumanTeam.isHasMet(PreviousTeam))
            ):
                # Absinthe: collect all wonders, including shrines (even though cities with shrines can't be destroyed in the mod)
                lAllWonders = [w for w in Wonder]
                for iWonder in [
                    Building.CATHOLIC_SHRINE,
                    Building.ORTHODOX_SHRINE,
                    Building.ISLAMIC_SHRINE,
                    Building.PROTESTANT_SHRINE,
                ]:
                    lAllWonders.append(iWonder)
                for iWonder in lAllWonders:
                    if city.getNumBuilding(iWonder) > 0:
                        sWonderName = gc.getBuildingInfo(iWonder).getDescription()
                        if ConquerPlayer.isHuman():
                            message(
                                human(),
                                text("TXT_KEY_MISC_WONDER_DESTROYED_1", sWonderName),
                                event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                                button=gc.getBuildingInfo(iWonder).getButton(),
                                color=MessageData.LIGHT_RED,
                                location=city,
                            )
                        elif HumanTeam.isHasMet(ConquerTeam):
                            ConquerName = ConquerPlayer.getCivilizationDescriptionKey()
                            message(
                                human(),
                                text("TXT_KEY_MISC_WONDER_DESTROYED_2", ConquerName, sWonderName),
                                event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                                button=gc.getBuildingInfo(iWonder).getButton(),
                                color=MessageData.LIGHT_RED,
                                location=city,
                            )
                        elif HumanTeam.isHasMet(PreviousTeam):
                            PreviousName = PreviousPlayer.getCivilizationDescriptionKey()
                            message(
                                human(),
                                text("TXT_KEY_MISC_WONDER_DESTROYED_3", PreviousName, sWonderName),
                                event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                                button=gc.getBuildingInfo(iWonder).getButton(),
                                color=MessageData.LIGHT_RED,
                                location=city,
                            )
        # Absinthe: wonder destroyed message end

        # Absinthe: Partisans! - not used currently
        # if city.getPopulation > 1 and iOwner != -1 and iPlayer != -1:
        #     owner = gc.getPlayer(iOwner)
        #     if not owner.isBarbarian() and owner.getNumCities() > 0:
        #         if gc.getTeam(owner.getTeam()).isAtWar(gc.getPlayer(iPlayer).getTeam()):
        #             if gc.getNumEventTriggerInfos() > 0: # prevents mods that don't have events from getting an error
        #                 iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_PARTISANS')
        #                 if iEvent != -1 and gc.getGame().isEventActive(iEvent) and owner.getEventTriggerWeight(iEvent) < 0:
        #                     triggerData = owner.initTriggeredData(iEvent, True, -1, city.getX(), city.getY(), iPlayer, city.getID(), -1, -1, -1, -1)
        # Absinthe: end

    def onCityAcquired(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "City Acquired"
        iPreviousOwner, iNewOwner, pCity, bConquest, bTrade = argsList
        CvUtil.pyPrint("City Acquired Event: %s" % (pCity.getName()))
        pPreviousOwner = gc.getPlayer(iPreviousOwner)
        pNewOwner = gc.getPlayer(iNewOwner)

        # Absinthe: Al-Azhar University start
        if pCity.getNumActiveBuilding(Wonder.ALAZHAR):
            iPreviousTeam = pPreviousOwner.getTeam()
            pPreviousTeam = gc.getTeam(iPreviousTeam)
            iNewTeam = pNewOwner.getTeam()
            pNewTeam = gc.getTeam(iNewTeam)
            for iTech in xrange(gc.getNumTechInfos()):  # type: ignore
                if gc.getTechInfo(iTech).getAdvisorType() == gc.getInfoTypeForString(
                    "ADVISOR_RELIGION"
                ):
                    if not pPreviousTeam.isHasTech(iTech):
                        research_cost = pPreviousTeam.getResearchCost(iTech)
                        pPreviousTeam.changeResearchProgress(
                            iTech,
                            max(-pPreviousTeam.getResearchProgress(iTech), -research_cost / 5),
                            iPreviousOwner,
                        )
                    if not pNewTeam.isHasTech(iTech):
                        research_cost = pNewTeam.getResearchCost(iTech)
                        pNewTeam.changeResearchProgress(
                            iTech,
                            min(
                                research_cost - pNewTeam.getResearchProgress(iTech),
                                research_cost / 5,
                            ),
                            iNewOwner,
                        )
        # Absinthe: Al-Azhar University end

        # Absinthe: Sistine Chapel start
        if pCity.getNumActiveBuilding(Wonder.SISTINE_CHAPEL):
            for loopCity in cities().owner(iPreviousOwner).entities():
                if loopCity.getNumWorldWonders() > 0:
                    loopCity.changeFreeSpecialistCount(
                        gc.getInfoTypeForString("SPECIALIST_ARTIST"), -1
                    )
            for loopCity in cities().owner(iNewOwner).entities():
                if loopCity.getNumWorldWonders() > 0 and not loopCity.getNumActiveBuilding(
                    Wonder.SISTINE_CHAPEL
                ):
                    loopCity.changeFreeSpecialistCount(
                        gc.getInfoTypeForString("SPECIALIST_ARTIST"), 1
                    )
        elif pCity.getNumWorldWonders() > 0:
            if pPreviousOwner.countNumBuildings(Wonder.SISTINE_CHAPEL) > 0:
                pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_ARTIST"), -1)
            elif pNewOwner.countNumBuildings(Wonder.SISTINE_CHAPEL) > 0:
                pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_ARTIST"), 1)
        # Absinthe: Sistine Chapel end

        # Absinthe: Jasna Gora start
        if pCity.getNumActiveBuilding(Wonder.JASNA_GORA):
            for loopCity in cities().owner(iPreviousOwner).entities():
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_CATHOLIC_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    0,
                )
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_ORTHODOX_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    0,
                )
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_PROTESTANT_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    0,
                )
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_ISLAMIC_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    0,
                )
            for loopCity in cities().owner(iNewOwner).entities():
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_CATHOLIC_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    1,
                )
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_ORTHODOX_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    1,
                )
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_PROTESTANT_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    1,
                )
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_ISLAMIC_TEMPLE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    1,
                )
        elif pPreviousOwner.countNumBuildings(Wonder.JASNA_GORA) > 0:
            pCity.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_CATHOLIC_TEMPLE"),
                CommerceTypes.COMMERCE_CULTURE,
                0,
            )
            pCity.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_ORTHODOX_TEMPLE"),
                CommerceTypes.COMMERCE_CULTURE,
                0,
            )
            pCity.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_PROTESTANT_TEMPLE"),
                CommerceTypes.COMMERCE_CULTURE,
                0,
            )
            pCity.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_ISLAMIC_TEMPLE"),
                CommerceTypes.COMMERCE_CULTURE,
                0,
            )
        elif pNewOwner.countNumBuildings(Wonder.JASNA_GORA) > 0:
            pCity.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_CATHOLIC_TEMPLE"),
                CommerceTypes.COMMERCE_CULTURE,
                1,
            )
            pCity.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_ORTHODOX_TEMPLE"),
                CommerceTypes.COMMERCE_CULTURE,
                1,
            )
            pCity.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_PROTESTANT_TEMPLE"),
                CommerceTypes.COMMERCE_CULTURE,
                1,
            )
            pCity.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_ISLAMIC_TEMPLE"),
                CommerceTypes.COMMERCE_CULTURE,
                1,
            )
        # Absinthe: Jasna Gora end

        # Absinthe: Kizil Kule start
        if pCity.getNumActiveBuilding(Wonder.KIZIL_KULE):
            for loopCity in cities().owner(iPreviousOwner).entities():
                loopCity.setBuildingYieldChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_HARBOR"), YieldTypes.YIELD_COMMERCE, 0
                )
            for loopCity in cities().owner(iNewOwner).entities():
                loopCity.setBuildingYieldChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_HARBOR"), YieldTypes.YIELD_COMMERCE, 2
                )
        elif pPreviousOwner.countNumBuildings(Wonder.KIZIL_KULE) > 0:
            pCity.setBuildingYieldChange(
                gc.getInfoTypeForString("BUILDINGCLASS_HARBOR"), YieldTypes.YIELD_COMMERCE, 0
            )
        elif pNewOwner.countNumBuildings(Wonder.KIZIL_KULE) > 0:
            pCity.setBuildingYieldChange(
                gc.getInfoTypeForString("BUILDINGCLASS_HARBOR"), YieldTypes.YIELD_COMMERCE, 2
            )
        # Absinthe: Kizil Kule end

        # Absinthe: Samogitian Alkas start
        if pCity.getNumActiveBuilding(Wonder.SAMOGITIAN_ALKAS):
            for loopCity in cities().owner(iPreviousOwner).entities():
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_PAGAN_SHRINE"),
                    CommerceTypes.COMMERCE_RESEARCH,
                    0,
                )
            for loopCity in cities().owner(iNewOwner).entities():
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_PAGAN_SHRINE"),
                    CommerceTypes.COMMERCE_RESEARCH,
                    2,
                )
        elif pPreviousOwner.countNumBuildings(Wonder.SAMOGITIAN_ALKAS) > 0:
            pCity.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_PAGAN_SHRINE"),
                CommerceTypes.COMMERCE_RESEARCH,
                0,
            )
        elif pNewOwner.countNumBuildings(Wonder.SAMOGITIAN_ALKAS) > 0:
            pCity.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_PAGAN_SHRINE"),
                CommerceTypes.COMMERCE_RESEARCH,
                2,
            )
        # Absinthe: Samogitian Alkas end

        # Absinthe: Magna Carta start
        if pCity.getNumActiveBuilding(Wonder.MAGNA_CARTA):
            for loopCity in cities().owner(iPreviousOwner).entities():
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_COURTHOUSE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    0,
                )
            for loopCity in cities().owner(iNewOwner).entities():
                loopCity.setBuildingCommerceChange(
                    gc.getInfoTypeForString("BUILDINGCLASS_COURTHOUSE"),
                    CommerceTypes.COMMERCE_CULTURE,
                    2,
                )
        elif pPreviousOwner.countNumBuildings(Wonder.MAGNA_CARTA) > 0:
            pCity.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_COURTHOUSE"),
                CommerceTypes.COMMERCE_CULTURE,
                0,
            )
        elif pNewOwner.countNumBuildings(Wonder.MAGNA_CARTA) > 0:
            pCity.setBuildingCommerceChange(
                gc.getInfoTypeForString("BUILDINGCLASS_COURTHOUSE"),
                CommerceTypes.COMMERCE_CULTURE,
                2,
            )
        # Absinthe: Magna Carta end

    def onCityAcquiredAndKept(self, argsList):
        "City Acquired and Kept"
        iOwner, pCity = argsList

        # Absinthe: wonder captured message start
        if pCity.getNumWorldWonders() > 0:
            ConquerPlayer = gc.getPlayer(pCity.getOwner())
            ConquerTeam = ConquerPlayer.getTeam()
            if pCity.getPreviousOwner() != -1:
                PreviousPlayer = gc.getPlayer(pCity.getPreviousOwner())
                PreviousTeam = PreviousPlayer.getTeam()
            HumanTeam = team()
            if ConquerPlayer.isHuman() or (
                player().isExisting()
                and (HumanTeam.isHasMet(ConquerTeam) or HumanTeam.isHasMet(PreviousTeam))
            ):
                # Absinthe: collect all wonders, including shrines
                lAllWonders = [w for w in Wonder] + [
                    Building.CATHOLIC_SHRINE,
                    Building.ORTHODOX_SHRINE,
                    Building.ISLAMIC_SHRINE,
                    Building.PROTESTANT_SHRINE,
                ]
                for iWonder in lAllWonders:
                    if pCity.getNumBuilding(iWonder) > 0:
                        sWonderName = gc.getBuildingInfo(iWonder).getDescription()
                        if ConquerPlayer.isHuman():
                            message(
                                human(),
                                text("TXT_KEY_MISC_WONDER_CAPTURED_1", sWonderName),
                                event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                                button=gc.getBuildingInfo(iWonder).getButton(),
                                color=MessageData.BLUE,
                                location=pCity,
                            )
                        elif HumanTeam.isHasMet(ConquerTeam):
                            ConquerName = ConquerPlayer.getCivilizationDescriptionKey()
                            message(
                                human(),
                                text("TXT_KEY_MISC_WONDER_CAPTURED_2", ConquerName, sWonderName),
                                event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                                button=gc.getBuildingInfo(iWonder).getButton(),
                                color=MessageData.CYAN,
                                location=pCity,
                            )
                        elif HumanTeam.isHasMet(PreviousTeam):
                            PreviousName = PreviousPlayer.getCivilizationDescriptionKey()
                            message(
                                human(),
                                text("TXT_KEY_MISC_WONDER_CAPTURED_3", PreviousName, sWonderName),
                                event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                                button=gc.getBuildingInfo(iWonder).getButton(),
                                color=MessageData.CYAN,
                                location=pCity,
                            )
        # Absinthe: wonder captured message end

        CvUtil.pyPrint("City Acquired and Kept Event: %s" % (pCity.getName()))
        CvUtil.pyPrint(
            "NewOwner: %s, PreviousOwner: %s"
            % (
                PyPlayer(pCity.getOwner()).getCivilizationName(),
                PyPlayer(pCity.getPreviousOwner()).getCivilizationName(),
            )
        )

    def onCityLost(self, argsList):
        "City Lost"
        city = argsList[0]
        player = PyPlayer(city.getOwner())
        if not self.__LOG_CITYLOST:
            return
        CvUtil.pyPrint(
            "City %s was lost by Player %d Civilization %s"
            % (city.getName(), player.getID(), player.getCivilizationName())
        )

    def onCultureExpansion(self, argsList):
        ## Platy Builder ##
        if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython:
            return
        ## Platy Builder ##
        "City Culture Expansion"
        pCity = argsList[0]
        iPlayer = argsList[1]
        CvUtil.pyPrint("City %s's culture has expanded" % (pCity.getName(),))

    def onCityGrowth(self, argsList):
        "City Population Growth"
        pCity = argsList[0]
        iPlayer = argsList[1]
        CvUtil.pyPrint("%s has grown" % (pCity.getName(),))

    def onCityDoTurn(self, argsList):
        "City Production"
        pCity = argsList[0]
        iPlayer = argsList[1]

        CvAdvisorUtils.cityAdvise(pCity, iPlayer)

    def onCityBuildingUnit(self, argsList):
        "City begins building a unit"
        pCity = argsList[0]
        iUnitType = argsList[1]
        if not self.__LOG_CITYBUILDING:
            return
        CvUtil.pyPrint(
            "%s has begun building a %s"
            % (pCity.getName(), gc.getUnitInfo(iUnitType).getDescription())
        )

    def onCityBuildingBuilding(self, argsList):
        "City begins building a Building"
        pCity = argsList[0]
        iBuildingType = argsList[1]
        if not self.__LOG_CITYBUILDING:
            return
        CvUtil.pyPrint(
            "%s has begun building a %s"
            % (pCity.getName(), gc.getBuildingInfo(iBuildingType).getDescription())
        )

    def onCityRename(self, argsList):
        "City is renamed"
        pCity = argsList[0]
        if pCity.getOwner() == gc.getGame().getActivePlayer():
            self.__eventEditCityNameBegin(pCity, True)

    def onCityHurry(self, argsList):
        "City is renamed"
        pCity = argsList[0]
        iHurryType = argsList[1]

    def onVictory(self, argsList):
        "Victory"
        iTeam, iVictory = argsList
        if iVictory >= 0 and iVictory < gc.getNumVictoryInfos():
            victoryInfo = gc.getVictoryInfo(int(iVictory))
            CvUtil.pyPrint(
                "Victory! Team %d achieves a %s victory" % (iTeam, victoryInfo.getDescription())
            )

    def onVassalState(self, argsList):
        "Vassal State"
        iMaster, iVassal, bVassal = argsList

        if bVassal:
            # Absinthe: Imperial Diet start
            MasterTeam = gc.getTeam(iMaster)
            for iPlayer in civilizations().majors().ids():
                pPlayer = gc.getPlayer(iPlayer)
                if (
                    pPlayer.getTeam() == iMaster
                    and pPlayer.countNumBuildings(Wonder.IMPERIAL_DIET) > 0
                ):
                    pPlayer.changeGoldenAgeTurns(3)
                    if human() == iPlayer:
                        message(
                            iPlayer,
                            text("TXT_KEY_BUILDING_IMPERIAL_DIET_EFFECT"),
                            color=MessageData.LIGHT_BLUE,
                        )
            # Absinthe: Imperial Diet end
            CvUtil.pyPrint("Team %d becomes a Vassal State of Team %d" % (iVassal, iMaster))
        else:
            CvUtil.pyPrint(
                "Team %d revolts and is no longer a Vassal State of Team %d" % (iVassal, iMaster)
            )

    def onGameUpdate(self, argsList):
        "sample generic event, called on each game turn slice"
        genericArgs = argsList[0][0]  # tuple of tuple of my args
        turnSlice = genericArgs[0]

    def onMouseEvent(self, argsList):
        "mouse handler - returns 1 if the event was consumed"
        eventType, mx, my, px, py, interfaceConsumed, screens = argsList
        if px != -1 and py != -1:
            if eventType == self.EventLButtonDown:
                if (
                    self.bAllowCheats
                    and self.bCtrl
                    and self.bAlt
                    and CyMap().plot(px, py).isCity()
                    and not interfaceConsumed
                ):
                    # Launch Edit City Event
                    self.beginEvent(CvUtil.EventEditCity, (px, py))
                    return 1

                elif self.bAllowCheats and self.bCtrl and self.bShift and not interfaceConsumed:
                    # Launch Place Object Event
                    self.beginEvent(CvUtil.EventPlaceObject, (px, py))
                    return 1

        if eventType == self.EventBack:
            return CvScreensInterface.handleBack(screens)
        elif eventType == self.EventForward:
            return CvScreensInterface.handleForward(screens)

        return 0

    #################### TRIGGERED EVENTS ##################

    def __eventEditCityNameBegin(self, city, bRename):
        popup = PyPopup.PyPopup(CvUtil.EventEditCityName, EventContextTypes.EVENTCONTEXT_ALL)
        popup.setUserData((city.getID(), bRename))
        popup.setHeaderString(text("TXT_KEY_NAME_CITY"))
        popup.setBodyString(text("TXT_KEY_SETTLE_NEW_CITY_NAME"))
        # Absinthe: if not a rename, it should offer the CNM__eventEditCityBegin name as the default name
        if bRename:
            popup.createEditBox(city.getName())
        else:
            szName = get_data_from_upside_down_map(CITIES_MAP, city.getOwner(), city)
            if szName == "-1":
                popup.createEditBox(city.getName())
            else:
                szName = unicode(szName)
                popup.createEditBox(szName)
        # Absinthe: end
        popup.setEditBoxMaxCharCount(15)
        popup.launch()

    def __eventEditCityNameApply(self, playerID, userData, popupReturn):
        "Edit City Name Event"
        iCityID = userData[0]
        bRename = userData[1]
        player = gc.getPlayer(playerID)
        city = player.getCity(iCityID)
        cityName = popupReturn.getEditBoxString(0)
        if len(cityName) > 30:
            cityName = cityName[:30]
        city.setName(cityName, not bRename)

    def __eventEditCityBegin(self, argsList):
        "Edit City Event"
        px, py = argsList
        CvWBPopups.CvWBPopups().initEditCity(argsList)

    def __eventEditCityApply(self, playerID, userData, popupReturn):
        "Edit City Event Apply"
        if getChtLvl() > 0:
            CvWBPopups.CvWBPopups().applyEditCity((popupReturn, userData))

    def __eventPlaceObjectBegin(self, argsList):
        "Place Object Event"
        CvDebugTools.CvDebugTools().initUnitPicker(argsList)

    def __eventPlaceObjectApply(self, playerID, userData, popupReturn):
        "Place Object Event Apply"
        if getChtLvl() > 0:
            CvDebugTools.CvDebugTools().applyUnitPicker((popupReturn, userData))

    def __eventAwardTechsAndGoldBegin(self, argsList):
        "Award Techs & Gold Event"
        CvDebugTools.CvDebugTools().cheatTechs()

    def __eventAwardTechsAndGoldApply(self, playerID, netUserData, popupReturn):
        "Award Techs & Gold Event Apply"
        if getChtLvl() > 0:
            CvDebugTools.CvDebugTools().applyTechCheat((popupReturn))

    def __eventShowWonderBegin(self, argsList):
        "Show Wonder Event"
        CvDebugTools.CvDebugTools().wonderMovie()

    def __eventShowWonderApply(self, playerID, netUserData, popupReturn):
        "Wonder Movie Apply"
        if getChtLvl() > 0:
            CvDebugTools.CvDebugTools().applyWonderMovie((popupReturn))

    ## Platy Builder ##
    def __eventEditUnitNameBegin(self, argsList):
        pUnit = argsList
        popup = PyPopup.PyPopup(CvUtil.EventEditUnitName, EventContextTypes.EVENTCONTEXT_ALL)
        popup.setUserData((pUnit.getID(), CyGame().getActivePlayer()))
        popup.setBodyString(text("TXT_KEY_RENAME_UNIT"))
        popup.createEditBox(pUnit.getNameNoDesc())
        popup.setEditBoxMaxCharCount(25)
        popup.launch()

    def __eventEditUnitNameApply(self, playerID, userData, popupReturn):
        unit = gc.getPlayer(userData[1]).getUnit(userData[0])
        newName = popupReturn.getEditBoxString(0)
        unit.setName(newName)
        if CyGame().GetWorldBuilderMode():
            WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeStats()
            WBUnitScreen.WBUnitScreen(
                CvPlatyBuilderScreen.CvWorldBuilderScreen()
            ).placeCurrentUnit()

    def __eventEditCityNameBegin(self, city, bRename):
        popup = PyPopup.PyPopup(CvUtil.EventEditCityName, EventContextTypes.EVENTCONTEXT_ALL)
        popup.setUserData((city.getID(), bRename, CyGame().getActivePlayer()))
        popup.setHeaderString(text("TXT_KEY_NAME_CITY"))
        popup.setBodyString(text("TXT_KEY_SETTLE_NEW_CITY_NAME"))
        # Absinthe: if not a rename, it should offer the CNM__eventEditCityBegin name as the default name
        if bRename:
            popup.createEditBox(city.getName())
        else:
            szName = get_data_from_upside_down_map(CITIES_MAP, city.getOwner(), city)
            if szName == "-1":
                popup.createEditBox(city.getName())
            else:
                szName = unicode(szName)
                popup.createEditBox(szName)
        # Absinthe: end
        popup.setEditBoxMaxCharCount(15)
        popup.launch()

    def __eventEditCityNameApply(self, playerID, userData, popupReturn):
        city = gc.getPlayer(userData[2]).getCity(userData[0])
        cityName = popupReturn.getEditBoxString(0)
        city.setName(cityName, not userData[1])
        if CyGame().GetWorldBuilderMode() and not CyGame().isInAdvancedStart():
            WBCityEditScreen.WBCityEditScreen().placeStats()

    def __eventWBUnitScriptPopupApply(self, playerID, userData, popupReturn):
        sScript = popupReturn.getEditBoxString(0)
        pUnit = gc.getPlayer(userData[0]).getUnit(userData[1])
        pUnit.setScriptData(CvUtil.convertToStr(sScript))
        WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
        return

    def __eventWBPlayerScriptPopupApply(self, playerID, userData, popupReturn):
        sScript = popupReturn.getEditBoxString(0)
        gc.getPlayer(userData[0]).setScriptData(CvUtil.convertToStr(sScript))
        WBPlayerScreen.WBPlayerScreen().placeScript()
        return

    def __eventWBCityScriptPopupApply(self, playerID, userData, popupReturn):
        sScript = popupReturn.getEditBoxString(0)
        pCity = gc.getPlayer(userData[0]).getCity(userData[1])
        pCity.setScriptData(CvUtil.convertToStr(sScript))
        WBCityEditScreen.WBCityEditScreen().placeScript()
        return

    def __eventWBScriptPopupBegin(self):
        return

    def __eventWBGameScriptPopupApply(self, playerID, userData, popupReturn):
        sScript = popupReturn.getEditBoxString(0)
        CyGame().setScriptData(CvUtil.convertToStr(sScript))
        WBGameDataScreen.WBGameDataScreen(
            CvPlatyBuilderScreen.CvWorldBuilderScreen()
        ).placeScript()
        return

    def __eventWBPlotScriptPopupApply(self, playerID, userData, popupReturn):
        sScript = popupReturn.getEditBoxString(0)
        pPlot = CyMap().plot(userData[0], userData[1])
        pPlot.setScriptData(CvUtil.convertToStr(sScript))
        WBPlotScreen.WBPlotScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
        return

    def __eventWBLandmarkPopupApply(self, playerID, userData, popupReturn):
        sScript = popupReturn.getEditBoxString(0)
        pPlot = CyMap().plot(userData[0], userData[1])
        iPlayer = userData[2]
        if userData[3] > -1:
            pSign = CyEngine().getSignByIndex(userData[3])
            iPlayer = pSign.getPlayerType()
            CyEngine().removeSign(pPlot, iPlayer)
        if len(sScript):
            if iPlayer == gc.getBARBARIAN_PLAYER():
                CyEngine().addLandmark(pPlot, CvUtil.convertToStr(sScript))
            else:
                CyEngine().addSign(pPlot, iPlayer, CvUtil.convertToStr(sScript))
        WBPlotScreen.iCounter = 10
        return


## Platy Builder ##
