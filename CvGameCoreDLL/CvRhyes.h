//Rhye
#ifndef CVRHYES_H
#define CVRHYES_H

#include "CvGlobals.h"

// rhyes.h
//#define EARTH_X					(100)
//#define EARTH_Y					(73)

#define MAX_NUM_PROVINCES (150)
#define PROVINCE_OWN (5)      // owns every tile
#define PROVINCE_CONQUER (4)  // own every city
#define PROVINCE_DOMINATE (3) // 2*City populations + Num plots
#define PROVINCE_LOST (2)     // lost, others have cities, you don't
#define PROVINCE_NOTHING (0)  // we have done nothing of the above

#define MAX_COM_SHRINE (20)

// 3Miro: Hard-coding things in the C++ makes the mod very rigid. We should use XML and Python to set the variables here
// this was needed for the Dynamic Civ Names, but not anymore (DCN is messed up code)
/*#define BURGUNDY				(0)
#define BYZANTIUM				(1)
#define FRANKIA					(2)
#define ARABIA					(3)
#define BULGARIA				(4)
#define CORDOBA					(5)
#define SPAIN					(6)
#define NORSE					(7)
#define VENECIA					(8)
#define KIEV					(9)
#define HUNGARY					(10)
#define GERMANY					(11)
#define POLAND					(12)
#define MOSCOW					(13)
#define GENOA					(14)
#define ENGLAND					(15)
#define PORTUGAL				(16)
#define AUSTRIA					(17)
#define TURKEY					(18)
#define SWEDEN					(19)
#define DUTCH					(20)
#define POPE					(21)*/
//#define NUM_MAJOR_PLAYERS		(21)
//#define INDEPENDENT			(22)
//#define INDEPENDENT2			(23)
//#define INDEPENDENT3			(24)
//#define INDEPENDENT4			(25)
//#define NUM_ALL_PLAYERS		(25)
//#define BARBARIAN				(26)
//#define NUM_ALL_PLAYERS_B		(26)

#define UP_HAPPINESS (0)
#define UP_PER_CITY_COMMERCE (1)
#define UP_CITY_TILE_YIELD (2)
#define UP_RELIGIOUS_TOLERANCE (3)
#define UP_CULTURAL_TOLERANCE (4)
#define UP_COMMERCE_PERCENT (5)
#define UP_UNIT_PRODUCTION (6)
#define UP_ENABLE_CIVIC (7)
#define UP_TRADE_ROUTES (8)
#define UP_IMPROVEMENT_BONUS (9)
#define UP_PROMOTION_I (10)
#define UP_PROMOTION_II (11)
#define UP_CAN_ENTER_TERRAIN (12)
#define UP_NO_RESISTANCE (13)
#define UP_CONSCRIPTION (14)
#define UP_INQUISITION (15)
#define UP_EMPEROR (16)
#define UP_FAITH (17)
#define UP_MERCENARIES (18)
#define UP_LAND_STABILITY (19)
#define UP_DISCOVERY (20)
#define UP_ENDLESS_LAND (21)
#define UP_FOREIGN_SEA (22)
#define UP_PIOUS (23)
#define UP_PAGAN_CULTURE (24)
#define UP_PAGAN_HAPPY (25)
#define UP_HEALTH_FOOD (26)
#define UP_TERRAIN_BONUS (27)
#define UP_FEATURE_BONUS (28)
#define UP_STABILITY_1 (29) // stability is handled in Python so make these generic
#define UP_STABILITY_2 (30) // stability is handled in Python so make these generic
#define UP_STABILITY_3 (31) // stability is handled in Python so make these generic
#define UP_STABILITY_4 (32) // stability is handled in Python so make these generic
#define UP_JANISSARY (33)
#define UP_IMPROVEMENT_BONUS_2 (34)
#define UP_IMPROVEMENT_BONUS_3 (35)
#define UP_IMPROVEMENT_BONUS_4 (36)
#define UP_IMPROVEMENT_BONUS_5 (37)

