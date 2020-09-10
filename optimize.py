#!/usr/bin/env python3

import csv
from ortools.graph import pywrapgraph

INDEX_ITERATOR = 0


def assignNode():
    global INDEX_ITERATOR
    ret = INDEX_ITERATOR
    INDEX_ITERATOR += 1
    return ret


SOURCE_NODE_INDEX = assignNode()
SINK_CONSTRAINT_INDEX = assignNode()
SINK_NODE_INDEX = assignNode()
schoolNodeMapping = {}
nodeSchoolMapping = {}
dateNodeMapping = {}
nodeDateMapping = {}
indexDateMapping = {}
rowIndexToDate = {}

START_NODES = []
END_NODES = []
CAPACITIES = []
UNIT_COSTS = []


def parse():
    with open("date-data.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        row_idx = 0

        for row in reader:
            if row_idx == 0:
                buildDateNodesForRow(row)
            else:
                school_name = row[0]
                schoolNodeMapping[school_name] = assignNode()
                nodeSchoolMapping[schoolNodeMapping[school_name]] = school_name
                buildEdgeForRow(row)
            row_idx += 1

        buildSourceToSchoolsEdges()
        buildDatesToSinkEdges()
        buildSinkConstraint()


def buildDateNodesForRow(row):
    dates = row[2:]
    for i, date in enumerate(dates):
        rowIndex = i + 2
        date = dates[i]
        dateNodeMapping[date] = assignNode()
        nodeDateMapping[dateNodeMapping[date]] = date
        rowIndexToDate[rowIndex] = date


def buildEdgeForRow(row):
    [school_name, school_cost] = row[:2]
    school_node = schoolNodeMapping[school_name]
    cells = row[2:]

    global START_NODES
    global END_NODES
    global CAPACITIES
    global UNIT_COSTS

    for i, cell in enumerate(cells):
        row_index = i + 2
        if cell == '1':
            date_node = dateNodeMapping[rowIndexToDate[row_index]]

            START_NODES += [school_node]
            END_NODES += [date_node]
            CAPACITIES += [1]
            UNIT_COSTS += [int(float(school_cost) * 2)]


def buildSourceToSchoolsEdges():
    global START_NODES
    global END_NODES
    global CAPACITIES
    global UNIT_COSTS

    for value in schoolNodeMapping.values():
        START_NODES += [SOURCE_NODE_INDEX]
        END_NODES += [value]
        CAPACITIES += [1]
        UNIT_COSTS += [0]


def buildDatesToSinkEdges():
    global START_NODES
    global END_NODES
    global CAPACITIES
    global UNIT_COSTS

    for value in dateNodeMapping.values():
        START_NODES += [value]
        END_NODES += [SINK_CONSTRAINT_INDEX]
        CAPACITIES += [1]
        UNIT_COSTS += [0]


def buildSinkConstraint(c=20):
    global START_NODES
    global END_NODES
    global CAPACITIES
    global UNIT_COSTS

    START_NODES += [SINK_CONSTRAINT_INDEX]
    END_NODES += [SINK_NODE_INDEX]
    CAPACITIES += [c]
    UNIT_COSTS += [0]


def optimize():
    min_cost_flow = pywrapgraph.SimpleMinCostFlow()

    for i in range(0, len(START_NODES)):
        min_cost_flow.AddArcWithCapacityAndUnitCost(
            START_NODES[i],
            END_NODES[i],
            CAPACITIES[i],
            UNIT_COSTS[i]
        )

    min_cost_flow.SetNodeSupply(SOURCE_NODE_INDEX, 20)
    min_cost_flow.SetNodeSupply(SINK_NODE_INDEX, -20)

    if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
        for i in range(min_cost_flow.NumArcs()):
            schoolNode = min_cost_flow.Tail(i)
            dateNode = min_cost_flow.Head(i)
            flow = min_cost_flow.Flow(i)

            if (schoolNode != SOURCE_NODE_INDEX
                    and dateNode != SINK_CONSTRAINT_INDEX
                    and flow == 1):
                schoolName = nodeSchoolMapping[schoolNode]
                date = nodeDateMapping[dateNode]
                print(date + ": " + schoolName)

    else:
        print('There was an issue with the min cost flow input.')


if __name__ == "__main__":
    print("building...")
    parse()
    print("optimizing...")
    optimize()
    print("done")
