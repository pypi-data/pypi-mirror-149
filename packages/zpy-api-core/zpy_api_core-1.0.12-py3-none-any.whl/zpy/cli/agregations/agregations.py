# Templates
adds = {
    "di.py": {
        "type": "file",
        "module": "db-oracle",
        "path": "src/di.py",
        "code": {
            "imports": [
                "from zpy.utils import get_env_or_throw as var\n",
                "from zdb.oracle import ZOracle, ZDBConfig\n"
            ],
            "blocks": [
                "\n",
                "db_config: ZDBConfig = ZDBConfig(\"DB_USER\", \"DB_PASSWORD\", \"DB_NAME\",\"DB_HOST\", 1521,service=\"XE\")\n"
                "db_mngr: ZOracle = ZOracle.setup_of(db_config)\n"
                "\n",
                "if var('ENVIRONMENT') == 'local':\n",
                "   # Setup only the environment is local.\n",
                "   db_mngr.init_local_client(path= var('ORACLE_CLIENT_PATH'))\n",
                "\n"
            ]
        }
    },
    "context_imports": {
        "type": "file",
        "module": "db-oracle",
        "path": "src/di.py",
        "code": {
            "imports": [
                "\n"
                "# Imports of @context_name context 📦\n"
                "from contexts.@context_name import @usecase_class, @repository_name, @repository_impl\n"
            ],
            "blocks": [
                "\n# Creation of instances of use cases, repositories etc. of the context: @context_name 📦\n",
                "@context_name_repository: @repository_name = @repository_impl()\n"
                "@usecase_var_uc: UseCase[Any, Any] = @usecase_class(@context_name_repository)\n"
                "\n"
            ]
        }
    },
    "use-cases": {
        "type": "file",
        "module": "db-oracle",
        "path": "src/di.py",
        "code": {
            "imports": [
                "\n"
                "# Import use case of @context_name context 📦\n"
                "from contexts.@context_name.application.@usecase_file import @usecase_class\n"
            ],
            "blocks": [
                "\n# Creation instance of use cases of the context: @context_name 📦\n",
                "@usecase_var: UseCase[Any, Any] = @usecase_class(@context_name_repository)\n"
                "\n"
            ]
        }
    }
}
