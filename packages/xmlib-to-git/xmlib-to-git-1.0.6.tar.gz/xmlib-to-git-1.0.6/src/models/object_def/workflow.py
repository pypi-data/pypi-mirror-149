# workflow.py


def creates_workflow(worflows, dir) -> None:
    t = open("{}/NODE.md".format(dir), "w+", encoding="utf-8")
    with t:
        t.write("\n## Node in workflow :\n")
        t.write("|s|a|\n|---|---|\n")
        for x in worflows:
            t.write("|{}|{}|\n".format(x["s"], x["a"]))
