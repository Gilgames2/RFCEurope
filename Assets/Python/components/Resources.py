# Rhye's and Fall of Civilization: Europe - Dynamic resources
# Based on SoI version, added by Absinthe

from CvPythonExtensions import *

from Consts import MessageData
from Core import text, message, year
from CoreTypes import Improvement, Bonus

# globals
gc = CyGlobalContext()


class Resources:
    def createResource(self, iX, iY, iBonus, textKey="TXT_KEY_RESOURCE_DISCOVERED"):
        """Creates a bonus resource and alerts the plot owner"""

        if (
            gc.getMap().plot(iX, iY).getBonusType(-1) == -1 or iBonus == -1
        ):  # Absinthe: only proceed if there isn't any bonus resources on the plot, or if we're removing the bonus
            if iBonus == -1:
                iBonus = gc.getMap().plot(iX, iY).getBonusType(-1)  # for alert
                gc.getMap().plot(iX, iY).setBonusType(-1)
            else:
                gc.getMap().plot(iX, iY).setBonusType(iBonus)

            iOwner = gc.getMap().plot(iX, iY).getOwner()
            if iOwner >= 0 and textKey != -1:  # Absinthe: only show alert to the tile owner
                city = gc.getMap().findCity(
                    iX,
                    iY,
                    iOwner,
                    TeamTypes.NO_TEAM,
                    True,
                    False,
                    TeamTypes.NO_TEAM,
                    DirectionTypes.NO_DIRECTION,
                    CyCity(),
                )
                if not city.isNone():
                    szText = text(
                        textKey,
                        gc.getBonusInfo(iBonus).getTextKey(),
                        city.getName(),
                        gc.getPlayer(iOwner).getCivilizationAdjective(0),
                    )
                    message(
                        iOwner,
                        szText,
                        sound="AS2D_DISCOVERBONUS",
                        event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                        button=gc.getBonusInfo(iBonus).getButton(),
                        color=MessageData.LIME,
                        location=(iX, iY),
                    )

    def removeResource(self, iX, iY, textKey="TXT_KEY_RESOURCE_EXHAUSTED"):
        """Removes a bonus resource and alerts the plot owner"""

        if (
            gc.getMap().plot(iX, iY).getBonusType(-1) != -1
        ):  # only proceed if there is a bonus resource on the plot
            iBonusType = gc.getMap().plot(iX, iY).getBonusType(-1)
            iImprovementType = gc.getMap().plot(iX, iY).getImprovementType()
            self.createResource(iX, iY, -1, textKey)
            # Absinthe: remove the improvement too, but only if it improves the given resource
            # 			for now only adding the ones we actually use
            # 			Pasture, Camp and Colonial Trade Route cannot be built on base terrain (only with resource), so it is always safe to remove those
            # 			the question is whether we should also remove Farms and Lumbermills for example
            if iBonusType == Bonus.HORSE and iImprovementType == Improvement.PASTURE:
                gc.getMap().plot(iX, iY).setImprovementType(-1)
            elif (
                iBonusType == Bonus.NORTH_ACCESS and iImprovementType == Improvement.COLONIAL_TRADE
            ):
                gc.getMap().plot(iX, iY).setImprovementType(-1)

    def checkTurn(self, iGameTurn):
        # Absinthe: note that all actions are taken place in the end of the turn, so actually the resources will appear/disappear for the next turn
        if iGameTurn == year(552):
            self.createResource(80, 24, Bonus.SILK)  # Silk near Constantinople
        elif iGameTurn == year(1000):
            self.createResource(36, 24, Bonus.RICE)  # Rice in Iberia
            self.createResource(86, 2, Bonus.RICE)  # Rice in the Middle East
        elif iGameTurn == (year(1066) + 1):
            self.removeResource(2, 69)  # Remove the NAA from Iceland
        elif iGameTurn == year(1452):  # Coffee spawns instead of being preplaced
            self.createResource(93, 0, Bonus.COFFEE)  # near Sinai
            self.createResource(99, 13, Bonus.COFFEE)  # between Damascus and Edessa
        elif iGameTurn == year(1500):
            self.createResource(
                55, 35, Bonus.RICE
            )  # Rice in Italy - represents trade of the merchant republics
        elif iGameTurn == year(1580):
            self.createResource(32, 59, Bonus.POTATO)  # Potatoes in Ireland
            self.createResource(29, 57, Bonus.POTATO)
            self.createResource(69, 49, Bonus.POTATO)  # Poland
            self.createResource(66, 46, Bonus.POTATO)
            self.createResource(60, 48, Bonus.POTATO)  # Northern Germany
            self.createResource(55, 52, Bonus.POTATO)
            self.createResource(59, 61, Bonus.ACCESS)  # Atlantic Access in Scandinavia

    def onTechAcquired(self, iTech, iPlayer):
        pass
