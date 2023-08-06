# coding: utf-8
import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AppConfig:
    
    lodoc_search: str
    """
    Search string usse for lodoc commands such as:
    
    https://duckduckgo.com/?q={0}+site:api.libreoffice.org/docs/idl/
    """
    loguide_writer_url: str
    """Writer Dev Guide Url"""
    loguide_writer_search: str
    """Writer Dev Guide Search Url"""
    loguide_calc_url: str
    """Calc Dev Guide Url"""
    loguide_calc_search: str
    """Calc Dev Guide Search Url"""
    loguide_draw_url: str
    """Draw Dev Guide Url"""
    loguide_draw_search: str
    """Draw Dev Guide Search Url"""
    loguide_chart_url: str
    """Chart Dev Guide Url"""
    loguide_chart_search: str
    """Chart Dev Guide Search Url"""
    loguide_base_url: str
    """Base Dev Guide Url"""
    loguide_base_search: str
    """Base Dev Guide Search Url"""
    loguide_form_url: str
    """Form Dev Guide Url"""
    loguide_form_search: str
    """Form Dev Guide Search Url"""
    loguide_dev_url: str
    """Writer Dev Guide Url"""
    loguide_dev_search: str
    """Dev Guide Search Url"""
    loguide_url: str
    """Dev Guide Url"""

def read_config(config_file: str) -> AppConfig:
    """
    Gets config for given config file

    Args:
        config_file (str): Config file to load

    Returns:
        AppConfig: Configuration object
    """
    with open(config_file, 'r') as file:
        data = json.load(file)
        return AppConfig(**data)

def read_config_default() -> AppConfig:
    """
    Loads default configuration ``config.json``

    Returns:
        AppConfig: Configuration Object
    """
    root = Path(__file__).parent
    config_file = Path(root, 'config.json')
    return read_config(str(config_file))