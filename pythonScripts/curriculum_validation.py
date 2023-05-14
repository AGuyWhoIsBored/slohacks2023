#!/usr/bin/env python3

import json_to_rules
import rules
import sys


def parseCurriculumFiles(fileName):
    f = open(fileName, "r")
    rulesSet = set()
    for name in f.readlines():
        rulesSet.add(json_to_rules.parseRules(name.strip()))
    f.close()

    return rules.AndRules(rulesSet, "Curriculum")


def validateCourses(courseFile, curriculum, courseDatabase):
    f = open(courseFile, "r")
    for course in f.readlines():
        curriculum.process(course.strip(), courseDatabase)
    f.close()


def writeResult(outfileName, curriculum, courseDatabase):
    f = open(outfileName, "w")
    f.write(f"{curriculum.isSatisfied(courseDatabase)}")
    f.close()


def main(args):
    # fail silently if incorrect number of args :)
    # >:(
    print("executing python script")
    if (len(args) != 5):
        return

    curriculum = parseCurriculumFiles(args[1])
    courseDatabase = json_to_rules.parseCourseData(args[2])
    validateCourses(args[3], curriculum, courseDatabase)
    print(curriculum.getUnsatisfiedRules(courseDatabase))
    writeResult(args[4], curriculum, courseDatabase)


if __name__ == "__main__":
    main(sys.argv)
