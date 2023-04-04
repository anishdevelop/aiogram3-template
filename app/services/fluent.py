from typing import TYPE_CHECKING

from pathlib import Path

from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator, TranslatorRunner

if TYPE_CHECKING:
    from i18n_stub import TranslatorRunner

__all__ = (
    "generate_hub",
    "TranslatorRunner",
)


def generate_hub(locales_dir: Path, root_locale: str) -> TranslatorHub:
    """
    Generate TranslatorHub instance with FluentTranslator instances
    Search for all .ftl files in locales_dir and generate FluentTranslator for each locale
    :param locales_dir: Path to directory with .ftl files
    :param root_locale: Default locale
    :return: TranslatorHub instance
    """
    locales = [
        locale.stem for locale in locales_dir.glob("*") if locale.name.endswith(".ftl")
    ]

    return TranslatorHub(
        locales_map={
            locale: (locale, root_locale) if locale != root_locale else (locale,)
            for locale in locales
        },
        translators=[
            FluentTranslator(
                locale,
                translator=FluentBundle.from_files(
                    locale, [locales_dir / f"{locale}.ftl"]
                ),
            )
            for locale in locales
        ],
        root_locale=root_locale,
        separator="-",
    )
