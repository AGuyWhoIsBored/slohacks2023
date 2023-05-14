#!/usr/local/bin/python3

import json_to_rules
import rules
import sys
import os

# https://stackoverflow.com/a/10824420
def flatten(container):
    for i in container:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i
            
# get the root req name and flatten the rest
def pullAndFlatten(container):
    req = container[0]
    rest = list(flatten(container[1]))

    # extra logic to preserve the recursion chain
    newRest = [rest[0]]
    for elem in rest[1:]:
        if elem != newRest[-1]:
            newRest.append(elem)

    # if we have a simple nested req (eg ['geA3', ['geA3]]), then remove it
    newRestFinal = [] if len(rest) == 1 and rest[0] == req else newRest

    return [req, newRestFinal]

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

def writeUnsatisfiedReqs(outfileName, unsatisfiedreqs):
    f = open(outfileName, "w")
    f.write(f"{unsatisfiedreqs}")
    f.close()

def main(args):
    
    # if executing from backend, change cwd so paths work
    if os.getcwd()[-9:] == 'goBackend':
        os.chdir(os.getcwd() + '/../pythonScripts')
    print("executing python script")
    print('args', args)
    print('cwd', os.getcwd())

    # fail silently if incorrect number of args :)
    # >:(
    if (len(args) != 5):
        return

    curriculum = parseCurriculumFiles(args[1])
    courseDatabase = json_to_rules.parseCourseData(args[2])
    validateCourses(args[3], curriculum, courseDatabase)

    # write out the missing reqs
    res = curriculum.getUnsatisfiedRules(courseDatabase)   
    resZipped = list(zip(res[::2], res[1::2]))
    missingReqs = [[elem[0][:-5], pullAndFlatten(elem[1])] for elem in resZipped]
    
    writeUnsatisfiedReqs(args[4], missingReqs)
    # writeResult(args[4], curriculum, courseDatabase)

if __name__ == "__main__":
    main(sys.argv)