#define UP_TOTAL_NUM (38)

// 3MiroFaith: define the possible bonuses here
#define FP_STABILITY (0)
#define FP_CIVIC_COST (1)
#define FP_GROWTH (2)
#define FP_UNITS (3)
#define FP_SCIENCE (4)
#define FP_PRODUCTION (5)
#define FP_DIPLOMACY (6)
#define FP_TOTAL_NUM (7)

//#define MAX_NUM_TECHS			(100)

// Absinthe: English UP is handled differently now
//#define IMPROVEMENT_WORKSHOP	(8)

// Absinthe: Cordoban and Swedish UP is handled differently now
//#define PROMOTION_MEDIC		(12)
//#define PROMOTION_FORMATION	(7)

// Absinthe: damage modifiers for the Hungarian UB
#define ENEMY_DAMAGE (12)
#define BARB_DAMAGE (18)

#define PROTESTANTISM (0)
#define ISLAM (1)
#define CATHOLICISM (2)
#define ORTHODOXY (3)
#define JUDAISM (4)

bool MiroBelongToCore(int iCiv, int x, int y);
bool MiroBelongToNormal(int iCiv, int x, int y);
int getSettlersMaps(int iCiv, int y, int x, char *);
// Absinthe: moved to CvPlayer, exported to python
int getWarsMaps(int iCiv, int y, int x, char *);

bool isIndep(int iCiv); // true if the nation is independent

int getModifiedTechCostForTurn(int iTech, int iTurn);

// TODO split to soundtrack_era
enum Eras
{
  ERA_ANCIENT,
  ERA_CLASSICAL,
  ERA_MEDIEVAL,
  ERA_RENAISSANCE,
  ERA_MEDIEVAL_ISLAMIC,
};

enum RfceTechs
{
  // early middle age
  CALENDAR,
  ARCHITECTURE,
  BRONZE_CASTING,
  THEOLOGY,
  MANORIALISM,
  STIRRUP,
  ENGINEERING,
  CHAIN_MAIL,
  ART,
  MONASTICISM,
  VASSALAGE,
  ASTROLABE,
  MACHINERY,
  VAULTED_ARCHES,
  MUSIC,
  HERBAL_MEDICINE,
  FEUDALISM,
  FARRIERS,
  // high middle age
  MAPMAKING,
  BLAST_FURNACE,
  SIEGE_ENGINES,
  GOTHIC_ARCHITECTURE,
  LITERATURE,
  CODE_OF_LAWS,
  ARISTOCRACY,
  LATEEN_SAILS,
  PLATE_ARMOR,
  MONUMENT_BUILDING,
  CLASSICAL_KNOWLEDGE,
  ALCHEMY,
  CIVIL_SERVICE,
  CLOCKMAKING,
  PHILOSOPHY,
  EDUCATION,
  GUILDS,
  CHIVALRY,
  // late middle age
  OPTICS,
  REPLACEABLE_PARTS,
  PATRONAGE,
  GUNPOWDER,
  BANKING,
  MILITARY_TRADITION,
  SHIP_BUILDING,
  DRAMA,
  DIVINE_RIGHT,
  CHEMISTRY,
  PAPER,
  PROFESSIONAL_ARMY,
  PRINTING_PRESS,
  PUBLIC_WORKS,
  MATCH_LOCK,
  ARABIC_KNOWLEDGE,
  // renaissance
  ASTRONOMY,
  STEAM_ENGINES,
  CONSTITUTION,
  POLYGONAL_FORT,
  ARABIC_MEDICINE,
  RENAISSANCE_ART,
  NATIONALISM,
  LIBERALISM,
  SCIENTIFIC_METHOD,
  MILITARY_TACTICS,
  NAVAL_ARCHITECTURE,
  CIVIL_ENGINEERING,
  RIGHT_OF_MAN,
  ECONOMICS,
  PHYSICS,
  BIOLOGY,
  COMBINED_ARMS,
  TRADING_COMPANIES,
  MACHINE_TOOLS,
  FREE_MARKET,
  EXPLOSIVES,
  MEDICINE,
  INDUSTRIAL_TECH,
};

