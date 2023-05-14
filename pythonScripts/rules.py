from itertools import permutations


class OrClasses():
    def __init__(self, classes: set, name: str) -> None:
        self.classes = classes
        self.satisfied = False
        self.name = name

    def __repr__(self):
        return self.name

    def getName(self) -> str:
        """returns the human-friendly name associated with the rule"""
        return self.name

    def process(self, cl, classDatabase: dict) -> bool:
        """Attempts to satisfy the rule (or part of the rule) with the provided class, cl.
        Returns True if the class satisfied part of the rule"""
        if cl in self.classes:
            self.satisfied = True
            return True
        return False

    def doesClassApply(self, cl, classDatabase: dict) -> bool:
        """Returns True if the class applies to the given rule"""
        return cl in self.classes

    def isSatisfied(self, classDatabase: dict) -> bool:
        """Returns true if the rule is satisfied"""
        return self.satisfied

    def reset(self) -> bool:
        """Resets the state of the rule"""
        self.satisfied = False

    def copy(self) -> 'OrClasses':
        return OrClasses(self.classes.copy(), self.name)

    def getUnsatisfiedRules(self, classDatabase):
        if self.isSatisfied(classDatabase):
            return []
        return [self.name]


class AndClasses():
    def __init__(self, classes: set, name: str) -> None:
        self.classes = classes
        self.savedClasses = classes.copy()
        self.satisfied = False
        self.name = name

    def __repr__(self):
        return self.name

    def getName(self) -> str:
        """returns the human-friendly name associated with the rule"""
        return self.name

    def process(self, cl, classDatabase: dict) -> bool:
        """Attempts to satisfy the rule (or part of the rule) with the provided class, cl.
        Returns True if the class satisfied part of the rule"""
        if cl in self.classes:
            self.classes.remove(cl)
            return True
        return False

    def doesClassApply(self, cl, classDatabase: dict) -> bool:
        """Returns True if the class applies to the given rule"""
        return cl in self.classes

    def isSatisfied(self, classDatabase: dict) -> bool:
        """Returns true if the rule is satisfied"""
        return len(self.classes) == 0

    def reset(self) -> bool:
        """Resets the state of the rule"""
        self.satisfied = False
        self.classes = self.savedClasses.copy()

    def copy(self) -> 'AndClasses':
        return AndClasses(self.classes.copy(), self.getName)

    def getUnsatisfiedRules(self, classDatabase):
        if self.isSatisfied(classDatabase):
            return []
        return [self.name]


class NUnitsOfClasses():
    def __init__(self, classes: set, numUnits: int, name: str) -> None:
        self.classes = classes
        self.unitsRequired = numUnits
        self.unitsFulfilled = 0
        self.name = name

    def __repr__(self):
        return self.name

    def getName(self) -> str:
        """returns the human-friendly name associated with the rule"""
        return self.name

    def process(self, cl, classDatabase: dict) -> bool:
        """Attempts to satisfy the rule (or part of the rule) with the provided class, cl.
        Returns True if the class satisfied part of the rule"""
        if cl in self.classes:
            unitStr = classDatabase[cl]["cUnits"]
            unitStr = unitStr.split("-")
            self.unitsFulfilled += int(unitStr[len(unitStr) - 1])
            return True
        return False

    def doesClassApply(self, cl, classDatabase: dict) -> bool:
        """Returns True if the class applies to the given rule"""
        return cl in self.classes

    def isSatisfied(self, classDatabase: dict) -> bool:
        """Returns true if the rule is satisfied"""
        return self.unitsFulfilled >= self.unitsRequired

    def reset(self) -> bool:
        """Resets the state of the rule"""
        self.satisfied = False
        self.unitsFulfilled = 0

    def copy(self) -> 'NUnitsOfClasses':
        return NUnitsOfClasses(self.classes.copy(), self.unitsRequired, self.name)

    def getUnsatisfiedRules(self, classDatabase):
        if self.isSatisfied(classDatabase):
            return []
        return [self.name]


