#!/usr/bin/env python
#
# Requires:
# conda create -n prefect -c ome -c conda-forge prefect
#

from prefect import Flow, Parameter, task
from prefect.tasks.shell import ShellTask
from prefect.utilities.debug import raise_on_exception


object = Parameter("object")


shell = ShellTask(
    return_all=True,
    log_stderr=True)


COMMAND = "/opt/omero/server/OMERO.server/bin/omero"

BULK_OPTIONS = "--file /uod/idr/metadata/idr0090-ashdown-malaria/screenA/idr0090-screenA-annotation.csv"

BULKMAP_OPTIONS = "--context bulkmap --batch 500 --wait 300 --cfg /uod/idr/metadata/idr0090-ashdown-malaria/screenA/idr0090-screenA-render.yml"

RENDER_CONFIG = "/uod/idr/metadata/idr0090-ashdown-malaria/screenA/idr0090-screenA-render.yml"


@task
def print_output(prefix, output):
    print(prefix, output)
    return output


@task
def annotate_bulk(object, ignore):
    return f"{COMMAND} metadata populate {BULK_OPTIONS} {object}"


@task
def annotate_bulk2map(object, ignore):
    return f"{COMMAND} metadata populate {BULKMAP_OPTIONS} {object}"

@task
def render(object, ignore):
    return f"{COMMAND} render set {object} {RENDER_CONFIG}"


with Flow("idr0090") as flow:
    key = shell(command=f"{COMMAND} sessions key")
    bulk = shell(annotate_bulk(object, key))
    bulk2map = shell(annotate_bulk2map(object, bulk))
    shell(render(object, bulk2map))

if __name__ == "__main__":
    with raise_on_exception():
        flow.run(object="Screen:2851")
