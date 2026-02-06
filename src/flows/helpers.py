import os
import yaml
from datetime import datetime


def load_flow_config(config_path: str) -> dict:
    """Reads flow configuration from a YAML file."""
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        print(f"Loaded config from {config_path}")
        return config
    except Exception as e:
        raise RuntimeError(f"Failed to load flow configuration from {config_path}: {e}")


def setup_output_directory(config: dict) -> str:
    """Handles folder validation, archiving, and creation. Returns the final output path."""
    save_folder = config.get("save_folder", "output")
    project_name = config.get("project_name", "project")
    version = config.get("version", "v1.0.0")

    dir_name = f"{project_name}_{version}"
    target_dir = os.path.join(save_folder, dir_name)

    if os.path.exists(target_dir):
        # Check if directory is empty
        is_empty = len(os.listdir(target_dir)) == 0

        if is_empty:
            print(f"Directory {target_dir} exists but is empty. Continuing to use it.")
        else:
            # Directory is not empty, rename it with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_dir = f"{target_dir}_{timestamp}"
            print(
                f"Directory not empty. Renaming existing {target_dir} to {archive_dir}"
            )
            try:
                os.rename(target_dir, archive_dir)
                print(f"Creating fresh directory: {target_dir}")
                os.makedirs(target_dir, exist_ok=True)
            except Exception as e:
                raise RuntimeError(
                    f"Failed to archive existing directory {target_dir}: {e}"
                )
    else:
        print(f"Creating fresh directory: {target_dir}")
        os.makedirs(target_dir, exist_ok=True)

    return target_dir


def initialize_workspace(config_path: str, idea_path: str) -> dict:
    """
    Combines configuration loading, idea loading, and output directory setup.
    Returns a dictionary containing the loaded config, init_idea, and output_path.
    """
    config = load_flow_config(config_path)
    output_path = setup_output_directory(config)

    return {"config": config, "output_path": output_path}
