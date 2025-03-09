:: Create the src directory if it doesn't exist
mkdir src

:: Move core application files
move main.py src\main.py
move main_window.py src\main_window.py
move main_gui.py src\main_gui.py
move integrated_app.py src\integrated_app.py

echo Core application files organized into src\ directory.

:: Create the gui directory if it doesn't exist
mkdir gui

:: Move GUI-related files
move login_dialog.py gui\login_dialog.py
move collaboration_dialog.py gui\collaboration_dialog.py
move contribution_dialog.py gui\contribution_dialog.py
move user_management_dialog.py gui\user_management_dialog.py

echo GUI components organized into gui\ directory.

:: Create the services directory if it doesn't exist
mkdir services

:: Move service-related files
move ai_integration.py services\ai_integration.py
move shodan_integration.py services\shodan_integration.py
move wayback_machine_integration.py services\wayback_integration.py
move tool_manager.py services\tool_manager.py

echo Service files organized into services\ directory.

:: Create the models directory if it doesn't exist
mkdir models

:: Move model-related files
move Nuclei\nuclei_template_model.py models\nuclei_template.py
move scan_target.py models\scan_target.py
move vulnerability_database.py models\vulnerability_db.py

echo Model files organized into models\ directory.

:: Create the config directory if it doesn't exist
mkdir config

:: Move configuration files
move config.json config\config.json
move config.template.json config\template.json
move config_updated.json config\updated.json
move config.py config\config.py
move scanning_profiles.json config\scanning_profiles.json
move tools.yml config\tools.yml
move nuclei.yaml config\nuclei.yaml
move amass.ini config\amass.ini

echo Configuration files organized into config\ directory.

:: Create the docs directory if it doesn't exist
mkdir docs

:: Move documentation files
move BugHunterScannerDocumentation.md docs\scanner.md
move knowledge_file.md docs\knowledge.md
move improvements.md docs\improvements.md
move README.md docs\README.md
move README-new.md docs\README_new.md
move README-updated.md docs\README_updated.md

echo Documentation files organized into docs\ directory.

:: Create the tests directory and subdirectories
mkdir tests
mkdir tests\openai
mkdir tests\nuclei
mkdir tests\logging
mkdir tests\output

:: Move test files
move test_openai_config.py tests\openai\test_config.py
move test_openai_console.py tests\openai\test_console.py
move test_openai_direct.py tests\openai\test_direct.py
move test_openai_file.py tests\openai\test_file.py
move test_openai_final.py tests\openai\test_final.py
move test_openai_stderr.py tests\openai\test_stderr.py
move test_openai_with_file.py tests\openai\test_with_file.py
move test_openai_with_logs.py tests\openai\test_with_logs.py
move test_openai.py tests\openai\test_main.py
move test_output.txt tests\output\test_output.txt
move test_doc.py tests\nuclei\test_doc.py
move test_cython_templating.py tests\nuclei\test_cython.py
move simple_log_test.py tests\logging\test_simple.py

echo Test files organized into tests\ directory.

:: Create the utils directory if it doesn't exist
mkdir utils

:: Move utility files
move setup.py utils\setup.py
move setup_database.py utils\setup_db.py
move setup_environment.py utils\setup_env.py
move update_tools.py utils\update_tools.py
move install.py utils\install.py
move install_app.py utils\install_app.py
move check_config.py utils\check_config.py
move check_env.bat utils\check_env.bat
move check_env.ps1 utils\check_env.ps1
move logger_config.py utils\logger_config.py
move notification.py utils\notification.py
move role_manager.py utils\role_manager.py
move scope_manager.py utils\scope_manager.py

echo Utility files organized into utils\ directory.

:: Create the data directory if it doesn't exist
mkdir data

:: Move data files
move database_schema.sql data\schema.sql
move debug_output.txt data\debug_output.txt
move training_ui.py data\training_ui.py
move write_check.py data\write_check.py
move write_test.py data\write_test.py

echo Data files organized into data\ directory.