#endif // CVRHYES_H

extern int INDEP_START;
extern int INDEP_END;
extern int BARBARIAN;
extern bool *AI_INDEP_HUNT;

extern int UNIT_PROSECUTOR;
extern int UNIT_PROSECUTOR_CLASS;
extern int NUM_RELIGIONS;

extern int UNIT_SAINT;
extern int UNIT_SAINT_BENEFIT;
extern int UNIT_SAINT_1_TRESHHOLD;
extern int UNIT_SAINT_3_TRESHHOLD;

extern int PAPAL_PLAYER;
extern int PAPAL_RELIGION;

extern int SCHISM_A, SCHISM_B; // The two religions
extern int SCHISM_YEAR;        // the year of the split (turn of the split)

extern int HOLIEST_CITY_X, HOLIEST_CITY_Y; // Holiest City, i.e. immune to prosecutions

extern int EARTH_X;
extern int EARTH_Y;
extern int NUM_MAJOR_PLAYERS;
extern int NUM_ALL_PLAYERS;
extern int NUM_ALL_PLAYERS_B;
extern int SETTLER_OFFSET;

extern int MAX_NUM_TECHS;
extern int NUM_BUILDINGS; // Plague is the last "building"
#define BUILDING_PLAGUE (NUM_BUILDINGS - 1)

extern int *startingTurn;
extern int *turnPlayed;      // 3Miro: overkill but leave it
extern int *civSpreadFactor; // 3Miro: includes major players, minor players, indeps and barbs

extern int
    techFoundedDate[120]; // 3Miro the date a tech has been founded, currently 120 tech allowed, read/write from CvGame

extern int *settlersMaps;
extern int *warsMaps;

extern int *UniquePowers;
extern int *FaithPowers;

extern int *FaithPointsCap;

// 3Miro: Start the export of the balance factors (for AI)
extern int *growthThresholdAI;
extern int *productionModifierUnitsAI;
extern int *productionModifierBuildingsAI;
extern int *productionModifierWondersAI;
extern int *inflationModifierAI;
extern int *gpModifierAI;
extern int *unitSupportModifierAI;
extern int *cityDistanceSupportAI;
extern int *cityNumberSupportAI;
extern int *civicSupportModifierAI;
extern int *researchModifierAI;
extern int *healthModifierAI;
extern int *workerModifierAI;
extern int *cultureModifierAI;
// 3Miro: Start the export of the balance factors (for Human)
extern int *growthThresholdHu;
extern int *productionModifierUnitsHu;
extern int *productionModifierBuildingsHu;
extern int *productionModifierWondersHu;
extern int *inflationModifierHu;
extern int *gpModifierHu;
extern int *unitSupportModifierHu;
extern int *cityDistanceSupportHu;
extern int *cityNumberSupportHu;
extern int *civicSupportModifierHu;
extern int *researchModifierHu;
extern int *healthModifierHu;
extern int *workerModifierHu;
extern int *cultureModifierHu;

extern int *cityInitPop;
extern int **cityInitBuildings;
// balance AI
extern int *cityClusterTop;
extern int *cityClusterBottom;
extern int *cityClusterMinus;
extern int **diplomacyModifiers;
extern int *colonyAIModifier;
extern int *startingWorkers;
extern int *buildingPrefs;

extern int *cityWarDistance;
extern int **techPreferences;

// 3Miro: AI cheat to make Ottomans conquer Constantinople
extern int psychoAI_x;
extern int psychoAI_y;
extern int psychoAI_player;

// 3Miro: AI cheats to help nations historically conquer certain players
extern int *historicalEnemyAIcheat;

