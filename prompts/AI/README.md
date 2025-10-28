### FoundationModels

https://cloud.ru/docs/foundation-models/ug/topics/quickstart


### Install VisualStudioCode, KiloCode

### Install Cloud.ru ContainerApps MCP 
https://github.com/Nick1994209/cloudru-containerapps-mcp

go install github.com/Nick1994209/cloudru-containerapps-mcp/cmd/cloudru-containerapps-mcp@latest

{
  "mcpServers": {
    "cloudru-containerapps-mcp": {
      "command": "cloudru-containerapps-mcp",
      "args": [],
      "env": {
        "CLOUDRU_KEY_ID": "********",
        "CLOUDRU_KEY_SECRET": "********",
        "CLOUDRU_PROJECT_ID": "a9e46dcd-b00a-4a87-8ec2-028b31931c7b",
      },
      "alwaysAllow": [
        "cloudru_containerapps_description",
        "cloudru_get_containerapp",
        "cloudru_get_list_containerapps",
        "cloudru_start_containerapp",
        "cloudru_get_list_docker_registries"
      ],
      "timeout": 900,
      "disabledTools": []
    }
  }
}