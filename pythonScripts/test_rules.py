import rules


def testOr():
    print("Testing Or...")
    introCPEOr = rules.OrClasses(
        {"CPE 101", "CPE 202", "CPE 203"}, "Intro CPE Courses OR")
    if not introCPEOr.process("CPE 101", None) and introCPEOr.isSatisfied(None):
        print("...failed to process CPE 101")
        return False
    introCPEOr.reset()
    if not introCPEOr.process("CPE 203", None) and introCPEOr.isSatisfied(None):
        print("...failed to process CPE 203")
        return False
    introCPEOr.reset()
    if introCPEOr.process("TEST", None) or introCPEOr.isSatisfied(None):
        print("...wrongly processed TEST")
        return False
    return True


def testAnd():
    print("Testing And...")
    classSet = {"CPE 101", "CPE 202", "CPE 203"}
    introCPEAnd = rules.AndClasses(classSet.copy(), "Intro to CPE Courses And")

    for cl in classSet:
        if not introCPEAnd.process(cl, None):
            print(f"...failed to process {cl}")

    if not introCPEAnd.isSatisfied(None):
        print("...and was not satisfied when given all classes")
        return False

    introCPEAnd.reset()

    for cl in {"CPE 101", "CPE 203"}:
        introCPEAnd.process(cl, None)

    if introCPEAnd.isSatisfied(None):
        print("...and was satisfied with impartial list")
        return False
    return True


def testNoDuplicate():
    print("Testing No Doublecount...")

    classSet = {"CPE 101", "CPE 202", "CPE 203"}

    orSet = classSet.copy()
    orSet.add("CSC 474")

    introCPEOr = rules.OrClasses(orSet, "Intro CPE Courses OR")
    introCPEAnd = rules.AndClasses(classSet.copy(), "Intro to CPE Courses And")

    noDoubleCountIntro = rules.NoDoubleCountRules(
        {introCPEOr, introCPEAnd}, "No doublecounting intro")

    for cl in classSet:
        if not noDoubleCountIntro.process(cl, None):
            print(f"...did not process {cl}")
            return False

    if noDoubleCountIntro.isSatisfied(None):
        print("...double count was satisfied by partial requirements")
        return False

    noDoubleCountIntro.process("CSC 474", None)

    if not noDoubleCountIntro.isSatisfied(None):
        print("...double count was not satisfied full requirements")
        return False

    return True


def testOrRules():
    print("Testing Or Rules...")

    classSet = {"CPE 101", "CPE 202", "CPE 203"}

    animationAnd = rules.AndClasses({"CSC 474"}, "CSC 474 Required")
    introCPEAnd = rules.AndClasses(classSet.copy(), "Intro to CPE Courses And")

    animationOrIntroCPE = rules.OrRules(
        {animationAnd, introCPEAnd}, "Animation or Intro to CPE courses")

    if not animationOrIntroCPE.process("CSC 474", None):
        print("...failed to process CSC 474 for or")
        return False

    if not animationOrIntroCPE.isSatisfied(None):
        print("...Or rule not satisfied by one condition")
        return False

    animationOrIntroCPE.reset()

    if animationOrIntroCPE.isSatisfied(None):
        print("...failed to reset Or Rules rule properly")
        return False

    for cl in classSet:
        if not animationOrIntroCPE.process(cl, None):
            print(f"...failed to process {cl}")
            return False

    if not animationOrIntroCPE.isSatisfied(None):
        print("...Or Rules rule not satisfied by satisfying second rule")
        return False

    animationOrIntroCPE.process("CSC 474", None)

    if not animationOrIntroCPE.isSatisfied(None):
        print("...Or Rules rule not staying satisfied on multiple satisfaction")
        return False

    return True


def testAndRules():
    print("Testing And Rules...")

    classSet = {"CPE 101", "CPE 202", "CPE 203"}

    animationAnd = rules.AndClasses({"CSC 474"}, "CSC 474 Required")
    introCPEAnd = rules.AndClasses(classSet.copy(), "Intro to CPE Courses And")

    animationOrIntroCPE = rules.AndRules(
        {animationAnd, introCPEAnd}, "Animation and Intro to CPE courses")

    if not animationOrIntroCPE.process("CSC 474", None):
        print("...failed to process CSC 474 for And")
        return False

    if animationOrIntroCPE.isSatisfied(None):
        print("...And rule satisfied by one condition")
        return False

    animationOrIntroCPE.reset()

    if animationOrIntroCPE.isSatisfied(None):
        print("...failed to reset And Rules rule properly")
        return False

    for cl in classSet:
        if not animationOrIntroCPE.process(cl, None):
            print(f"...failed to process {cl}")
            return False

    if animationOrIntroCPE.isSatisfied(None):
        print("...And Rules rule satisfied by satisfying only second rule")
        return False

    animationOrIntroCPE.process("CSC 474", None)

    if not animationOrIntroCPE.isSatisfied(None):
        print("...And Rules rule not satisfied by all rules being satisfied")
        return False

    return True


def testNUnitsOfClasses():
    print("Testing n units of classes rule...")

    classDatabase = {"MATH248": {"cNum": "4"},
                     "BIO213": {"cNum": "4"},
                     "CHEM124": {"cNum": "2"},
                     "ENGL149": {"cNum": "2"}}

    nUnitsRule = rules.NUnitsOfClasses(
        {"CPE101", "CPE202", "MATH248", "BIO213", "CHEM124", "ENGL149", "IME144"},
        12,
        "12 Units of Random Classes")

    for cl in ["MATH248", "BIO213", "ENGL149"]:
        if not nUnitsRule.process(cl, classDatabase):
            print(f"...failed to process {cl}")
            return False

        if nUnitsRule.isSatisfied(classDatabase):
            print(f"...N units rule satisfied with less than number of required units")
            return False

    if not nUnitsRule.process("CHEM124", classDatabase):
        print("...failed to process CHEM124")
        return False

    if not nUnitsRule.isSatisfied(classDatabase):
        print("...failed to satisfy nUnitsRule with correct number of units")
        return False

    return True


def test():
    if not testOr():
        print("Failed Or Classes Test")

    if not testAnd():
        print("Failed And Classes Test")

    if not testNoDuplicate():
        print("Failed No Duplicate Test")

    if not testOrRules():
        print("Failed Or Rules Test")

    if not testAndRules():
        print("Failed And Rules Test")

    if not testNUnitsOfClasses():
        print("Failed N Units of Classes Test")


if __name__ == "__main__":
    test()