class NoDoubleCountRules():
    def __init__(self, rules: set, name: str) -> None:
        self.rulesAndApplicableClasses = {rule: [] for rule in rules}
        self.satisfied = False
        self.name = name

    def __repr__(self):
        return self.name

    def getName(self) -> str:
        """returns the human-friendly name associated with the rule"""
        return self.name

    def process(self, cl, classDatabase: dict) -> bool:
        """Attempts to satisfy the rule (or part of the rule) with the provided class, cl.
        Returns True if the class satisfied part of the rule"""
        isClassApplicable = False
        for rule in self.rulesAndApplicableClasses.keys():
            if rule.doesClassApply(cl, classDatabase):
                self.rulesAndApplicableClasses[rule].append(cl)
                isClassApplicable = True
        return isClassApplicable

    def isSatisfiedHelper(self, rulesAndClasses: list, usedClasses: set, classDatabase: dict) -> bool:
        if len(rulesAndClasses) == 0:
            return True
        rule, classes = rulesAndClasses.pop()
        numClasses = len(classes)
        usedClassesFromPerm = []
        for classPermutaiton in permutations(classes, numClasses):
            # Pick classes until the rule is satisfied, or there are no more classes
            i = 0
            while i < numClasses and not rule.isSatisfied(classDatabase):
                # If the classes has not already been used by a rule, use it in the current rule
                if (classPermutaiton[i] not in usedClasses):
                    rule.process(classPermutaiton[i], classDatabase)
                    usedClasses.add(classPermutaiton[i])
                    usedClassesFromPerm.append(classPermutaiton[i])
                i += 1

            # If the rule was satisfied, try to satisfy the next rule
            if rule.isSatisfied(classDatabase):
                if (self.isSatisfiedHelper(rulesAndClasses, usedClasses, classDatabase)):
                    rulesAndClasses.append((rule, classes))
                    return True

            for cl in usedClassesFromPerm:
                usedClasses.remove(cl)

            usedClassesFromPerm.clear()

            # If the rule was not satisfied, no permutation will satisfy the rule
            if not rule.isSatisfied(classDatabase):
                rule.reset()
                rulesAndClasses.append((rule, classes))
                return False

            rule.reset()

        # If no permutation satisfied the rule, return False
        rulesAndClasses.append((rule, classes))
        return False

    def isSatisfied(self, classDatabase: dict) -> bool:
        """Returns true if the rule is satisfied"""
        ruleAndClassPairs = [(rule.copy(), classes)
                             for rule, classes in self.rulesAndApplicableClasses.items()]
        ruleAndClassPairs.sort(key=lambda pair: len(pair[1]), reverse=True)
        usedClasses = set()
        return self.isSatisfiedHelper(ruleAndClassPairs, usedClasses, classDatabase)

    def getUnsatisfiedRules(self, classDatabase):
        if self.isSatisfied(classDatabase):
            return []
        return [self.name]


class OrRules():
    def __init__(self, rules: set, name: str) -> None:
        self.rules = rules
        self.satisfied = False
        self.name = name

    def __repr__(self):
        return self.name

    def getName(self):
        return self.name

    def process(self, cl, classDatabase: dict):
        isClassApplicable = False
        for rule in self.rules:
            isClassApplicable = isClassApplicable or rule.process(
                cl, classDatabase)
            if rule.isSatisfied(classDatabase):
                self.satisfied = True
        return isClassApplicable

    def doesClassApply(self, cl, classDatabase: dict):
        for rule in self.rules:
            if rule.doesClassApply(cl, classDatabase):
                return True
        return False

    def isSatisfied(self, classDatabase: dict):
        return self.satisfied

    def reset(self):
        for rule in self.rules:
            rule.reset()
        self.satisfied = False

    def getUnsatisfiedRules(self, classDatabase):
        if self.isSatisfied(classDatabase):
            return []
        return [self.name]


class AndRules():
    def __init__(self, rules: set, name: str) -> None:
        self.rules = rules
        self.savedRules = rules.copy()
        self.name = name

    def __repr__(self):
        return self.name

    def getName(self):
        return self.name

    def process(self, cl, classDatabase: dict):
        isClassApplicable = False
        satisfied_rules = []
        for rule in self.rules:
            isClassApplicable = rule.process(
                cl, classDatabase) or isClassApplicable
            if rule.isSatisfied(classDatabase):
                satisfied_rules.append(rule)

        for rule in satisfied_rules:
            self.rules.remove(rule)

        return isClassApplicable

    def doesClassApply(self, cl, classDatabase: dict):
        for rule in self.rules:
            if rule.doesClassApply(cl, classDatabase):
                return True
        return False

    def isSatisfied(self, classDatabase: dict):
        return len(self.rules) == 0

    def reset(self):
        self.rules = self.savedRules.copy()
        for rule in self.rules:
            rule.reset()

    def getUnsatisfiedRules(self, classDatabase):
        # only unsatisfied rules are in the rules set
        ret = []
        for rule in self.rules:
            ret += (rule.name, rule.getUnsatisfiedRules(classDatabase))
        return ret


def main():
    print("Nice")


if __name__ == "__main__":
    main()
