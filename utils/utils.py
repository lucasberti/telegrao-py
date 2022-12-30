from dataclasses import fields

# 
class DataClassUnpack:
    classFieldCache = {}

    @classmethod
    def instantiate(cls, classToInstantiate, argDict):
        if classToInstantiate not in cls.classFieldCache:
            cls.classFieldCache[classToInstantiate] = {f.name for f in fields(classToInstantiate) if f.init}

        fieldSet = cls.classFieldCache[classToInstantiate]
        filteredArgDict = {k : v for k, v in argDict.items() if k in fieldSet}
        return classToInstantiate(**filteredArgDict)