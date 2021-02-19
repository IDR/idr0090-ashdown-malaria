#!/usr/bin/env python
#
# Requires:
# conda create -n prefect -c ome -c conda-forge prefect
#

from prefect import Flow, Parameter, task
from prefsect.tasks.shell import ShellTask
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
def annotate_bulk(object):
    return f"{COMMAND} metadata populate {BULK_OPTIONS} {object}"


@task
def annotate_bulk2map(object):
    return f"{COMMAND} metadata populate {BULKMAP_OPTIONS}{object}"

@task
def render(object):
    return f"{COMMAND} render set {object} {RENDER_CONFIG}"


with Flow("idr0090") as flow:
    key = shell(command="omero sessions key")
    shell(annotate_bulk(object))
    shell(annotate_bulk2map(object))
    shell(render(object))

if __name__ == "__main__":
    with raise_on_exception():
        flow.run(screen="Screen:2851")
