from threading import Thread

from IPython.core.display import display
from ipywidgets import Output, widgets

from servicefoundry.build.build import LOCAL, REMOTE, build_and_deploy
from servicefoundry.notebook.notebook_callback import NotebookOutputCallBack

thread = None


def deploy(project_folder, is_local=True):
    global thread
    output = Output(
        layout=widgets.Layout(
            width="100%", height="auto", max_height="200px", overflow="hidden scroll"
        )
    )

    if thread is not None and thread.is_alive():
        output.append_stdout("Stopping the old process.")
        thread.stop()
        thread.join()

    deployment = build_and_deploy(
        env="test",
        base_dir=project_folder,
        build=LOCAL if is_local else REMOTE,
        callback=NotebookOutputCallBack(output),
    )
    if isinstance(deployment, Thread):
        thread = deployment

    box = widgets.Box(
        children=[output], layout=widgets.Layout(width="100%", height="auto")
    )
    display(box)