// Absinthe: unused in RFCE
// 3Miro: Stability last owned cities and plots
//extern int* lOwnedCities;
//extern int* lOwnedPlots;

// Absinthe: in python now
// 3Miro: counts the turn for prosecution instability
extern int *ProsecutionCount;

// 3Miro: Normal and Core Areas for stability and map swaps
extern int **CoreAreasRect;
extern int *CoreAreasMinusCount;
extern int **CoreAreasMinus;
extern int **NormalAreasRect;
extern int *NormalAreasMinusCount;
extern int **NormalAreasMinus;

extern int *StrategicTileX;
extern int *StrategicTileY;

// 3Miro: GlobalWarming
extern bool USE_GLOBAL_WARMING;
extern int FAST_TERRAIN;

// 3Miro: hack on the culture bug, see CvRhye.cpp
extern bool withinSpawnDate;

// 3Miro: autorun hack (a unit is created and destroyed every turn for the Human player)
// we need a place to put the unit and a unit index
extern int iAutorunUnit;
extern int iAutorunX;
extern int iAutorunY;

// 3Miro: Commerce from Building + Civic
extern int iCivicBuildingCommerse1;
extern int iCivicBuildingCommerse2;
extern int iCivicBuildingCommerse3;
// iBuilding + 1000 * iCivic + 100,000 * iGold + 1,000,000 * iResearch + 10,000,000 * iCulture + 100,000,000 * iEspionage
// none of the bonuses can be more than 9

// 3MiroTimeline: set the timeline for technologies
extern int *timelineTechDates;
extern int timelineTechPenaltyTop;
extern int timelineTechPenaltyBottom;
extern int timelineTechPenaltyCap;
extern int timelineTechBuffTop;
extern int timelineTechBuffBottom;
extern int timelineTechBuffCap;

// 3MiroProvinces: province map and other things
extern int *provinceMap;
extern int *provinceSizeList; // those are for cross reference purposes
extern int **provinceTileList;
extern int iNumProvinceTypes;              // how many type of provinces are there
extern int *iSettlerValuesPerProvinceType; // how do settlers value tiles from the specific province (AI purposes)
extern int *iWarValuesPerProvinceType;     // how do you consider attacking a specific province (AI purposes)
extern int *iModCultureTop;                // how do you modify culture for the specific province
extern int *iModCultureBottom;             // Culture * Top / Bottom
extern int *iCultureImmune;          // locks a province so that only the player in exception can put culture in it
extern int *iCultureImmuneException; // the only player that can put culture on the tiles of this province
//extern int provinceToColor; //Absinthe: moved to python
extern int numRegions;         // for map areas, give the number of regions
extern int *provinceRegionMap; // give the region for each province (province -1 is default reigion 0)

// Additional Plotting Tools:
extern int iPlotCore;   // plot the core area of this player
extern int iPlotNormal; // plot the normal area of this player
// Absinthe: plotting updates:
//extern int iPlotSettlers; // which player to plot for the settlers map
//extern int iPlotWars; // which player to plot for the wars map
extern int iCoreToPlot;
extern int iNormalToPlot;
//extern int iWhatToPlot; // 0 plots Core, 1 plots Normal, 2 plots Settlers and 3 plots Wars

extern int *conditionalVassalage; // conditions for vassalizing, -1 cannot vassalize, 1 can vassalize, 0 condition
extern int
    provinceFlagToVassalize; // we can vassalize if we have overlap (city in province) of provinces of type >= provinceFlagToVassalize

// 3Miro: Protestant Schism: this serves to stop non-Catholics from founding Protestantism
extern int iParentReligion;
extern int iSchismReligion;

extern int iMercPromotion; // 3Miro: the promotion to block upgrades

extern int iPeaceTurnsAfterSpawn;

extern int minorReligion;         // 3Miro: set the Jews here to be the minorReligion in the game
extern int minorReligionRefugies; // 3Miro: this is incremented every time the minorReligion is prosecuted
