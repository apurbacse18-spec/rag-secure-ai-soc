def classify_threat(query: str):
    q = query.lower()

    threat_patterns = {
        "prompt_injection": [
            "ignore previous instructions",
            "ignore all previous instructions",
            "bypass safety",
            "reveal system prompt",
            "show system prompt",
            "system prompt",
            "act as admin",
            "override instructions"
        ],
        "sql_injection": [
            "select * from",
            "drop table",
            "union select",
            "' or '1'='1",
            "\" or \"1\"=\"1",
            "--",
            ";--"
        ],
        "data_exfiltration": [
            "dump database",
            "show all data",
            "export all records",
            "leak data",
            "reveal confidential data"
        ],
        "command_injection": [
            "rm -rf",
            "del /f",
            "shutdown /s",
            "wget http",
            "curl http",
            "powershell -enc",
            "cmd /c"
        ]
    }

    for threat_type, patterns in threat_patterns.items():
        for pattern in patterns:
            if pattern in q:
                return threat_type

    return None