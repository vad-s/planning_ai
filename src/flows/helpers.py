import os
import yaml
from datetime import datetime
from src.generic.init_idea import InitIdea

def load_flow_config(config_path: str) -> dict:
    """Reads flow configuration from a YAML file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        print(f"Loaded config from {config_path}")
        return config
    except Exception as e:
        raise RuntimeError(f"Failed to load flow configuration from {config_path}: {e}")

def load_init_idea(idea_path: str) -> InitIdea:
    """Loads and parses the initial idea from a YAML file."""
    try:
        if not os.path.exists(idea_path):
            print(f"Warning: Idea file {idea_path} not found.")
            return None
            
        with open(idea_path, 'r') as f:
            idea_data = yaml.safe_load(f)
        
        if "init_idea" in idea_data:
            print(f"Loaded InitIdea from {idea_path}")
            return InitIdea(**idea_data["init_idea"])
        else:
            print(f"Warning: 'init_idea' key not found in {idea_path}")
            return None
    except Exception as e:
        print(f"Error loading init_idea from {idea_path}: {e}")
        return None

def setup_output_directory(config: dict) -> str:
    """Handles folder validation, archiving, and creation. Returns the final output path."""
    save_folder = config.get('save_folder', 'output')
    project_name = config.get('project_name', 'project')
    version = config.get('version', 'v1.0.0')
    overwrite = config.get('overwrite', False)

    dir_name = f"{project_name}_{version}"
    target_dir = os.path.join(save_folder, dir_name)
    
    if os.path.exists(target_dir):
        if overwrite:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_dir = f"{target_dir}_{timestamp}"
            print(f"Archive enabled. Renaming existing {target_dir} to {archive_dir}")
            try:
                os.rename(target_dir, archive_dir)
            except Exception as e:
                raise RuntimeError(f"Failed to archive existing directory {target_dir}: {e}")
        else:
            print(f"Error: Version {version} for project {project_name} already exists and overwrite is False.")
            raise ValueError(f"Directory {target_dir} already exists and overwrite is False.")
    
    print(f"Creating fresh directory: {target_dir}")
    os.makedirs(target_dir, exist_ok=True)
    return target_dir
    
def initialize_workspace(config_path: str, idea_path: str) -> dict:
    """
    Combines configuration loading, idea loading, and output directory setup.
    Returns a dictionary containing the loaded config, init_idea, and output_path.
    """
    config = load_flow_config(config_path)
    init_idea = load_init_idea(idea_path)
    output_path = setup_output_directory(config)
    
    return {
        "config": config,
        "init_idea": init_idea,
        "output_path": output_path
    }
