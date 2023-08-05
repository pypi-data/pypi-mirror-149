#! /usr/bin/env python3

import click
import os
from shutil import which

script_file = "script.txt"
recording_directory_name = "Recordings"
recording_format = "wav"
script_segments = {}


def test_sox_exists():
    try:
        assert which("sox")
    except AssertionError:
        print("Cant find sox.  Install sox somewhere in your path.")
        exit(1)


def get_recording_file_name(slug):
    return f"{recording_directory_name}/{slug}.{recording_format}"


def project_prep():
    if not os.path.exists(recording_directory_name):
        os.makedirs(recording_directory_name)
    if not os.path.exists(f"{recording_directory_name}/Archive"):
        os.makedirs(f"{recording_directory_name}/Archive")


def wait_for_input():
    click.echo("*" * 40)
    _ = input("Press ENTER to Continue")


def add_slug_text(slug, text):
    script_segments[slug] = text


def recording_exists(slug):
    if os.path.isfile(get_recording_file_name(slug)):
        return True
    return False


def script_exists():
    if os.path.isfile(script_file):
        return True
    return False


def noise_profile_missing():
    if os.path.isfile(f"{recording_directory_name}/noise.prof"):
        return False
    return True


def combined_recording_exists():
    if os.path.isfile(f"{recording_directory_name}/combined.{recording_format}"):
        return True
    return False


def truncate_audio(slug):
    recording = get_recording_file_name(slug)
    new_recording = f"{recording_directory_name}/{slug}-truncated.{recording_format}"
    click.echo(f"truncating {recording}")

    SOX_CMD = (
        f"sox -V2 {recording}  {new_recording}   silence -l 1 0.1 .1% -1 1.0 .1%   stat"
    )
    click.echo(SOX_CMD)
    os.system(SOX_CMD)
    os.system(
        f" mv -v {recording} {recording_directory_name}/Archive/{slug}.{recording_format}"
    )
    os.rename(new_recording, recording)
    review_audio(slug)


def play_audio(slug):
    recording = get_recording_file_name(slug)
    click.echo(f"Playing {recording}")
    os.system(f"play {recording}")
    review_audio(slug)


def delete_audio(slug):
    recording = get_recording_file_name(slug)
    os.remove(recording)


def review_audio(slug):
    review_menu = ["(p)lay", "(a)ccept", "(r)eccord again", "(t)runcate"]
    click.echo(slug)
    for i in review_menu:
        click.echo(i)
    menu_action = input(">> ")
    if menu_action == "p":
        play_audio(slug)
    elif menu_action == "a":
        exit()
    elif menu_action == "r":
        delete_audio(slug)
        find_and_record_next()
    elif menu_action == "t":
        truncate_audio(slug)
    else:
        review_audio(slug)


def record_audio(slug):
    new_recording = get_recording_file_name(slug)
    click.echo(f"Creating {new_recording}")
    click.echo("press Enter to start then CRTL-C to quit")
    wait_for_input()
    os.system(f"rec {new_recording}")


def record_silent_audio():
    silent_recording = f"{recording_directory_name}/silence.{recording_format}"
    click.echo("RECORD 5 SECONDS OF SILENCE \n" * 5)
    click.echo("press Enter to start")
    wait_for_input()
    os.system(f"rec {silent_recording} trim 0 5")
    os.system(
        f"sox {silent_recording} -n noiseprof {recording_directory_name}/noise.prof"
    )


def load_script():
    linetext = ""
    with open(script_file) as script_file_reader:
        for line in script_file_reader.readlines():

            if not line.strip():

                slug = linetext[:40].title()
                segment_name = "".join(filter(str.isalnum, slug))
                add_slug_text(segment_name, linetext)
                linetext = ""

            else:
                linetext += f"{line}  \n"
    if not linetext == "":
        slug = linetext[:40].title()
        segment_name = "".join(filter(str.isalnum, slug))
        add_slug_text(segment_name, linetext)
        linetext = ""


def combine_recordings_for_export():
    recording_list = []
    combined_recording = f"{recording_directory_name}/combined.{recording_format}"
    for slug, text in script_segments.items():
        recording = get_recording_file_name(slug)
        recording_list.append(recording)
    recording_list_string = " ".join(recording_list)
    print(recording_list_string)
    SOX_CMD = f"sox  {recording_list_string}  {combined_recording} noisered {recording_directory_name}/noise.prof 0.21 norm -3"
    click.echo(SOX_CMD)
    os.system(SOX_CMD)


def find_and_record_next():
    for slug, text in script_segments.items():
        if recording_exists(slug):
            continue
        click.clear()
        click.echo(slug)
        click.echo("*" * 40)
        click.echo(text)
        click.echo("*" * 40)
        record_audio(slug)
        review_audio(slug)


def complete_segment_count():
    recorded_count = 0
    for slug, text in script_segments.items():
        if recording_exists(slug):
            recorded_count += 1
    return recorded_count


def print_status():

    segment_count = len(script_segments)
    complete = complete_segment_count()
    remaining = segment_count - complete
    if script_exists() is False:
        click.secho("No Script file", fg="red")
    else:
        click.echo("Segments:")
        click.echo(f"\t{segment_count} Total")
        click.echo(f"\t{complete_segment_count()} Complete")
        if remaining == 0:
            click.secho("All Segments Recorded", fg="green")
            if combined_recording_exists():
                click.secho("Combined Recording is Ready", fg="green")
            else:
                click.secho("No Combined Recording", fg="yellow")
        else:
            click.secho(f"\t{segment_count - complete} Remaining", fg="yellow")
    if noise_profile_missing():
        click.secho("No Noise Profile", fg="yellow")


@click.group()
def cli():
    test_sox_exists()
    if script_exists():
        load_script()
    pass


@cli.command()
def combine():
    "Combine Segments into single audio file"
    combine_recordings_for_export()


@cli.command()
def record():
    "Record next unrecorded segment"
    project_prep()
    if noise_profile_missing():
        record_silent_audio()
    find_and_record_next()


@cli.command()
def silence():
    "Generate noise profile"
    project_prep()
    record_silent_audio()


@cli.command()
def status():
    print_status()


# @cli.command()
# def print_recordings():
#    for slug, text in script_segments.items():
#        click.echo(slug, recording_exists(slug))


@cli.command()
def review():
    "Print segments"

    for slug, text in script_segments.items():
        click.clear()
        click.echo(slug)
        click.echo("*" * 40)
        click.echo()
        click.echo(text)
        wait_for_input()


if __name__ == "__main__":
    cli()
