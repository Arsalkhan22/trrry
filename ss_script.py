#!/usr/bin/python
"""
STATIC WORDPRESS: WordPress as Static Site Generator
A Python Package for Converting WordPress Installation to a Static Website
"""
import os
import sys
import logging
from pathlib import Path

from src.staticwordpress.core.workflow import Workflow
from src.staticwordpress.core.constants import SOURCE, HOST
from src.staticwordpress.utils.validators import validate_url, validate_output_path

def validate_environment():
    """Validate required environment variables"""
    required_vars = {
        "user": os.environ.get("user"),
        "token": os.environ.get("token"),
        "src": os.environ.get("src"),
        "dst": os.environ.get("dst")
    }
    
    for var_name, value in required_vars.items():
        if not value:
            raise ValueError(f"Missing required environment variable: {var_name}")
        if var_name in ["src", "dst"] and not validate_url(value):
            raise ValueError(f"Invalid URL in environment variable: {var_name}")
    
    return required_vars

def main():
    """Main execution function"""
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
        stream=sys.stdout,
    )

    try:
        # Validate environment
        env_vars = validate_environment()
        
        # Get optional environment variables with defaults
        env_404 = os.environ.get("404", "404-error")
        env_search = os.environ.get("search", "search")
        env_output = os.environ.get("output", "output")

        if not validate_output_path(env_output):
            raise ValueError("Invalid output path")

        # Create output path
        Path(env_output).mkdir(parents=True, exist_ok=True)

        # Initialize and run workflow
        workflow = Workflow()
        workflow.create_project(
            project_name_="simply-static-zip-deploy",
            wp_user_=env_vars["user"],
            wp_api_token_=env_vars["token"],
            src_url_=env_vars["src"],
            dst_url_=env_vars["dst"],
            output_folder_=env_output,
            custom_404_=env_404,
            custom_search_=env_search,
            src_type_=SOURCE.ZIP,
            host_type_=HOST.NETLIFY,
        )

        # Execute workflow steps
        workflow.download_zip_file()
        workflow.setup_zip_folders()
        workflow.add_404_page()
        workflow.add_robots_txt()
        workflow.add_redirects()
        workflow.add_search()

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()