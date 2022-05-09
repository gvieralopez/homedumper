import typer
import homedumper
from homedumper.const import DEFAULT_OUT

app = typer.Typer()

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

if __name__ == "__main__":    
    app()