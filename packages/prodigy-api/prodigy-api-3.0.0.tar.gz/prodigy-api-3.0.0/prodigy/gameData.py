import os
from typing import List, TypedDict
import requests_cache
from prodigy.gameStatus import gameStatus

s = requests_cache.CachedSession(os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache"))

class GameDataObject(TypedDict):
    ID: int
    assetID: int
    type: str
    gender: int
    data: dict
    metadata: dict
    name: str

class GameData(TypedDict):
    ad: List[GameDataObject]   
    affix: List[GameDataObject]
    atlas: List[GameDataObject]
    bgm: List[GameDataObject]
    bitmapFont: List[GameDataObject]
    boots: List[GameDataObject]
    boss: List[GameDataObject]
    bountyName: List[GameDataObject]
    bundle: List[GameDataObject]
    currency: List[GameDataObject]
    dailyReward: List[GameDataObject]
    dialogue: List[GameDataObject]
    dorm: List[GameDataObject]
    dormbg: List[GameDataObject]
    dungeon: List[GameDataObject]
    emote: List[GameDataObject]
    eyeColor: List[GameDataObject]
    face: List[GameDataObject]
    faceColor: List[GameDataObject]
    follow: List[GameDataObject]
    fontStyle: List[GameDataObject]
    fossil: List[GameDataObject]
    fsm: List[GameDataObject]
    gameFeed: List[GameDataObject]
    gender: List[GameDataObject]
    generic: List[GameDataObject]
    giftBox: List[GameDataObject]
    hair: List[GameDataObject]
    hairColor: List[GameDataObject]
    hat: List[GameDataObject]
    item: List[GameDataObject]
    itemTable: List[GameDataObject]
    key: List[GameDataObject]
    mathTownDecor: List[GameDataObject]
    mathTownFrame: List[GameDataObject]
    mathTownInterior: List[GameDataObject]
    mount: List[GameDataObject]
    name: List[GameDataObject]
    nickname: List[GameDataObject]
    orb: List[GameDataObject]
    outfit: List[GameDataObject]
    particleEffect: List[GameDataObject]
    pet: List[GameDataObject]
    prizeWheel: List[GameDataObject]
    relic: List[GameDataObject]
    sfx: List[GameDataObject]
    singleImage: List[GameDataObject]
    skinColor: List[GameDataObject]
    spell: List[GameDataObject]
    spellRelic: List[GameDataObject]
    spine: List[GameDataObject]
    streamedMap: List[GameDataObject]
    tiledMap: List[GameDataObject]
    tileset: List[GameDataObject]
    titan: List[GameDataObject]
    ui: List[GameDataObject]
    weapon: List[GameDataObject]

def gameData(log: bool = False) -> GameData:
    gameDataVersion = gameStatus(log)["prodigyGameFlags"]["gameDataVersion"]
    if log:
        print("Fetching game version...")
    return s.get(f"https://cdn.prodigygame.com/game/data/production/{gameDataVersion}/data.json").json()
