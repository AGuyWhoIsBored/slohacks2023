import json
import rules


def parseCourseData(fileName):
    f = open(fileName, "r")
    classes = json.load(f)
    d = dict()
    for cl in classes:
        d[cl["cID"]] = cl

    f.close()
    return d


def deprecated_parseGEReqs(fileName):
    """Well-formatted GE Reqs should simply use parseRules()"""
    f = open(fileName, "r")
    reqs = json.load(f)
    rulesSet = set()
    for reqName, reqClasses in reqs.items():
        rulesSet.add(rules.OrClasses(set(reqClasses), reqName))

    f.close()
    return rules.NoDoubleCountRules(rulesSet, "GE Requirements")


def dictToRule(ruleDict: dict):
    t = ruleDict["type"]
    rule = None
    if t == "Or":
        rule = rules.OrClasses(set(ruleDict["classes"]), ruleDict["name"])
    elif t == "And":
        rule = rules.AndClasses(set(ruleDict["classes"]), ruleDict["name"])
    elif t == "CompoundOr":
        rule = rules.OrRules({dictToRule(d)
                             for d in ruleDict["rules"]}, ruleDict["name"])
    elif t == "CompoundAnd":
        rule = rules.AndRules({dictToRule(d)
                              for d in ruleDict["rules"]}, ruleDict["name"])
    elif t == "NoDoubleCount":
        rule = rules.NoDoubleCountRules(
            {dictToRule(d) for d in ruleDict["rules"]}, ruleDict["name"])
    elif t == "NUnitsOf":
        rule = rules.NUnitsOfClasses(
            set(ruleDict["classes"]), int(ruleDict["number"]), ruleDict["name"])
    return rule


def parseRules(fileName) -> rules.AndRules:
    f = open(fileName, "r")
    jsonRules = json.load(f)
    rulesSet = set()

    for ruleDict in jsonRules:
        rulesSet.add(dictToRule(ruleDict))

    return rules.AndRules(rulesSet, fileName)


def getSatisfyingGESet(fileName):
    f = open(fileName, "r")
    reqs = json.load(f)
    classes = []
    for reqName, reqClasses in reqs.items():
        classes.append(reqClasses[0])

    f.close()
    return classes


def main():
    courseData = parseCourseData("2020-2021.json")
    GERules = deprecated_parseGEReqs("2022-2026-GE.json")
    satisfyingClasses = getSatisfyingGESet("2022-2026-GE.json")
    for cl in satisfyingClasses:
        GERules.process(cl, courseData)
    if not GERules.isSatisfied():
        print("Failed to satisfy criteria")
    else:
        print("Finished")


if __name__ == "__main__":
    main()
