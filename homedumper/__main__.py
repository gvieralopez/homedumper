import pathlib
import typer
import homedumper
from homedumper.const import DEFAULT_OUT

app = typer.Typer()


@app.command()
def dump(video_path: str, output_path: str = DEFAULT_OUT):
    """
    Dumps the database from the video.

    Parameters
    ----------
    video_path : str
        Path to the video to extract frames from.
    output_path : str, optional
        Path to the output folder, by default DEFAULT_OUT
    """
    # Exctract frames from the video
    count = homedumper.extract(video_path=video_path, output_path=output_path)
    typer.echo(f"Extracted {count} frames from {video_path}")

    # Locate the project folder
    video_path = pathlib.Path(video_path)
    folder_path = pathlib.Path(output_path) / video_path.stem

    # Boxify the frames
    count = homedumper.boxify(folder_path=folder_path)
    typer.echo(f"{count} frames converted to box from {folder_path}")

    # Download resurces
    homedumper.download()
    typer.echo(f"All resources downloaded")

    # Match all thumbnails to pokemon names
    count = homedumper.match(path=folder_path)
    typer.echo(f"{count} pokemon found in {folder_path}")

@app.command()
def extract(video_path: str, output_path: str = DEFAULT_OUT):
    """
    Extract all different frames from the video.

    Parameters
    ----------
    video_path : str
        Path to the video to extract frames from.
    output_path : str, optional
        Path to the output folder, by default DEFAULT_OUT
    """
    count = homedumper.extract(video_path=video_path, output_path=output_path)
    typer.echo(f"Extracted {count} frames from {video_path}")


@app.command()
def boxify(folder_path: str):
    """
    Convert a folder with raw Pokemon Home screenshots of boxes into a folder
    structure with isolated images of each pokemon found.

    Parameters
    ----------
    folder_path : str
        Path to the folder that contains the 'frames' subfolder with the images.
    """

    count = homedumper.boxify(folder_path=folder_path)
    typer.echo(f"{count} frames converted to box from {folder_path}")


@app.command()
def match(folder_path: str):
    """
    Convert a folder structure with isolated images of each pokemon found into
    an annotated list of pokemon found in the images.

    Parameters
    ----------
    folder_path : str
        Path to the folder that contains the 'boxes' subfolder with the images.
    """

    count = homedumper.match(path=folder_path)
    typer.echo(f"{count} pokemon found in {folder_path}")


@app.command()
def download():
    """
    Download required templates.
    """
    homedumper.download()
    typer.echo(f"Download Completed")


if __name__ == "__main__":
    app()
