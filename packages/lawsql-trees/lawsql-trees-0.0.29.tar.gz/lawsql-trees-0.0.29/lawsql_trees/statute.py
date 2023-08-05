import itertools
from dataclasses import dataclass
from datetime import date
from enum import Enum, auto, unique
from pathlib import Path
from typing import NoReturn

import yaml
from dateutil.parser import parse
from slugify import slugify
from statute_matcher import StatuteMatcher
from statute_serial_number import StatuteID, get_member
from treeish import fetch_values_from_key, set_node_ids

from .statute_formatter import format_units, get_first_short_title_from_units
from .statute_unformatted import (
    fix_absent_signer_problem,
    fix_multiple_sections_in_first,
)


@dataclass
class StatuteItem:
    """
    Utilizes `StatuteID` to get data from `*.yaml` files through the `category` and `idx` parameters. This will process data to generate a `StatuteItem` with titles that map to `TitleConvetions`."""

    path_to_statute_dir: Path

    def __post_init__(self):
        if not self.path_to_statute_dir.exists():
            raise Exception("Missing directory; cannot make StatuteItem.")

        self.category, self.idx = (
            self.path_to_statute_dir.parent.stem.upper(),
            self.path_to_statute_dir.stem.upper(),
        )

        self.member: StatuteID = get_member(self.category)

        self.category_label: str = self.get_category_label()

        self.data: dict = self.get_data

        self.specified_date: date = parse(self.data["date"]).date()

        self.units: list[dict] = self.data["units"]

        self.emails: list[str] = self.data.get("emails", None)

        self.effects: list[str] = self.data.get("effects", None)

        self.short_title = get_first_short_title_from_units(
            {"units": self.units}
        )

        self.serial_title = self.member.make_title(self.idx)

        self.aliases = self.data.get("aliases", [])

        self.titles: dict = {
            "short": self.short_title,
            "official": self.official_title,
            "serial": self.serial_title,
            "aliases": self.aliases,
        }

    @property
    def details_and_units(self) -> Path | NoReturn:
        folder = self.path_to_statute_dir

        details_path = folder / "details.yaml"
        if not details_path.exists():
            raise Exception(f"Could not find details.yaml")

        premade = folder / f"{self.category}{self.idx}.yaml"
        if premade.exists():
            return details_path, premade

        scraped = folder / "units.yaml"
        if scraped.exists():
            return details_path, scraped

        raise Exception(f"Could not find units.yaml")

    def get_category_label(self):
        text = self.member.value[0]
        if the_word_number := self.member.value[1]:
            text = f"{text} {the_word_number}"  # e.g. No./Blg. if present
        return text

    @property
    def get_data(self) -> NoReturn | dict:
        result = self.details_and_units
        if not result:
            raise Exception(f"Could not find details / units")

        detail_path, units_path = result

        raw_data = yaml.load(
            detail_path.read_text(),
            Loader=yaml.SafeLoader,
        )
        raw_data["units"] = yaml.load(
            units_path.read_text(),
            Loader=yaml.SafeLoader,
        )

        if "date" not in raw_data:
            raise Exception(f"Date missing from StatuteItem")

        if "units" not in raw_data:
            raise Exception(f"Units missing from StatuteItem")

        if not isinstance(raw_data["units"], list):
            raise Exception(f"Units not properly formatted")

        raw_data = fix_absent_signer_problem(raw_data)
        raw_data = fix_multiple_sections_in_first(raw_data)

        format_units(raw_data["units"])  # adds a short title, if possible
        set_node_ids(raw_data["units"])  # adds id to each node

        return raw_data

    @property
    def effective_actions(self) -> list[dict]:
        """Parse the data for all values with the key `effects`"""
        return list(
            itertools.chain(*fetch_values_from_key(self.data, "effects"))
        )

    @property
    def official_title(self) -> str | None:
        return self.data.get("law_title", None) or self.data.get("item", None)

    @property
    def slug(self) -> str:
        return slugify(f"{self.category}-{self.idx}-{self.data['date']}")


def get_statute_title_convention_choices() -> list[str]:
    """Get the names of each member of the `TitleConventions` enum"""

    @unique
    class StatuteTitleConventions(Enum):
        SERIAL = auto()  # e.g. Republic Act No. 386
        SHORT = auto()  # e.g. Civil Code of the Philippines
        OFFICIAL = auto()  # e.g. An Act to Ordain and Institute the...
        ALIAS = auto()  # e.g. New Civil Code

    return [name for name, _ in StatuteTitleConventions.__members__.items()]


def get_statute_on_local(text: str) -> StatuteItem | None:
    """Given text denominated as a statute by `StatuteMatcher`, e.g. 'Republic Act No. 386', 'Civil Code', get a prefilled `StatuteItem` from the local `rawlaw` repository.
    >>> x = get_statute_on_local("Republic Act No. 10410")
    StatuteItem(category='RA', idx='10410')
    """
    try:
        if match := StatuteMatcher.get_single_category_idx(text):
            return StatuteItem(match[0], match[1])
    except Exception as e:
        print(f"{e}")
    return None
