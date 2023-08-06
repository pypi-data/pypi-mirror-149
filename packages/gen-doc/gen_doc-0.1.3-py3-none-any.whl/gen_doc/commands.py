"""
commands to build documentation
"""

import click

from gen_doc.doc_generator import DocGenerator
from gen_doc.extensions import GenDocParsers
from gen_doc.serializers import GenDocSerializers
from gen_doc.utils.config_handler import copy_config, load_config

from .utils.command_utils import GroupWithCommandOptions
from .utils.utils import get_version


@click.group(
    help="Utility for generating project documentation from docstrings",
    cls=GroupWithCommandOptions,
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.option(
    "-v",
    "--version",
    "version",
    is_flag=True,
    required=False,
    default=False,
    help="Get library version",
    type=bool,
)
@click.option(
    "-i",
    "--init",
    "init_var",
    is_flag=True,
    required=False,
    default=False,
    help="Init gen_doc config with default parameters",
    type=bool,
)
@click.option(
    "-b",
    "--build",
    "build_var",
    is_flag=True,
    required=False,
    default=False,
    help="Build documentation by config",
    type=bool,
)
@click.pass_context
def entry_point(ctx, version, init_var, build_var):
    if version:
        print("GenDoc Version:", get_version())
    if init_var:
        ctx.invoke(init)
    if build_var:
        ctx.invoke(build, config=True)


@entry_point.command(
    "init",
    help="To init config file in order to generate documentation.",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.option(
    "-f",
    "--file-config",
    "file_config",
    show_default=True,
    required=False,
    default="gen_doc.yaml",
    help="Config file name",
    type=str,
)
@click.option(
    "-o",
    "--overwrite",
    "overwrite",
    is_flag=True,
    required=False,
    default=False,
    help="To overwrite, in case file already exists",
    type=bool,
)
def init(file_config: str = "gen_doc.yaml", overwrite: bool = False, *args, **kwargs):
    welcome_string = """Config was created"""
    is_correct = copy_config(file_config, overwrite)
    if not is_correct:
        return
    print(welcome_string)


@entry_point.command(
    "build",
    help="Build documentation",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.argument(
    "language",
    required=False,
    default="py",
    type=click.Choice([i.name for i in GenDocParsers]),
)
@click.option(
    "-sm",
    "--save-mode",
    "save_mode",
    required=False,
    default="md",
    help="Save mode",
    type=click.Choice([i.name for i in GenDocSerializers]),
)
@click.option(
    "-hi",
    "--hierarchically",
    "hierarchically",
    is_flag=True,
    required=False,
    default=True,
    help="Extract with the same hierarchy",
    type=bool,
)
@click.option(
    "-o",
    "--overwrite",
    "overwrite",
    is_flag=True,
    required=False,
    default=True,
    help="To overwrite, in case file already exists",
    type=bool,
)
@click.option(
    "-p2r",
    "--path-to-root",
    "path_to_root",
    required=False,
    default=None,
    help="Path to the directory for which documentation should be compiled",
    type=str,
)
@click.option(
    "-p2s",
    "--path-to-save",
    "path_to_save",
    required=False,
    default=None,
    help="Path to the directory where the documentation should be saved",
    type=str,
)
@click.option(
    "-f2s",
    "--file-to-save",
    "file_to_save",
    required=False,
    default=None,
    help="Path to the directory where the documentation should be saved",
    type=str,
)
@click.option(
    "-c",
    "--config",
    "config",
    is_flag=True,
    required=False,
    default=False,
    help="Use config for build documentation.",
    type=bool,
)
@click.option(
    "-f",
    "--file-config",
    "file_config",
    show_default=True,
    required=False,
    default="gen_doc.yaml",
    help="Config file name",
    type=str,
)
def build(
    language,
    save_mode,
    path_to_root,
    config,
    hierarchically,
    overwrite,
    path_to_save,
    file_to_save,
    file_config,
    *args,
    **kwargs,
):
    if config:
        configs = load_config(file_config)
        if configs is None:
            print("No config file to build. Use `gen_doc init` to initiate the config.")
            return
        elif not configs:
            print("Specified incorrectly or broken file")
            return
        options = configs.get("OPTIONS", dict())
        author = configs.get("AUTHOR", dict())
        project = configs.get("PROJECT", dict())
        allowed_parsers = [parser.name for parser in GenDocParsers]
        if "language" not in options:
            print(
                "Please don't drop required fields from the config."
                "Add `language` field to the config and try again."
            )
            return
        if options["language"] not in allowed_parsers:
            print(
                f"You specified unavailable value for languages."
                f"Available values are: {allowed_parsers}"
            )
            return
        parser = DocGenerator(
            parse_mode=options["language"],
            path_to_root_folder=options.get("path_to_root_folder", None),
            extract_with_same_hierarchy=options.get(
                "extract_with_same_hierarchy", True
            ),
            overwrite_if_file_exists=options.get("overwrite_if_file_exists", False),
            path_to_save=options.get("path_to_save", None),
            file_to_save=options.get("file_to_save", None),
            save_mode=options.get("save_mode", "md"),
            additional_files_to_ignore=options.get("additional_files_to_ignore", None),
            additional_folders_to_ignore=options.get(
                "additional_folders_to_ignore", None
            ),
            title=project.get("title"),
            description=project.get("description"),
            repository_main_url=project.get("repository"),
            release=project.get("release"),
            author=author.get("author"),
            author_contacts=author.get("author_contacts"),
        )
    else:
        parser = DocGenerator(
            parse_mode=language,
            path_to_root_folder=path_to_root,
            extract_with_same_hierarchy=hierarchically,
            overwrite_if_file_exists=overwrite,
            path_to_save=path_to_save,
            file_to_save=file_to_save,
            save_mode=save_mode,
        )
    parser.generate()


if __name__ == "__main__":
    entry_point()
