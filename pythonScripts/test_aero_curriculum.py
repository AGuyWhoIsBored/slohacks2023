import json_to_rules
import rules


def main():
    sampleCourses = ["AERO121", "AERO215", "AERO220",
                     "AERO299", "AERO300", "AERO302",
                     "AERO303", "AERO320", "AERO321",
                     "AERO331", "AERO350", "AERO431",
                     "AERO433", "AERO460", "AERO465",
                     "CE208", "EE201", "EE251", "BIO213",
                     "CHEM124", "ENGL149", "IME144",
                     "MATE210", "MATH141", "MATH142",
                     "MATH143", "MATH241", "MATH244",
                     "ME211", "ME212", "PHYS141",
                     "PHYS132", "PHYS133", "STAT312",
                     "AERO351", "AERO355", "AERO356",
                     "AERO402", "AERO421", "AERO446",
                     "AERO447", "AERO448", "AERO449",
                     "AERO360", "AERO432", "AERO566"]

    satisfyingClasses = json_to_rules.getSatisfyingGESet("2020-2021-GE.json")
    sampleCourses += satisfyingClasses

    courseDatabase = json_to_rules.parseCourseData("2020-2021.json")
    geRules = json_to_rules.parseGEReqs("2020-2021-GE.json")
    aeroRules = json_to_rules.parseRules("2020-2021-AERO.json")
    astronauticsRules = json_to_rules.parseRules(
        "2020-2021-AERO-Astronautics-Concentration.json")

    curriculum = rules.AndRules(
        {geRules, aeroRules, astronauticsRules}, "Curriculum")

    for cl in sampleCourses:
        if not curriculum.process(cl, courseDatabase):
            pass  # print(f"Failed to process {cl}\n")
            # return

    if not curriculum.isSatisfied(courseDatabase):
        print("Curriculum was not satisfied by provided classes")
        return

    print("Passed!")


if __name__ == "__main__":
    main()
