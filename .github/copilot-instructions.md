# GitHub Copilot Instructions

## Overview
This document provides guidelines for using GitHub Copilot effectively within the `const-collection-full-stack-hackathon` project. It outlines the architecture, workflows, conventions, and integration points to enhance productivity.

## Architecture
- **Project Structure**: The project is organized into several apps, each handling different functionalities. The main apps include:
  - `collections_app`
  - `events_app`
  - `owner_app`
  - `store_app`

## Workflows
- **Development Workflow**: Follow the standard Git workflow for branching and merging. Use feature branches for new features and bug fixes.
- **Testing**: Ensure all tests are written in the respective `tests.py` files within each app. Run tests frequently to maintain code quality.

## Conventions
- **Code Style**: Adhere to PEP 8 guidelines for Python code. Use meaningful variable and function names.
- **Documentation**: Document all public functions and classes using docstrings.

## Integration Points
- **Static Files**: Manage static files in the `static/` directory. Ensure all assets are properly linked in templates.
- **Templates**: Use the `templates/` directory for HTML files. Follow the naming conventions for easy identification.

## Examples
- **Creating a New View**: When creating a new view, ensure to add it to the respective `urls.py` file and document its purpose.
- **Adding a New Model**: Define the model in `models.py`, run migrations, and update the admin interface if necessary.

## Conclusion
By following these guidelines, developers can leverage GitHub Copilot to enhance their coding efficiency and maintain a high standard of code quality.