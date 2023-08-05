import itertools
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import NoReturn

import yaml
from citation_decision import CitationDocument
from dateutil.parser import parse
from slugify import slugify
from statute_matcher import StatuteMatcher
from treeish import fetch_values_from_key, set_node_ids

from .statute_formatter import format_units


@dataclass
class CodificationItem:
    """Each validated yaml file is parsed to create a `CodificationItem`.

    Upon loading the the file, the following properties validate:
    1. `complete_data`
    2. `get_units`
    3. `statutes_in_sync`
    4. `get_histories`

    If validation does not raise any exceptions, pull history data from `get_histories`.

    Aside from generic metadata, this dataclass contains two complex keys:
    1. `units`: A list of nested `unit` dicts - each `unit` may contain a `history`.
    2. `histories`: A list of `history` dicts - each `history` indicates a `Statute` or a `Decision`.

    Each `unit` of object's `units` represent an element of the `base` Statute as modified by the `requisites`.
    """

    path_to_code_yaml: Path

    def __post_init__(self):
        self.data: dict = self.fetch_complete_data_from_file
        self.publication_date: date = parse(self.data["date"]).date()
        self.sync = self.statutes_in_sync
        self.units: list[dict] = self.data["units"]
        self.version = str(self.data["version"])
        self.emails: list[str] = self.data["emails"]
        self.title = self.data["title"]
        self.description = self.data["description"]
        self.base = self.data["base"]
        self.histories: list[dict] = self.get_histories

    @property
    def fetch_complete_data_from_file(self) -> NoReturn | dict:
        """If there are any missing keys, raise error."""
        text = self.path_to_code_yaml.read_text()
        raw_data = yaml.load(text, Loader=yaml.SafeLoader)
        for key in [
            "title",
            "description",
            "version",
            "emails",
            "date",
            "version",
            "base",
            "requisites",
            "units",
        ]:
            if key not in raw_data:
                raise Exception(f"Missing {key}")
        format_units(raw_data["units"])  # fixes item, caption, content
        self.format_citations(
            raw_data["units"]
        )  # adjusts the canonical citations
        set_node_ids(raw_data["units"])  # adds id to each node

        return raw_data

    def format_citations(self, nodes: list[dict]) -> None:
        for node in nodes:
            if histories := node.get("history", None):
                for history in histories:
                    if history.get("citation", None):
                        doc = CitationDocument(history["citation"])
                        history["citation"] = doc.first_canonical
            if new_nodes := node.get("units", None):
                self.format_citations(new_nodes)  # call self

    @property
    def statutes_from_histories(self) -> set[str] | NoReturn:
        """Get all strings of Statutes found in the "statute" key in the nested dictionary"""
        if not (blocks := set(fetch_values_from_key(self.data, "statute"))):
            raise Exception(f"No statute blocks found; see {blocks=}")
        return blocks

    @property
    def decisions_from_citations(self) -> list[str]:
        return list(set(fetch_values_from_key(self.data, "citation")))

    @property
    def requisites_sans_base(self) -> set[str]:
        """Get set of texts representing statute serial names without the base statute for the codification."""
        return set(self.data["requisites"])

    @property
    def statutes_in_requisites(self) -> set[str]:
        """Get set of texts representing statute serial names with the base statute for the codification."""
        return set(self.data["requisites"] + [self.data["base"]])

    @property
    def statutes_in_sync(self) -> bool | NoReturn:
        """Indicates that Statutes found in history blocks match stated requisites."""
        if err := self.statutes_from_histories - self.statutes_in_requisites:
            raise Exception(f"In body not in requisites: {str(err)=}")
        if err := self.statutes_in_requisites - self.statutes_from_histories:
            raise Exception(f"In requisites not in body: {str(err)=}")
        return True

    @property
    def get_history_lists(self) -> list[list[dict]] | NoReturn:
        """Each unit may have its history; each history is a list of blocks"""
        if not (l := list(fetch_values_from_key(self.data, "history"))):
            raise Exception(f"No history blocks; see {l=}")
        return l

    @property
    def get_histories(self) -> list[dict] | NoReturn:
        """Get histories by flattening list (chain)"""
        return list(itertools.chain(*self.get_history_lists))

    @property
    def slug(self) -> str:
        matched = StatuteMatcher(self.base).matches[0]
        cat = matched.category
        idx = matched.identifier
        year = self.publication_date.year
        version = f"v{self.version}"
        folder = self.path_to_code_yaml.parent.stem
        slug = slugify(f"{cat}-{idx}-pubyear-{year}-{version}-by-{folder}")
        return slug
