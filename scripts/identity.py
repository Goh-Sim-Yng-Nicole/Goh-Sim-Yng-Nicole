"""
Single source of truth for who this profile belongs to.

Every generator imports from here, so the handle/name appear in exactly one
place instead of being hardcoded into each script's prompt strings.
"""
import os

# GitHub username -- must match the repo name for the profile README to render.
USERNAME = os.environ.get("GH_PROFILE_USER", "Goh-Sim-Yng-Nicole")

# Short handle used in the fake shell prompts ("nicole@github ~ $ ...").
HANDLE = os.environ.get("GH_PROFILE_HANDLE", "nicole")

# Display name printed by the `whoami` line under the portrait.
DISPLAY_NAME = os.environ.get("GH_PROFILE_NAME", "Nicole Goh")
